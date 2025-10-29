"""
Script automatisé pour télécharger 7200 portraits réalistes depuis thispersonnotexist.org
Utilise Playwright pour automatiser le navigateur et télécharger les images
"""
import os
import asyncio
import time
from pathlib import Path
from typing import Dict, List
import random
from playwright.async_api import async_playwright, Page

class AutomatedPortraitDownloader:
    """Télécharge automatiquement des portraits via Playwright"""
    
    # Mapping continents → ethnicités
    CONTINENT_MAPPING = {
        'africa': {
            'name': 'Afrique',
            'race': 'Black',
            'ages': ['21-35', '35-50']
        },
        'asia': {
            'name': 'Asie',
            'race': 'Asian',
            'ages': ['21-35', '35-50']
        },
        'europe': {
            'name': 'Europe',
            'race': 'White',
            'ages': ['21-35', '35-50']
        },
        'north_america': {
            'name': 'Amérique du Nord',
            'race': ['White', 'Latino Hispanic'],  # Mix
            'ages': ['21-35', '35-50']
        },
        'south_america': {
            'name': 'Amérique du Sud',
            'race': 'Latino Hispanic',
            'ages': ['21-35', '35-50']
        },
        'oceania': {
            'name': 'Océanie',
            'race': ['White', 'Asian'],  # Mix
            'ages': ['21-35', '35-50']
        }
    }
    
    GENDERS = ['Male', 'Female']
    PORTRAITS_PER_GENDER = 600
    
    def __init__(self, base_path: str = "/app/backend/static/portraits"):
        self.base_path = Path(base_path)
        self.base_url = "https://thispersonnotexist.org"
        
    def create_directory_structure(self):
        """Crée la structure de dossiers"""
        print("\n📁 Création de la structure de dossiers...")
        
        for continent_id in self.CONTINENT_MAPPING.keys():
            for gender in ['male', 'female']:
                dir_path = self.base_path / continent_id / gender
                dir_path.mkdir(parents=True, exist_ok=True)
                print(f"   ✓ {dir_path}")
    
    def get_race(self, continent_id: str) -> str:
        """Retourne la race pour un continent"""
        race = self.CONTINENT_MAPPING[continent_id]['race']
        if isinstance(race, list):
            return random.choice(race)
        return race
    
    async def download_single_image(self, page: Page, race: str, gender: str, age: str, save_path: Path) -> bool:
        """Télécharge une seule image via Playwright"""
        try:
            # Aller sur la page principale
            await page.goto(self.base_url, wait_until='networkidle')
            await page.wait_for_timeout(2000)
            
            # Sélectionner la race
            print(f"      Sélection race: {race}...", end='')
            race_selector = f"button:has-text('{race}')"
            await page.click(race_selector)
            await page.wait_for_timeout(1000)
            print(" ✓")
            
            # Sélectionner l'âge
            print(f"      Sélection âge: {age}...", end='')
            age_selector = f"button:has-text('{age}')"
            await page.click(age_selector)
            await page.wait_for_timeout(1000)
            print(" ✓")
            
            # Sélectionner le genre
            print(f"      Sélection genre: {gender}...", end='')
            if gender == 'Female':
                await page.click("button:has-text('Female')")
            else:
                await page.click("button:has-text('Male')")
            await page.wait_for_timeout(2000)
            print(" ✓")
            
            # Attendre que l'image soit générée
            print("      Génération de l'image...", end='')
            await page.wait_for_selector('img[alt]', timeout=30000)
            await page.wait_for_timeout(3000)
            print(" ✓")
            
            # Trouver l'image générée
            images = await page.query_selector_all('img')
            target_image = None
            
            for img in images:
                src = await img.get_attribute('src')
                if src and 'data:image' in src or (src and 'thispersonnotexist' in src):
                    target_image = img
                    break
            
            if not target_image:
                print(" ✗ (Image non trouvée)")
                return False
            
            # Télécharger l'image
            print("      Téléchargement...", end='')
            screenshot = await target_image.screenshot()
            
            with open(save_path, 'wb') as f:
                f.write(screenshot)
            
            print(f" ✓ ({len(screenshot)} bytes)")
            return True
            
        except Exception as e:
            print(f" ✗ Erreur: {str(e)[:50]}")
            return False
    
    async def download_portraits_for_continent(self, page: Page, continent_id: str, gender_label: str):
        """Télécharge tous les portraits pour un continent et un genre"""
        continent_name = self.CONTINENT_MAPPING[continent_id]['name']
        ages = self.CONTINENT_MAPPING[continent_id]['ages']
        gender_dir = gender_label.lower()
        
        print(f"\n🌍 {continent_name} - {gender_label.upper()}")
        print(f"   Objectif: {self.PORTRAITS_PER_GENDER} portraits")
        print(f"   " + "=" * 70)
        
        save_dir = self.base_path / continent_id / gender_dir
        
        # Compter les images existantes
        existing_files = list(save_dir.glob("*.png"))
        downloaded = len(existing_files)
        
        if downloaded > 0:
            print(f"   ℹ️ {downloaded} portraits déjà présents, reprise...")
        
        consecutive_failures = 0
        max_consecutive_failures = 5
        
        while downloaded < self.PORTRAITS_PER_GENDER:
            # Alterner les tranches d'âge
            age = random.choice(ages)
            race = self.get_race(continent_id)
            
            # Nom de fichier
            filename = f"portrait_{downloaded + 1:04d}.png"
            save_path = save_dir / filename
            
            if save_path.exists():
                downloaded += 1
                continue
            
            print(f"\n   [{downloaded + 1}/{self.PORTRAITS_PER_GENDER}] {race}, {gender_label}, {age}")
            
            success = await self.download_single_image(page, race, gender_label, age, save_path)
            
            if success:
                downloaded += 1
                consecutive_failures = 0
                
                # Vérifier la taille du fichier
                if save_path.stat().st_size < 1000:
                    print(f"      ⚠️ Fichier trop petit, suppression...")
                    save_path.unlink()
                    downloaded -= 1
                
                # Petit délai entre les téléchargements
                await asyncio.sleep(2)
            else:
                consecutive_failures += 1
                print(f"      ⚠️ Échec ({consecutive_failures}/{max_consecutive_failures})")
                
                if consecutive_failures >= max_consecutive_failures:
                    print(f"\n   ⛔ Trop d'échecs consécutifs. Pause de 30 secondes...")
                    await asyncio.sleep(30)
                    consecutive_failures = 0
                else:
                    await asyncio.sleep(5)
        
        print(f"\n   ✅ Terminé: {downloaded}/{self.PORTRAITS_PER_GENDER} portraits")
    
    async def download_all_portraits(self):
        """Télécharge tous les portraits"""
        print("=" * 80)
        print("🎨 TÉLÉCHARGEMENT AUTOMATISÉ DE 7200 PORTRAITS")
        print("=" * 80)
        print(f"\n📦 Source: {self.base_url}")
        print(f"📁 Destination: {self.base_path}")
        print(f"\n📊 Configuration:")
        print(f"   • Continents: {len(self.CONTINENT_MAPPING)}")
        print(f"   • Portraits par continent: 1200 (600M + 600F)")
        print(f"   • Total: 7200 portraits")
        
        self.create_directory_structure()
        
        start_time = time.time()
        
        async with async_playwright() as p:
            # Lancer le navigateur
            print("\n🌐 Lancement du navigateur Chromium...")
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            )
            page = await context.new_page()
            
            try:
                # Télécharger pour chaque continent et genre
                for continent_id, info in self.CONTINENT_MAPPING.items():
                    for gender in self.GENDERS:
                        await self.download_portraits_for_continent(page, continent_id, gender)
                        
                        # Petite pause entre les continents
                        print(f"\n   ⏸️ Pause de 10 secondes...")
                        await asyncio.sleep(10)
                
            finally:
                await browser.close()
        
        elapsed_time = time.time() - start_time
        
        # Compter les fichiers téléchargés
        total_files = 0
        for continent_id in self.CONTINENT_MAPPING.keys():
            for gender in ['male', 'female']:
                dir_path = self.base_path / continent_id / gender
                total_files += len(list(dir_path.glob("*.png")))
        
        print("\n" + "=" * 80)
        print("✅ TÉLÉCHARGEMENT TERMINÉ")
        print("=" * 80)
        print(f"📊 Statistiques:")
        print(f"   • Total téléchargé: {total_files} portraits")
        print(f"   • Temps écoulé: {elapsed_time/60:.1f} minutes")
        print(f"   • Temps moyen par image: {elapsed_time/total_files:.1f}s")
        print(f"   • Emplacement: {self.base_path}")
        print("\n💡 Les portraits sont maintenant disponibles pour votre application !")


async def main():
    """Point d'entrée principal"""
    print("\n🚀 Démarrage du téléchargement automatisé...")
    print("\n⏰ Ce processus peut prendre plusieurs heures (environ 4-6h)")
    print("   Vous pouvez l'arrêter à tout moment (Ctrl+C)")
    print("   et le relancer : il reprendra là où il s'est arrêté.\n")
    
    response = input("Voulez-vous continuer ? (y/n): ")
    if response.lower() != 'y':
        print("Annulé.")
        return
    
    downloader = AutomatedPortraitDownloader()
    await downloader.download_all_portraits()


if __name__ == "__main__":
    asyncio.run(main())
