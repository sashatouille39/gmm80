"""
Étape 2 : Classification automatique des visages avec DeepFace
Analyse l'ethnicité, le genre et l'âge de chaque image téléchargée
Version optimisée pour gérer la mémoire
"""
import os
import json
import gc
from pathlib import Path
from tqdm import tqdm
from deepface import DeepFace
import cv2

# Limiter l'utilisation mémoire de TensorFlow
os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Réduire les logs


class FaceClassifier:
    """Classifie les visages par ethnicité, genre et âge"""
    
    # Mapping des ethnicités DeepFace vers nos continents
    ETHNICITY_TO_CONTINENT = {
        'asian': 'asia',
        'indian': 'asia',
        'white': 'europe',
        'black': 'africa',
        'latino hispanic': 'south_america',
        'middle eastern': 'europe',  # Réparti entre Europe/Asie
    }
    
    def __init__(self, 
                 temp_dir: str = "/app/backend/static/portraits/temp",
                 results_file: str = "/app/backend/static/portraits/classification_results.json"):
        self.temp_dir = Path(temp_dir)
        self.results_file = Path(results_file)
        self.results = {}
        
        # Charger les résultats existants si disponibles
        if self.results_file.exists():
            with open(self.results_file, 'r') as f:
                self.results = json.load(f)
            print(f"✓ {len(self.results)} classifications déjà effectuées")
    
    def classify_single_image(self, image_path: Path) -> dict:
        """Classifie une seule image"""
        try:
            # Vérifier si l'image existe
            if not image_path.exists():
                return None
            
            # Vérifier si déjà classifiée
            img_name = image_path.name
            if img_name in self.results:
                return self.results[img_name]
            
            # Lire l'image
            img = cv2.imread(str(image_path))
            if img is None:
                return None
            
            # Analyser avec DeepFace
            # actions: age, gender, race, emotion
            analysis = DeepFace.analyze(
                img_path=str(image_path),
                actions=['age', 'gender', 'race'],
                enforce_detection=False,  # Ne pas échouer s'il n'y a pas de visage détecté
                detector_backend='opencv',  # Plus rapide
                silent=True
            )
            
            # DeepFace peut retourner une liste ou un dict
            if isinstance(analysis, list):
                analysis = analysis[0]
            
            # Extraire les informations
            race = analysis.get('dominant_race', 'unknown').lower()
            gender = analysis.get('dominant_gender', 'unknown').lower()
            age = analysis.get('age', 0)
            
            # Mapper vers nos catégories
            continent = self.ETHNICITY_TO_CONTINENT.get(race, 'unknown')
            gender_mapped = 'male' if gender == 'man' else 'female' if gender == 'woman' else 'unknown'
            
            result = {
                'file': img_name,
                'race': race,
                'continent': continent,
                'gender': gender_mapped,
                'age': age,
                'raw_race_scores': analysis.get('race', {}),
                'raw_gender_scores': analysis.get('gender', {})
            }
            
            return result
            
        except Exception as e:
            # En cas d'erreur, retourner unknown
            return {
                'file': image_path.name,
                'race': 'unknown',
                'continent': 'unknown',
                'gender': 'unknown',
                'age': 0,
                'error': str(e)
            }
    
    def classify_all_images(self, batch_size: int = 50):
        """Classifie toutes les images du dossier temporaire par lots"""
        print("=" * 80)
        print("🔍 CLASSIFICATION AUTOMATIQUE DES VISAGES")
        print("=" * 80)
        print(f"\n📁 Dossier source: {self.temp_dir}")
        print(f"📄 Fichier résultats: {self.results_file}")
        print(f"\n⚙️ Traitement par lots de {batch_size} images")
        print("\n⏰ Cette étape peut prendre 1-2 heures...")
        print("=" * 80 + "\n")
        
        # Lister toutes les images
        image_files = sorted(self.temp_dir.glob("temp_*.jpg"))
        total_images = len(image_files)
        
        if total_images == 0:
            print("❌ Aucune image trouvée. Exécutez d'abord download_random_faces.py")
            return
        
        print(f"📊 {total_images} images à classifier\n")
        
        # Classifier avec barre de progression
        classified = 0
        failed = 0
        
        with tqdm(total=total_images, desc="Classification") as pbar:
            for img_path in image_files:
                result = self.classify_single_image(img_path)
                
                if result:
                    self.results[result['file']] = result
                    classified += 1
                else:
                    failed += 1
                
                pbar.update(1)
                pbar.set_postfix({
                    'OK': classified,
                    'Échec': failed
                })
                
                # Sauvegarder et nettoyer la mémoire tous les batch_size images
                if classified % batch_size == 0:
                    self.save_results()
                    gc.collect()  # Forcer le garbage collector
        
        # Sauvegarder les résultats finaux
        self.save_results()
        
        # Afficher les statistiques
        self.print_statistics()
    
    def save_results(self):
        """Sauvegarde les résultats dans un fichier JSON"""
        with open(self.results_file, 'w') as f:
            json.dump(self.results, f, indent=2)
    
    def print_statistics(self):
        """Affiche les statistiques de classification"""
        print("\n" + "=" * 80)
        print("✅ CLASSIFICATION TERMINÉE")
        print("=" * 80)
        
        # Compter par continent
        continent_counts = {}
        gender_counts = {}
        continent_gender_counts = {}
        
        for result in self.results.values():
            continent = result.get('continent', 'unknown')
            gender = result.get('gender', 'unknown')
            
            # Compter continents
            continent_counts[continent] = continent_counts.get(continent, 0) + 1
            
            # Compter genres
            gender_counts[gender] = gender_counts.get(gender, 0) + 1
            
            # Compter continent + genre
            key = f"{continent}_{gender}"
            continent_gender_counts[key] = continent_gender_counts.get(key, 0) + 1
        
        print("\n📊 STATISTIQUES PAR CONTINENT:")
        print("-" * 80)
        for continent in ['africa', 'asia', 'europe', 'south_america']:
            count = continent_counts.get(continent, 0)
            male = continent_gender_counts.get(f"{continent}_male", 0)
            female = continent_gender_counts.get(f"{continent}_female", 0)
            print(f"   {continent.upper():15} : {count:4} total ({male:4} M, {female:4} F)")
        
        unknown = continent_counts.get('unknown', 0)
        print(f"\n   {'UNKNOWN':15} : {unknown:4} (à réassigner)")
        
        print("\n📊 STATISTIQUES PAR GENRE:")
        print("-" * 80)
        for gender, count in gender_counts.items():
            print(f"   {gender.upper():15} : {count:4}")
        
        print("\n💡 Passez à l'étape suivante : réorganisation des images")
        print("   Commande: python reorganize_faces.py")


def main():
    """Point d'entrée principal"""
    print("\n🔍 Démarrage de la classification...")
    print("\n⚠️ Première exécution : téléchargement des modèles DeepFace (~500MB)")
    print("   Les exécutions suivantes seront plus rapides.\n")
    
    classifier = FaceClassifier()
    classifier.classify_all_images()


if __name__ == "__main__":
    main()
