"""
Script pour identifier et supprimer les portraits d'enfants (âge < 21 ans)
Utilise DeepFace pour détecter l'âge et déplace les portraits inappropriés
"""
import os
import json
import shutil
from pathlib import Path
from tqdm import tqdm
from deepface import DeepFace
import cv2

# Limiter l'utilisation mémoire
os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# Configuration
MIN_AGE = 21  # Âge minimum autorisé
PORTRAITS_DIR = Path("/app/backend/static/realistic_portraits")
BACKUP_DIR = Path("/app/backend/static/realistic_portraits_backup_children")
REPORT_FILE = Path("/app/backend/children_removal_report.json")

# Dossiers à scanner (tous les sous-dossiers d'ethnicités avec genres)
PORTRAIT_FOLDERS = [
    "africa/black/M",
    "africa/black/F",
    "asia/asian/M",
    "asia/asian/F",
    "asia/indian/M",
    "asia/indian/F",
    "europe/white/M",
    "europe/white/F",
    "america/white/M",
    "america/white/F",
    "america/latino_hispanic/M",
    "america/latino_hispanic/F",
    "middle_east/middle_eastern/M",
    "middle_east/middle_eastern/F",
    "oceania/white/M",
    "oceania/white/F"
]

class ChildrenPortraitRemover:
    def __init__(self):
        self.portraits_dir = PORTRAITS_DIR
        self.backup_dir = BACKUP_DIR
        self.report_file = REPORT_FILE
        self.removed_portraits = []
        self.scanned_count = 0
        self.error_count = 0
        
        # Créer le dossier de backup
        self.backup_dir.mkdir(parents=True, exist_ok=True)
    
    def check_age(self, image_path: Path) -> dict:
        """Vérifie l'âge d'un portrait avec DeepFace"""
        try:
            # Analyser avec DeepFace
            analysis = DeepFace.analyze(
                img_path=str(image_path),
                actions=['age'],
                enforce_detection=False,
                detector_backend='opencv',
                silent=True
            )
            
            # DeepFace peut retourner une liste ou un dict
            if isinstance(analysis, list):
                analysis = analysis[0]
            
            age = analysis.get('age', None)
            
            return {
                'success': True,
                'age': age,
                'error': None
            }
            
        except Exception as e:
            return {
                'success': False,
                'age': None,
                'error': str(e)
            }
    
    def move_to_backup(self, image_path: Path, age: int, relative_path: str):
        """Déplace un portrait vers le dossier de backup"""
        # Créer la structure de dossier dans le backup
        backup_path = self.backup_dir / relative_path / image_path.name
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Déplacer le fichier
        shutil.move(str(image_path), str(backup_path))
        
        # Enregistrer dans le rapport
        self.removed_portraits.append({
            'original_path': str(image_path),
            'backup_path': str(backup_path),
            'age': age,
            'filename': image_path.name,
            'folder': relative_path
        })
    
    def scan_and_remove(self):
        """Scanne tous les dossiers et supprime les portraits d'enfants"""
        print(f"\n🔍 Scan des portraits pour détecter les enfants (âge < {MIN_AGE} ans)...")
        print(f"📁 Dossier: {self.portraits_dir}")
        print(f"💾 Backup: {self.backup_dir}\n")
        
        # Scanner chaque dossier
        for folder in PORTRAIT_FOLDERS:
            folder_path = self.portraits_dir / folder
            
            # Vérifier si le dossier existe
            if not folder_path.exists():
                print(f"⚠️  Dossier ignoré (n'existe pas): {folder}")
                continue
            
            # Lister tous les fichiers image
            image_files = list(folder_path.glob("*.png")) + \
                         list(folder_path.glob("*.jpg")) + \
                         list(folder_path.glob("*.jpeg"))
            
            if not image_files:
                continue
            
            print(f"\n📂 Analyse: {folder} ({len(image_files)} portraits)")
            
            # Analyser chaque image
            removed_in_folder = 0
            for image_path in tqdm(image_files, desc=f"  {folder}"):
                self.scanned_count += 1
                
                # Vérifier l'âge
                result = self.check_age(image_path)
                
                if not result['success']:
                    self.error_count += 1
                    continue
                
                age = result['age']
                
                # Si l'âge est < MIN_AGE, déplacer vers backup
                if age is not None and age < MIN_AGE:
                    self.move_to_backup(image_path, age, folder)
                    removed_in_folder += 1
            
            if removed_in_folder > 0:
                print(f"  ❌ Supprimés: {removed_in_folder} portraits d'enfants")
    
    def generate_report(self):
        """Génère un rapport détaillé"""
        report = {
            'summary': {
                'total_scanned': self.scanned_count,
                'total_removed': len(self.removed_portraits),
                'errors': self.error_count,
                'min_age_threshold': MIN_AGE
            },
            'removed_by_folder': {},
            'removed_portraits': self.removed_portraits
        }
        
        # Compter par dossier
        for portrait in self.removed_portraits:
            folder = portrait['folder']
            if folder not in report['removed_by_folder']:
                report['removed_by_folder'][folder] = {
                    'count': 0,
                    'ages': []
                }
            report['removed_by_folder'][folder]['count'] += 1
            report['removed_by_folder'][folder]['ages'].append(portrait['age'])
        
        # Sauvegarder en JSON
        with open(self.report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        # Afficher le résumé
        print("\n" + "="*60)
        print("📊 RAPPORT DE SUPPRESSION")
        print("="*60)
        print(f"✅ Portraits scannés: {self.scanned_count}")
        print(f"❌ Portraits d'enfants supprimés: {len(self.removed_portraits)}")
        print(f"⚠️  Erreurs d'analyse: {self.error_count}")
        print(f"📝 Âge minimum: {MIN_AGE} ans")
        
        if self.removed_portraits:
            print(f"\n📁 Répartition par dossier:")
            for folder, data in sorted(report['removed_by_folder'].items()):
                avg_age = sum(data['ages']) / len(data['ages'])
                min_age = min(data['ages'])
                max_age = max(data['ages'])
                print(f"  • {folder}: {data['count']} portraits")
                print(f"    └─ Âges: {min_age}-{max_age} ans (moyenne: {avg_age:.1f} ans)")
        
        print(f"\n💾 Backup: {self.backup_dir}")
        print(f"📄 Rapport détaillé: {self.report_file}")
        print("="*60 + "\n")


def main():
    print("\n" + "="*60)
    print("🔞 SUPPRESSION DES PORTRAITS D'ENFANTS")
    print("="*60)
    print(f"Âge minimum autorisé: {MIN_AGE} ans")
    print(f"Les portraits d'enfants seront déplacés vers: {BACKUP_DIR}")
    print("="*60)
    print("\n✅ Démarrage du scan automatique...")
    
    # Créer le remover et lancer le scan
    remover = ChildrenPortraitRemover()
    remover.scan_and_remove()
    remover.generate_report()
    
    print("\n✅ Opération terminée avec succès!")
    
    if remover.removed_portraits:
        print(f"\n⚠️  {len(remover.removed_portraits)} portraits d'enfants ont été supprimés")
        print(f"💾 Les fichiers sont sauvegardés dans: {BACKUP_DIR}")
    else:
        print("\n✅ Aucun portrait d'enfant détecté!")


if __name__ == "__main__":
    main()
