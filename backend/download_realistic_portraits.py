#!/usr/bin/env python3
"""
Script d'automatisation pour télécharger 1200 portraits semi-réalistes PAR continent
depuis thispersonnotexist.org

Organisation :
- 1200 portraits par continent
- 50/50 hommes/femmes (600 + 600)
- Ages : 21-35 et 35-50 (pas d'enfants)
- Émotion : Neutre
- Par ethnies selon les continents

Continents et ethnies :
1. Afrique (1200) : Black
2. Asie (1200) : Asian (700), Indian (500)  
3. Europe (1200) : White
4. Amérique (1200) : Latino Hispanic (700), White (500)
5. Moyen-Orient (1200) : Middle Eastern
6. Océanie (1200) : White avec variations

Total : 7200 portraits
"""

import asyncio
import os
import time
from pathlib import Path
from playwright.async_api import async_playwright
import random

# Configuration
BASE_DIR = Path("/app/backend/static/realistic_portraits")
PORTRAITS_PER_CONTINENT = 1200
PORTRAITS_PER_GENDER = 600  # 50/50

# Mapping continent -> ethnies
CONTINENT_CONFIG = {
    "africa": {
        "ethnicities": [
            {"name": "black", "count": 1200}
        ]
    },
    "asia": {
        "ethnicities": [
            {"name": "asian", "count": 700},
            {"name": "indian", "count": 500}
        ]
    },
    "europe": {
        "ethnicities": [
            {"name": "white", "count": 1200}
        ]
    },
    "america": {
        "ethnicities": [
            {"name": "latino hispanic", "count": 700},
            {"name": "white", "count": 500}
        ]
    },
    "middle_east": {
        "ethnicities": [
            {"name": "middle eastern", "count": 1200}
        ]
    },
    "oceania": {
        "ethnicities": [
            {"name": "white", "count": 1200}
        ]
    }
}

# Ages disponibles (sans enfants)
AGES = ["21-35", "34-50"]
EMOTION = "neutral"
GENDERS = ["M", "F"]

class RealisticPortraitDownloader:
    def __init__(self):
        self.base_dir = BASE_DIR
        self.total_downloaded = 0
        self.errors = []
        
    async def setup_browser(self):
        """Initialise le navigateur Playwright"""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-setuid-sandbox']
        )
        self.context = await self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        
    async def close_browser(self):
        """Ferme le navigateur"""
        await self.context.close()
        await self.browser.close()
        await self.playwright.stop()
        
    def create_directory_structure(self):
        """Crée la structure de dossiers"""
        for continent in CONTINENT_CONFIG.keys():
            for ethnicity_config in CONTINENT_CONFIG[continent]["ethnicities"]:
                ethnicity = ethnicity_config["name"].replace(" ", "_")
                for gender in GENDERS:
                    dir_path = self.base_dir / continent / ethnicity / gender
                    dir_path.mkdir(parents=True, exist_ok=True)
                    print(f"✅ Dossier créé : {dir_path}")
                    
    async def download_portrait(self, page, continent, ethnicity, gender, age, index):
        """Télécharge un portrait avec les paramètres spécifiés"""
        try:
            # Aller sur le site
            await page.goto('https://thispersonnotexist.org/', wait_until='networkidle', timeout=30000)
            await asyncio.sleep(2)
            
            # Sélectionner le genre
            if gender == "M":
                await page.click('input#tabthree')  # Male
            else:
                await page.click('input#tabtwo')  # Female
            await asyncio.sleep(1)
            
            # Sélectionner l'ethnie
            await page.select_option('select#xrace', ethnicity)
            await asyncio.sleep(1)
            
            # Sélectionner l'âge
            await page.select_option('select#xage', age)
            await asyncio.sleep(1)
            
            # Sélectionner l'émotion neutre
            await page.select_option('select#xemotion', EMOTION)
            await asyncio.sleep(1)
            
            # Cliquer sur le bouton reload pour générer
            await page.click('label.reloadbtnx')
            await asyncio.sleep(5)  # Attendre la génération
            
            # Attendre que l'image soit chargée
            await page.wait_for_selector('img[src^="https://"]', timeout=15000)
            
            # Trouver l'image générée (première image dans le conteneur)
            image_element = await page.query_selector('img[src^="https://thispersonnotexist.org/image"]')
            
            if not image_element:
                # Essayer d'autres sélecteurs
                image_element = await page.query_selector('img[alt*="face"]')
            
            if image_element:
                image_url = await image_element.get_attribute('src')
                
                # Télécharger l'image
                ethnicity_clean = ethnicity.replace(" ", "_")
                filename = f"{continent}_{ethnicity_clean}_{gender}_{age.replace('-', '_')}_{index:04d}.png"
                file_path = self.base_dir / continent / ethnicity_clean / gender / filename
                
                # Télécharger via le contexte
                async with self.context.expect_download() as download_info:
                    await page.evaluate(f'() => {{ window.location.href = "{image_url}"; }}')
                    
                download = await download_info.value
                await download.save_as(file_path)
                
                self.total_downloaded += 1
                print(f"✅ [{self.total_downloaded}/7200] Téléchargé : {filename}")
                return True
            else:
                raise Exception("Image non trouvée sur la page")
                
        except Exception as e:
            error_msg = f"❌ Erreur pour {continent}/{ethnicity}/{gender}/{age}_{index}: {str(e)}"
            print(error_msg)
            self.errors.append(error_msg)
            return False
            
    async def download_continent(self, continent, config):
        """Télécharge tous les portraits d'un continent"""
        print(f"\n🌍 === CONTINENT : {continent.upper()} ===\n")
        
        page = await self.context.new_page()
        
        for ethnicity_config in config["ethnicities"]:
            ethnicity = ethnicity_config["name"]
            total_count = ethnicity_config["count"]
            per_gender = total_count // 2  # 50/50
            
            print(f"\n👥 Ethnie : {ethnicity} ({total_count} portraits)")
            
            for gender in GENDERS:
                gender_name = "Hommes" if gender == "M" else "Femmes"
                print(f"\n  🚻 {gender_name} ({per_gender} portraits)")
                
                portraits_per_age = per_gender // len(AGES)
                remainder = per_gender % len(AGES)
                
                for age_idx, age in enumerate(AGES):
                    count = portraits_per_age + (1 if age_idx < remainder else 0)
                    print(f"    📅 Âge {age} : {count} portraits")
                    
                    for i in range(count):
                        success = await self.download_portrait(
                            page, continent, ethnicity, gender, age, i + 1
                        )
                        
                        if success:
                            # Pause entre téléchargements pour éviter le rate limiting
                            await asyncio.sleep(random.uniform(2, 4))
                        else:
                            # Pause plus longue en cas d'erreur
                            await asyncio.sleep(5)
                            
        await page.close()
        
    async def run(self):
        """Lance le téléchargement complet"""
        print("🚀 Début du téléchargement des portraits réalistes")
        print(f"📊 Objectif : 7200 portraits (1200 par continent)")
        print(f"📁 Destination : {self.base_dir}\n")
        
        # Créer la structure de dossiers
        self.create_directory_structure()
        
        # Initialiser le navigateur
        await self.setup_browser()
        
        start_time = time.time()
        
        try:
            # Télécharger continent par continent
            for continent, config in CONTINENT_CONFIG.items():
                await self.download_continent(continent, config)
                
        except KeyboardInterrupt:
            print("\n⚠️ Interruption par l'utilisateur")
        except Exception as e:
            print(f"\n❌ Erreur fatale : {str(e)}")
        finally:
            # Fermer le navigateur
            await self.close_browser()
            
        # Rapport final
        elapsed = time.time() - start_time
        print("\n" + "="*60)
        print("📊 RAPPORT FINAL")
        print("="*60)
        print(f"✅ Portraits téléchargés : {self.total_downloaded}/7200")
        print(f"⏱️  Temps écoulé : {elapsed/60:.1f} minutes")
        print(f"⚠️  Erreurs : {len(self.errors)}")
        
        if self.errors:
            print("\n❌ Liste des erreurs :")
            for error in self.errors[:10]:  # Afficher les 10 premières
                print(f"  - {error}")
                
        print("\n✅ Téléchargement terminé !")
        
if __name__ == "__main__":
    downloader = RealisticPortraitDownloader()
    asyncio.run(downloader.run())
