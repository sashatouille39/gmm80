#!/usr/bin/env python3
"""
Script pour supprimer les portraits identifiés comme étant des enfants
"""
import os
from pathlib import Path
import shutil
from datetime import datetime

# Dossier des portraits
PORTRAITS_DIR = Path("/app/backend/static/realistic_portraits")
BACKUP_DIR = Path("/app/backend/static/portraits_backup_children")

# Liste des portraits à supprimer (ajoutez les chemins relatifs ici)
PORTRAITS_TO_REMOVE = [
    "europe/white/F/europe_white_F_34_50_0060.jpg",
]

def create_backup():
    """Crée un dossier de sauvegarde avec timestamp"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_folder = BACKUP_DIR / timestamp
    backup_folder.mkdir(parents=True, exist_ok=True)
    return backup_folder

def remove_portraits(portraits_list):
    """Supprime les portraits de la liste"""
    
    print("=" * 60)
    print("🗑️  SUPPRESSION DES PORTRAITS D'ENFANTS")
    print("=" * 60)
    
    backup_folder = create_backup()
    print(f"📦 Dossier de sauvegarde: {backup_folder}")
    
    removed_count = 0
    not_found = []
    
    for portrait_path in portraits_list:
        full_path = PORTRAITS_DIR / portrait_path
        
        if not full_path.exists():
            not_found.append(portrait_path)
            print(f"⚠️  Non trouvé: {portrait_path}")
            continue
        
        try:
            # Copier dans le backup
            backup_path = backup_folder / portrait_path
            backup_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(full_path, backup_path)
            
            # Supprimer l'original
            full_path.unlink()
            removed_count += 1
            print(f"✅ Supprimé: {portrait_path}")
            
        except Exception as e:
            print(f"❌ Erreur lors de la suppression de {portrait_path}: {e}")
    
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ")
    print("=" * 60)
    print(f"✅ Portraits supprimés: {removed_count}")
    if not_found:
        print(f"⚠️  Non trouvés: {len(not_found)}")
    print(f"📁 Sauvegarde: {backup_folder}")
    
    return removed_count

def scan_for_similar_patterns():
    """Scanner pour trouver des patterns similaires"""
    print("\n🔍 Recherche de patterns similaires...")
    
    # Chercher d'autres fichiers avec des numéros bas (qui pourraient être problématiques)
    suspicious = []
    
    for continent in PORTRAITS_DIR.iterdir():
        if not continent.is_dir():
            continue
        
        for ethnicity in continent.iterdir():
            if not ethnicity.is_dir():
                continue
            
            for gender in ethnicity.iterdir():
                if not gender.is_dir():
                    continue
                
                # Lister les fichiers
                portraits = sorted(gender.glob("*.jpg"))
                
                # Vérifier les 50 premiers de chaque catégorie (souvent générés en premier et peuvent avoir des problèmes)
                for portrait in portraits[:50]:
                    filename = portrait.name
                    # Extraire le numéro
                    try:
                        number = int(filename.split('_')[-1].replace('.jpg', ''))
                        if number <= 100:  # Numéros bas potentiellement problématiques
                            suspicious.append(portrait.relative_to(PORTRAITS_DIR))
                    except:
                        pass
    
    print(f"⚠️  {len(suspicious)} portraits avec numéros bas trouvés (potentiellement à vérifier)")
    
    return suspicious

if __name__ == "__main__":
    # Supprimer les portraits identifiés
    removed = remove_portraits(PORTRAITS_TO_REMOVE)
    
    # Scanner pour patterns similaires
    print("\n" + "=" * 60)
    suspicious = scan_for_similar_patterns()
    
    if suspicious:
        print("\n💡 SUGGESTION:")
        print("   Des portraits avec numéros bas ont été détectés.")
        print("   Ils peuvent nécessiter une vérification manuelle.")
        print(f"   Exemples (10 premiers):")
        for s in suspicious[:10]:
            print(f"   • {s}")
    
    print("\n✅ Terminé!")
