#!/usr/bin/env python3
"""
Script optimisé pour télécharger 1200 portraits PAR continent depuis thispersonnotexist.org
Le site génère 8 portraits à la fois, ce qui est parfait pour accélérer le processus.
"""

import asyncio
import os
import time
from pathlib import Path
from playwright.async_api import async_playwright
import random
import json
from datetime import datetime

# Configuration
BASE_DIR = Path("/app/backend/static/realistic_portraits")
PORTRAITS_PER_BATCH = 8  # Le site génère 8 images à la fois
DELAY_BETWEEN_BATCHES = random.uniform(3, 5)  # Secondes

# Mapping continent -> ethnies (1200 portraits par continent)
CONTINENT_CONFIG = {
    "africa": {
        "ethnicities": [
            {"name": "black", "male": 600, "female": 600}
        ]
    },
    "asia": {
        "ethnicities": [
            {"name": "asian", "male": 350, "female": 350},
            {"name": "indian", "male": 250, "female": 250}
        ]
    },
    "europe": {
        "ethnicities": [
            {"name": "white", "male": 600, "female": 600}
        ]
    },
    "america": {
        "ethnicities": [
            {"name": "latino hispanic", "male": 350, "female": 350},
            {"name": "white", "male": 250, "female": 250}
        ]
    },
    "middle_east": {
        "ethnicities": [
            {"name": "middle eastern", "male": 600, "female": 600}
        ]
    },
    "oceania": {
        "ethnicities": [
            {"name": "white", "male": 600, "female": 600}
        ]
    }
}

# Ages disponibles (sans enfants)
AGES = ["21-35", "34-50"]
EMOTION = "neutral"

class OptimizedPortraitDownloader:
    def __init__(self):
        self.base_dir = BASE_DIR
        self.total_downloaded = 0
        self.errors = []
        self.progress_file = Path("/tmp/portrait_download_progress.json")
        self.progress = self.load_progress()
        
    def load_progress(self):
        """Charge la progression sauvegardée"""
        if self.progress_file.exists():
            with open(self.progress_file, 'r') as f:
                return json.load(f)
        return {}
        
    def save_progress(self):
        """Sauvegarde la progression"""
        with open(self.progress_file, 'w') as f:
            json.dump(self.progress, f, indent=2)
            
    async def setup_browser(self):
        """Initialise le navigateur Playwright"""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
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
                for gender in ["M", "F"]:
                    dir_path = self.base_dir / continent / ethnicity / gender
                    dir_path.mkdir(parents=True, exist_ok=True)
                    
    def get_progress_key(self, continent, ethnicity, gender, age):
        """Génère une clé unique pour suivre la progression"""
        return f"{continent}_{ethnicity}_{gender}_{age}".replace(" ", "_")
        
    def count_existing_files(self, continent, ethnicity, gender, age):
        """Compte les fichiers déjà téléchargés"""
        ethnicity_clean = ethnicity.replace(" ", "_")
        dir_path = self.base_dir / continent / ethnicity_clean / gender
        if not dir_path.exists():
            return 0
        age_pattern = age.replace('-', '_')
        existing = list(dir_path.glob(f"{continent}_{ethnicity_clean}_{gender}_{age_pattern}_*.jpg"))
        return len(existing)
    
    async def download_batch(self, page, continent, ethnicity, gender, age, batch_num, batch_size, start_num):
        """Télécharge un lot de 8 portraits"""
        ethnicity_clean = ethnicity.replace(" ", "_")
        progress_key = self.get_progress_key(continent, ethnicity, gender, age)
        
        try:
            # Naviguer vers le site
            await page.goto('https://thispersonnotexist.org/', wait_until='networkidle', timeout=30000)
            await asyncio.sleep(3)
            
            # Sélectionner le genre
            if gender == "M":
                await page.click('label[for="tabthree"]', force=True)
            else:
                await page.click('label[for="tabtwo"]', force=True)
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
            
            # Cliquer sur reload pour générer 8 images
            await page.click('label.reloadbtnx', force=True)
            await asyncio.sleep(8)  # Attendre la génération
            
            # Récupérer toutes les images générées
            images = await page.query_selector_all('img[alt*="Person Face"][alt*="That Not Exist"]')
            
            if len(images) == 0:
                print(f"⚠️  Aucune image trouvée pour {continent}/{ethnicity}/{gender}/{age}")
                return 0
                
            downloaded_count = 0
            for idx, img in enumerate(images[:batch_size]):  # Maximum batch_size images
                try:
                    src = await img.get_attribute('src')
                    if not src or src == '#':
                        continue
                        
                    # Télécharger l'image
                    image_num = start_num + idx + 1
                    filename = f"{continent}_{ethnicity_clean}_{gender}_{age.replace('-', '_')}_{image_num:04d}.jpg"
                    file_path = self.base_dir / continent / ethnicity_clean / gender / filename
                    
                    # Utiliser l'API Request de Playwright
                    response = await self.context.request.get(src)
                    if response.ok:
                        content = await response.body()
                        with open(file_path, 'wb') as f:
                            f.write(content)
                        downloaded_count += 1
                        self.total_downloaded += 1
                        print(f"✅ [{self.total_downloaded}/7200] {filename}")
                    else:
                        print(f"⚠️  Échec HTTP {response.status} pour {filename}")
                            
                except Exception as e:
                    print(f"⚠️  Erreur image {idx}: {str(e)}")
                    continue
                    
            # Mettre à jour la progression
            if progress_key not in self.progress:
                self.progress[progress_key] = 0
            self.progress[progress_key] += downloaded_count
            self.save_progress()
            
            return downloaded_count
            
        except Exception as e:
            error_msg = f"❌ Erreur batch {batch_num} pour {continent}/{ethnicity}/{gender}/{age}: {str(e)}"
            print(error_msg)
            self.errors.append(error_msg)
            return 0
            
    async def download_category(self, page, continent, ethnicity, gender, count):
        """Télécharge tous les portraits d'une catégorie (continent/ethnie/genre)"""
        ethnicity_clean = ethnicity.replace(" ", "_")
        gender_name = "Hommes" if gender == "M" else "Femmes"
        
        # Répartir équitablement entre les deux tranches d'âge
        count_per_age = count // len(AGES)
        remainder = count % len(AGES)
        
        for age_idx, age in enumerate(AGES):
            age_count = count_per_age + (1 if age_idx < remainder else 0)
            
            # Vérifier les fichiers existants
            existing_count = self.count_existing_files(continent, ethnicity, gender, age)
            
            if existing_count >= age_count:
                print(f"    📅 Âge {age} : {existing_count}/{age_count} ✅ Déjà complet, skip")
                self.total_downloaded += existing_count
                continue
            
            remaining_to_download = age_count - existing_count
            num_batches = (remaining_to_download + PORTRAITS_PER_BATCH - 1) // PORTRAITS_PER_BATCH
            
            print(f"    📅 Âge {age} : {existing_count}/{age_count} déjà téléchargés, {remaining_to_download} restants ({num_batches} lots)")
            
            for batch_num in range(num_batches):
                # Calculer combien d'images dans ce lot
                batch_size = min(PORTRAITS_PER_BATCH, remaining_to_download - (batch_num * PORTRAITS_PER_BATCH))
                start_num = existing_count + (batch_num * PORTRAITS_PER_BATCH)
                
                downloaded = await self.download_batch(
                    page, continent, ethnicity, gender, age, batch_num, batch_size, start_num
                )
                
                # Pause entre les lots
                if downloaded > 0:
                    await asyncio.sleep(random.uniform(3, 5))
                else:
                    await asyncio.sleep(2)
                    
    async def download_continent(self, continent, config):
        """Télécharge tous les portraits d'un continent"""
        print(f"\n{'='*70}")
        print(f"🌍 CONTINENT : {continent.upper()}")
        print(f"{'='*70}\n")
        
        page = await self.context.new_page()
        
        try:
            for ethnicity_config in config["ethnicities"]:
                ethnicity = ethnicity_config["name"]
                male_count = ethnicity_config["male"]
                female_count = ethnicity_config["female"]
                total_count = male_count + female_count
                
                print(f"👥 Ethnie : {ethnicity} ({total_count} portraits)")
                
                # Télécharger hommes
                print(f"  🚹 Hommes ({male_count} portraits)")
                await self.download_category(page, continent, ethnicity, "M", male_count)
                
                # Télécharger femmes
                print(f"  🚺 Femmes ({female_count} portraits)")
                await self.download_category(page, continent, ethnicity, "F", female_count)
                
        finally:
            await page.close()
            
    async def run(self):
        """Lance le téléchargement complet"""
        print("🚀 Téléchargement de portraits réalistes depuis thispersonnotexist.org")
        print(f"📊 Objectif : 7200 portraits (1200 par continent × 6 continents)")
        print(f"📁 Destination : {self.base_dir}")
        print(f"⚡ Optimisé : 8 portraits par lot\n")
        
        # Créer la structure
        self.create_directory_structure()
        
        # Initialiser le navigateur
        await self.setup_browser()
        
        start_time = time.time()
        
        try:
            # Télécharger continent par continent
            for continent, config in CONTINENT_CONFIG.items():
                await self.download_continent(continent, config)
                print(f"\n✅ Continent {continent} terminé !")
                
        except KeyboardInterrupt:
            print("\n⚠️  Interruption par l'utilisateur")
        except Exception as e:
            print(f"\n❌ Erreur fatale : {str(e)}")
            import traceback
            traceback.print_exc()
        finally:
            await self.close_browser()
            
        # Rapport final
        elapsed = time.time() - start_time
        hours = int(elapsed // 3600)
        minutes = int((elapsed % 3600) // 60)
        
        print("\n" + "="*70)
        print("📊 RAPPORT FINAL")
        print("="*70)
        print(f"✅ Portraits téléchargés : {self.total_downloaded}/7200")
        print(f"📈 Pourcentage : {(self.total_downloaded/7200)*100:.1f}%")
        print(f"⏱️  Temps écoulé : {hours}h {minutes}min")
        print(f"⚠️  Erreurs : {len(self.errors)}")
        
        if self.errors:
            print("\n❌ Dernières erreurs :")
            for error in self.errors[-5:]:
                print(f"  - {error}")
                
        print("\n✅ Téléchargement terminé !")
        print(f"📁 Portraits sauvegardés dans : {self.base_dir}")
        
if __name__ == "__main__":
    downloader = OptimizedPortraitDownloader()
    asyncio.run(downloader.run())
