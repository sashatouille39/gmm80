#!/usr/bin/env python3
"""
Script SUPER optimisé pour télécharger les portraits en parallèle
Télécharge plusieurs continents simultanément
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
PORTRAITS_PER_BATCH = 8
DELAY_BETWEEN_BATCHES = 2  # Réduit de 3-5s à 2s

# Mapping continent -> ethnies
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

AGES = ["21-35", "34-50"]
EMOTION = "neutral"

class ParallelPortraitDownloader:
    def __init__(self, continent_name):
        self.continent_name = continent_name
        self.base_dir = BASE_DIR
        self.total_downloaded = 0
        self.errors = []
        self.progress_file = Path(f"/tmp/portrait_download_{continent_name}.json")
        self.progress = self.load_progress()
        
    def load_progress(self):
        if self.progress_file.exists():
            with open(self.progress_file, 'r') as f:
                return json.load(f)
        return {}
        
    def save_progress(self):
        with open(self.progress_file, 'w') as f:
            json.dump(self.progress, f, indent=2)
            
    async def setup_browser(self):
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
        await self.context.close()
        await self.browser.close()
        await self.playwright.stop()
        
    def create_directory_structure(self):
        continent = self.continent_name
        for ethnicity_config in CONTINENT_CONFIG[continent]["ethnicities"]:
            ethnicity = ethnicity_config["name"].replace(" ", "_")
            for gender in ["M", "F"]:
                dir_path = self.base_dir / continent / ethnicity / gender
                dir_path.mkdir(parents=True, exist_ok=True)
                
    def count_existing_files(self, continent, ethnicity, gender, age):
        ethnicity_clean = ethnicity.replace(" ", "_")
        dir_path = self.base_dir / continent / ethnicity_clean / gender
        if not dir_path.exists():
            return 0
        age_pattern = age.replace('-', '_')
        existing = list(dir_path.glob(f"{continent}_{ethnicity_clean}_{gender}_{age_pattern}_*.jpg"))
        return len(existing)
    
    async def download_batch(self, page, continent, ethnicity, gender, age, batch_num, batch_size, start_num):
        ethnicity_clean = ethnicity.replace(" ", "_")
        
        try:
            await page.goto('https://thispersonnotexist.org/', wait_until='networkidle', timeout=30000)
            await asyncio.sleep(2)
            
            if gender == "M":
                await page.click('label[for="tabthree"]', force=True)
            else:
                await page.click('label[for="tabtwo"]', force=True)
            await asyncio.sleep(0.5)
            
            await page.select_option('select#xrace', ethnicity)
            await asyncio.sleep(0.5)
            
            await page.select_option('select#xage', age)
            await asyncio.sleep(0.5)
            
            await page.select_option('select#xemotion', EMOTION)
            await asyncio.sleep(0.5)
            
            await page.click('label.reloadbtnx', force=True)
            await asyncio.sleep(6)
            
            images = await page.query_selector_all('img[alt*="Person Face"][alt*="That Not Exist"]')
            
            if len(images) == 0:
                return 0
                
            downloaded_count = 0
            for idx, img in enumerate(images[:batch_size]):
                try:
                    src = await img.get_attribute('src')
                    if not src or src == '#':
                        continue
                        
                    image_num = start_num + idx + 1
                    filename = f"{continent}_{ethnicity_clean}_{gender}_{age.replace('-', '_')}_{image_num:04d}.jpg"
                    file_path = self.base_dir / continent / ethnicity_clean / gender / filename
                    
                    response = await self.context.request.get(src)
                    if response.ok:
                        content = await response.body()
                        with open(file_path, 'wb') as f:
                            f.write(content)
                        downloaded_count += 1
                        self.total_downloaded += 1
                        print(f"✅ [{self.continent_name}] {filename}")
                            
                except Exception as e:
                    continue
            
            return downloaded_count
            
        except Exception as e:
            return 0
            
    async def download_category(self, page, continent, ethnicity, gender, count):
        ethnicity_clean = ethnicity.replace(" ", "_")
        
        count_per_age = count // len(AGES)
        remainder = count % len(AGES)
        
        for age_idx, age in enumerate(AGES):
            age_count = count_per_age + (1 if age_idx < remainder else 0)
            
            existing_count = self.count_existing_files(continent, ethnicity, gender, age)
            
            if existing_count >= age_count:
                print(f"    [{self.continent_name}] {age} : {existing_count}/{age_count} ✅ Skip")
                self.total_downloaded += existing_count
                continue
            
            remaining_to_download = age_count - existing_count
            num_batches = (remaining_to_download + PORTRAITS_PER_BATCH - 1) // PORTRAITS_PER_BATCH
            
            print(f"    [{self.continent_name}] {age} : {existing_count}/{age_count}, {remaining_to_download} restants")
            
            for batch_num in range(num_batches):
                batch_size = min(PORTRAITS_PER_BATCH, remaining_to_download - (batch_num * PORTRAITS_PER_BATCH))
                start_num = existing_count + (batch_num * PORTRAITS_PER_BATCH)
                
                downloaded = await self.download_batch(
                    page, continent, ethnicity, gender, age, batch_num, batch_size, start_num
                )
                
                if downloaded > 0:
                    await asyncio.sleep(DELAY_BETWEEN_BATCHES)
                else:
                    await asyncio.sleep(1)
                    
    async def download_continent(self):
        continent = self.continent_name
        config = CONTINENT_CONFIG[continent]
        
        print(f"\n🌍 [{continent.upper()}] DÉMARRAGE")
        
        page = await self.context.new_page()
        
        try:
            for ethnicity_config in config["ethnicities"]:
                ethnicity = ethnicity_config["name"]
                male_count = ethnicity_config["male"]
                female_count = ethnicity_config["female"]
                
                print(f"👥 [{continent}] {ethnicity}")
                
                print(f"  🚹 [{continent}] Hommes ({male_count})")
                await self.download_category(page, continent, ethnicity, "M", male_count)
                
                print(f"  🚺 [{continent}] Femmes ({female_count})")
                await self.download_category(page, continent, ethnicity, "F", female_count)
                
        finally:
            await page.close()
            
    async def run(self):
        print(f"🚀 [{self.continent_name.upper()}] Démarrage téléchargement")
        
        self.create_directory_structure()
        await self.setup_browser()
        
        start_time = time.time()
        
        try:
            await self.download_continent()
            print(f"\n✅ [{self.continent_name.upper()}] Terminé !")
        except Exception as e:
            print(f"\n❌ [{self.continent_name.upper()}] Erreur : {str(e)}")
        finally:
            await self.close_browser()
            
        elapsed = time.time() - start_time
        print(f"⏱️  [{self.continent_name.upper()}] Temps : {int(elapsed//60)}min")
        print(f"📊 [{self.continent_name.upper()}] Téléchargés : {self.total_downloaded}")

async def download_multiple_continents(continents):
    """Télécharge plusieurs continents en parallèle"""
    tasks = []
    for continent in continents:
        downloader = ParallelPortraitDownloader(continent)
        tasks.append(downloader.run())
    
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    # Télécharger 3 continents en parallèle (pas tous pour ne pas surcharger)
    continents_to_download = ["asia", "europe", "america"]
    
    print("🚀🚀🚀 TÉLÉCHARGEMENT PARALLÈLE - 3 CONTINENTS")
    print("=" * 70)
    print("Continents : asia, europe, america")
    print("=" * 70)
    
    asyncio.run(download_multiple_continents(continents_to_download))
    
    print("\n" + "=" * 70)
    print("✅ TÉLÉCHARGEMENT PARALLÈLE TERMINÉ")
    print("=" * 70)
