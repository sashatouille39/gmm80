"""
Étape 3 : Réorganisation automatique des images classifiées
Déplace les images dans les bons dossiers par continent et genre
Objectif : 600 hommes + 600 femmes par continent (1200 par continent)
"""
import os
import json
import shutil
from pathlib import Path
from collections import defaultdict


class FaceReorganizer:
    """Réorganise les images classifiées dans les dossiers finaux"""
    
    CONTINENTS = ['africa', 'asia', 'europe', 'south_america', 'north_america', 'oceania']
    GENDERS = ['male', 'female']
    TARGET_PER_GENDER = 600  # 600 par genre = 1200 par continent
    
    def __init__(self,
                 temp_dir: str = "/app/backend/static/portraits/temp",
                 final_dir: str = "/app/backend/static/portraits",
                 results_file: str = "/app/backend/static/portraits/classification_results.json"):
        self.temp_dir = Path(temp_dir)
        self.final_dir = Path(final_dir)
        self.results_file = Path(results_file)
        self.results = {}
        
        # Charger les résultats de classification
        if not self.results_file.exists():
            print("❌ Fichier de classification non trouvé!")
            print("   Exécutez d'abord classify_faces.py")
            return
        
        with open(self.results_file, 'r') as f:
            self.results = json.load(f)
        
        print(f"✓ {len(self.results)} classifications chargées")
    
    def create_directory_structure(self):
        """Crée la structure de dossiers pour tous les continents"""
        print("\n📁 Création de la structure de dossiers...")
        
        for continent in self.CONTINENTS:
            for gender in self.GENDERS:
                dir_path = self.final_dir / continent / gender
                dir_path.mkdir(parents=True, exist_ok=True)
    
    def organize_images_by_category(self):
        """Organise les images par catégorie (continent + genre)"""
        categories = defaultdict(list)
        
        for filename, data in self.results.items():
            continent = data.get('continent', 'unknown')
            gender = data.get('gender', 'unknown')
            
            # Ignorer les unknown
            if continent == 'unknown' or gender == 'unknown':
                continue
            
            # Ajouter à la catégorie appropriée
            if continent in ['africa', 'asia', 'europe', 'south_america']:
                key = f"{continent}_{gender}"
                categories[key].append(filename)
        
        return categories
    
    def distribute_for_mixed_continents(self, categories: dict):
        """
        Distribue les images pour les continents mixtes (North America, Oceania)
        North America: mélange de White et Latino
        Oceania: mélange de White et Asian
        """
        print("\n🌍 Distribution pour les continents mixtes...")
        
        # North America : 50% White, 50% Latino Hispanic
        for gender in self.GENDERS:
            europe_key = f"europe_{gender}"
            south_america_key = f"south_america_{gender}"
            north_america_key = f"north_america_{gender}"
            
            # Prendre des images de europe et south_america
            available_europe = categories.get(europe_key, [])
            available_south_america = categories.get(south_america_key, [])
            
            # Prendre 300 de chaque (si disponible)
            north_america_images = []
            
            if len(available_europe) > 300:
                north_america_images.extend(available_europe[:300])
                categories[europe_key] = available_europe[300:]
            
            if len(available_south_america) > 300:
                north_america_images.extend(available_south_america[:300])
                categories[south_america_key] = available_south_america[300:]
            
            categories[north_america_key] = north_america_images
            print(f"   {north_america_key}: {len(north_america_images)} images")
        
        # Oceania : 50% White, 50% Asian
        for gender in self.GENDERS:
            europe_key = f"europe_{gender}"
            asia_key = f"asia_{gender}"
            oceania_key = f"oceania_{gender}"
            
            available_europe = categories.get(europe_key, [])
            available_asia = categories.get(asia_key, [])
            
            oceania_images = []
            
            if len(available_europe) > 300:
                oceania_images.extend(available_europe[:300])
                categories[europe_key] = available_europe[300:]
            
            if len(available_asia) > 300:
                oceania_images.extend(available_asia[:300])
                categories[asia_key] = available_asia[300:]
            
            categories[oceania_key] = oceania_images
            print(f"   {oceania_key}: {len(oceania_images)} images")
        
        return categories
    
    def copy_images_to_final_folders(self, categories: dict):
        """Copie les images dans les dossiers finaux"""
        print("\n📦 Copie des images dans les dossiers finaux...")
        
        stats = {}
        
        for continent in self.CONTINENTS:
            for gender in self.GENDERS:
                key = f"{continent}_{gender}"
                images = categories.get(key, [])
                
                # Limiter à 600 images par catégorie
                images_to_copy = images[:self.TARGET_PER_GENDER]
                
                dest_dir = self.final_dir / continent / gender
                
                copied = 0
                for i, filename in enumerate(images_to_copy):
                    src = self.temp_dir / filename
                    dest = dest_dir / f"portrait_{i+1:04d}.jpg"
                    
                    if src.exists():
                        shutil.copy2(src, dest)
                        copied += 1
                
                stats[key] = copied
                print(f"   {key:25} : {copied:4} / {self.TARGET_PER_GENDER} images")
        
        return stats
    
    def reorganize_all(self):
        """Réorganise toutes les images"""
        print("=" * 80)
        print("📂 RÉORGANISATION DES IMAGES")
        print("=" * 80)
        print(f"\n📁 Source: {self.temp_dir}")
        print(f"📁 Destination: {self.final_dir}")
        print(f"🎯 Objectif: 600 images par genre et continent")
        print("=" * 80)
        
        if not self.results:
            return
        
        # Créer la structure
        self.create_directory_structure()
        
        # Organiser par catégorie
        print("\n🔄 Organisation des images par catégorie...")
        categories = self.organize_images_by_category()
        
        # Afficher les disponibilités
        print("\n📊 Images disponibles par catégorie:")
        for key in sorted(categories.keys()):
            print(f"   {key:25} : {len(categories[key]):4} images")
        
        # Distribuer pour les continents mixtes
        categories = self.distribute_for_mixed_continents(categories)
        
        # Copier les images
        stats = self.copy_images_to_final_folders(categories)
        
        # Statistiques finales
        self.print_final_statistics(stats)
    
    def print_final_statistics(self, stats: dict):
        """Affiche les statistiques finales"""
        print("\n" + "=" * 80)
        print("✅ RÉORGANISATION TERMINÉE")
        print("=" * 80)
        
        print("\n📊 RÉSUMÉ PAR CONTINENT:")
        print("-" * 80)
        
        total_images = 0
        for continent in self.CONTINENTS:
            male_key = f"{continent}_male"
            female_key = f"{continent}_female"
            
            male_count = stats.get(male_key, 0)
            female_count = stats.get(female_key, 0)
            total = male_count + female_count
            
            total_images += total
            
            status = "✅" if total >= 1200 else "⚠️"
            print(f"   {status} {continent.upper():15} : {total:4} / 1200 ({male_count:4} M, {female_count:4} F)")
        
        print("\n" + "-" * 80)
        print(f"   📊 TOTAL : {total_images} images")
        
        if total_images < 7200:
            missing = 7200 - total_images
            print(f"\n⚠️ {missing} images manquantes")
            print("   💡 Solution : Téléchargez plus d'images et relancez le pipeline")
            print("      Ou ajustez les catégories manuellement")
        else:
            print("\n🎉 Objectif de 7200 images atteint !")
        
        print(f"\n📁 Les portraits sont disponibles dans: {self.final_dir}")
        print("   Organisés par continent et genre")
        print("\n💡 Vous pouvez maintenant utiliser ces portraits dans votre application !")


def main():
    """Point d'entrée principal"""
    print("\n📂 Démarrage de la réorganisation...\n")
    
    reorganizer = FaceReorganizer()
    reorganizer.reorganize_all()


if __name__ == "__main__":
    main()
