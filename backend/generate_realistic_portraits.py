"""
Script pour télécharger 1200 portraits réalistes par continent depuis thispersonnotexist.org
Total : 7200 portraits (6 continents × 1200 portraits)
Répartition : 600 hommes + 600 femmes par continent
"""
import os
import time
import requests
from pathlib import Path
from typing import Dict, List
import random

class RealisticPortraitDownloader:
    """Télécharge des portraits réalistes depuis thispersonnotexist.org"""
    
    # Mapping continents → ethnicités du site
    CONTINENT_MAPPING = {
        'africa': {
            'name': 'Afrique',
            'race': 'black',
            'ages': ['21-35', '35-50']  # Adultes
        },
        'asia': {
            'name': 'Asie',
            'race': 'asian',
            'ages': ['21-35', '35-50']
        },
        'europe': {
            'name': 'Europe',
            'race': 'white',
            'ages': ['21-35', '35-50']
        },
        'north_america': {
            'name': 'Amérique du Nord',
            'race': ['white', 'latino_hispanic'],  # Mix
            'ages': ['21-35', '35-50']
        },
        'south_america': {
            'name': 'Amérique du Sud',
            'race': 'latino_hispanic',
            'ages': ['21-35', '35-50']
        },
        'oceania': {
            'name': 'Océanie',
            'race': ['white', 'asian'],  # Mix
            'ages': ['21-35', '35-50']
        }
    }
    
    GENDERS = ['male', 'female']
    PORTRAITS_PER_GENDER = 600  # 600 par genre = 1200 par continent
    
    def __init__(self, base_path: str = "/app/backend/static/portraits"):
        self.base_path = Path(base_path)
        self.base_url = "https://thispersonnotexist.org"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
    def create_directory_structure(self):
        """Crée la structure de dossiers pour tous les continents"""
        print("\n📁 Création de la structure de dossiers...")
        
        for continent_id in self.CONTINENT_MAPPING.keys():
            for gender in self.GENDERS:
                dir_path = self.base_path / continent_id / gender
                dir_path.mkdir(parents=True, exist_ok=True)
                print(f"   ✓ {dir_path}")
    
    def get_race_param(self, continent_id: str) -> str:
        """Retourne le paramètre de race pour un continent donné"""
        race = self.CONTINENT_MAPPING[continent_id]['race']
        
        # Si c'est une liste (mix), choisir aléatoirement
        if isinstance(race, list):
            return random.choice(race)
        return race
    
    def download_image(self, url: str, save_path: Path, retries: int = 3) -> bool:
        """Télécharge une image avec gestion des erreurs"""
        for attempt in range(retries):
            try:
                response = self.session.get(url, timeout=30)
                if response.status_code == 200:
                    with open(save_path, 'wb') as f:
                        f.write(response.content)
                    return True
                else:
                    print(f"   ⚠️ Erreur HTTP {response.status_code}, tentative {attempt + 1}/{retries}")
            except Exception as e:
                print(f"   ⚠️ Erreur: {e}, tentative {attempt + 1}/{retries}")
                time.sleep(2)
        
        return False
    
    def fetch_face_from_api(self, race: str, gender: str, age: str) -> str:
        """
        Récupère l'URL d'un visage depuis thispersonnotexist.org
        Note: Cette fonction doit être adaptée selon l'API réelle du site
        """
        # Pour l'instant, on va utiliser une approche de scraping simple
        # Le site génère des images à la volée, on doit analyser comment il fonctionne
        
        # URL de base pour récupérer une image
        # Selon le site, il faut probablement faire une requête AJAX ou POST
        
        try:
            # Tentative de récupération directe
            # (À adapter selon l'API réelle du site)
            params = {
                'race': race,
                'gender': gender,
                'age': age
            }
            
            # Le site utilise probablement une API interne
            # Pour l'instant, on va utiliser l'URL de base et télécharger l'image générée
            response = self.session.get(f"{self.base_url}/", params=params, timeout=30)
            
            if response.status_code == 200:
                # Chercher l'URL de l'image dans la réponse
                # (Cette partie nécessite d'analyser le HTML ou l'API)
                return None
            
        except Exception as e:
            print(f"   ⚠️ Erreur lors de la récupération: {e}")
        
        return None
    
    def download_portraits_for_continent(self, continent_id: str, gender: str):
        """Télécharge tous les portraits pour un continent et un genre"""
        continent_name = self.CONTINENT_MAPPING[continent_id]['name']
        ages = self.CONTINENT_MAPPING[continent_id]['ages']
        
        print(f"\n🌍 {continent_name} - {gender.upper()}")
        print(f"   Objectif: {self.PORTRAITS_PER_GENDER} portraits")
        print(f"   " + "=" * 60)
        
        save_dir = self.base_path / continent_id / gender
        downloaded = 0
        failed = 0
        
        # Compter les images déjà téléchargées
        existing_files = list(save_dir.glob("*.png")) + list(save_dir.glob("*.jpg"))
        if existing_files:
            print(f"   ℹ️ {len(existing_files)} portraits déjà présents, reprise...")
            downloaded = len(existing_files)
        
        while downloaded < self.PORTRAITS_PER_GENDER:
            # Alterner entre les tranches d'âge
            age = random.choice(ages)
            race = self.get_race_param(continent_id)
            
            # Nom de fichier unique
            filename = f"portrait_{downloaded + 1:04d}.png"
            save_path = save_dir / filename
            
            # Si le fichier existe déjà, passer au suivant
            if save_path.exists():
                downloaded += 1
                continue
            
            # **IMPORTANT: Cette URL doit être adaptée selon l'API réelle**
            # Pour l'instant, c'est un placeholder
            image_url = f"{self.base_url}/generate?race={race}&gender={gender}&age={age}"
            
            print(f"   [{downloaded + 1}/{self.PORTRAITS_PER_GENDER}] Téléchargement: {race}, {gender}, {age}...", end='')
            
            if self.download_image(image_url, save_path):
                downloaded += 1
                print(" ✓")
                
                # Délai pour éviter de surcharger le serveur
                time.sleep(1)
            else:
                failed += 1
                print(" ✗")
                
                # Pause plus longue en cas d'échec
                time.sleep(3)
                
                # Arrêter après trop d'échecs consécutifs
                if failed > 10:
                    print(f"\n   ⛔ Trop d'échecs consécutifs. Arrêt temporaire.")
                    print(f"   ℹ️ Progression sauvegardée: {downloaded}/{self.PORTRAITS_PER_GENDER}")
                    return False
        
        print(f"\n   ✅ Terminé: {downloaded} portraits téléchargés")
        return True
    
    def download_all_portraits(self):
        """Télécharge tous les portraits pour tous les continents"""
        print("=" * 80)
        print("🎨 TÉLÉCHARGEMENT DE 7200 PORTRAITS RÉALISTES")
        print("=" * 80)
        print(f"\n📦 Source: {self.base_url}")
        print(f"📁 Destination: {self.base_path}")
        print(f"\n📊 Configuration:")
        print(f"   • Continents: {len(self.CONTINENT_MAPPING)}")
        print(f"   • Portraits par continent: 1200 (600M + 600F)")
        print(f"   • Total: {len(self.CONTINENT_MAPPING) * 1200} portraits")
        
        # Créer la structure de dossiers
        self.create_directory_structure()
        
        start_time = time.time()
        total_downloaded = 0
        
        # Télécharger pour chaque continent et genre
        for continent_id, info in self.CONTINENT_MAPPING.items():
            for gender in self.GENDERS:
                success = self.download_portraits_for_continent(continent_id, gender)
                
                if success:
                    total_downloaded += self.PORTRAITS_PER_GENDER
                else:
                    print(f"\n⚠️ Téléchargement interrompu pour {info['name']} - {gender}")
                    print("   Vous pouvez relancer le script pour continuer.")
                    return
        
        elapsed_time = time.time() - start_time
        
        print("\n" + "=" * 80)
        print("✅ TÉLÉCHARGEMENT TERMINÉ")
        print("=" * 80)
        print(f"📊 Statistiques:")
        print(f"   • Total téléchargé: {total_downloaded} portraits")
        print(f"   • Temps écoulé: {elapsed_time/60:.1f} minutes")
        print(f"   • Emplacement: {self.base_path}")
        print("\n💡 Les portraits sont maintenant disponibles pour votre application !")


def main():
    """Point d'entrée principal"""
    print("\n" + "🚀 " * 20)
    print("AVERTISSEMENT IMPORTANT")
    print("🚀 " * 20)
    print("""
⚠️  Ce script est un TEMPLATE qui doit être adapté.
    
Le site thispersonnotexist.org ne fournit pas d'API publique documentée.
Pour télécharger automatiquement les images, vous devez :

1. Analyser le site web pour comprendre comment il génère les images
2. Identifier les requêtes AJAX/API qui récupèrent les images
3. Adapter la fonction fetch_face_from_api() et download_image()

ALTERNATIVES:
- Utiliser un service avec API documentée (Generated Photos, etc.)
- Télécharger manuellement via l'interface web
- Utiliser un scraper avancé (Selenium, Playwright)

Voulez-vous que je crée une version avec Selenium/Playwright pour
automatiser le téléchargement via le navigateur ?
""")
    
    response = input("\nContinuer avec ce template ? (y/n): ")
    if response.lower() != 'y':
        print("Annulé.")
        return
    
    downloader = RealisticPortraitDownloader()
    downloader.download_all_portraits()


if __name__ == "__main__":
    main()
