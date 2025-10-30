#!/usr/bin/env python3
"""
Script de test pour télécharger un petit échantillon (32 portraits)
"""

import asyncio
import os
import time
from pathlib import Path
from playwright.async_api import async_playwright
import random

BASE_DIR = Path("/app/backend/static/realistic_portraits_sample")
BASE_DIR.mkdir(parents=True, exist_ok=True)

async def test_optimized_download():
    """Test avec 4 lots de 8 portraits"""
    print("🧪 Test de téléchargement optimisé (32 portraits)\n")
    
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(
        headless=True,
        args=['--no-sandbox', '--disable-setuid-sandbox']
    )
    context = await browser.new_context(
        viewport={'width': 1920, 'height': 1080},
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    )
    page = await context.new_page()
    
    tests = [
        {"continent": "africa", "ethnicity": "black", "gender": "M", "age": "21-35"},
        {"continent": "africa", "ethnicity": "black", "gender": "F", "age": "21-35"},
        {"continent": "asia", "ethnicity": "asian", "gender": "M", "age": "34-50"},
        {"continent": "europe", "ethnicity": "white", "gender": "F", "age": "34-50"},
    ]
    
    total_downloaded = 0
    
    try:
        for idx, test in enumerate(tests):
            print(f"\n📦 Lot {idx+1}/4 : {test['continent']} / {test['ethnicity']} / {test['gender']} / {test['age']}")
            
            # Créer le dossier
            ethnicity_clean = test['ethnicity'].replace(" ", "_")
            dir_path = BASE_DIR / test['continent'] / ethnicity_clean / test['gender']
            dir_path.mkdir(parents=True, exist_ok=True)
            
            # Naviguer
            await page.goto('https://thispersonnotexist.org/', wait_until='networkidle', timeout=30000)
            await asyncio.sleep(3)
            
            # Sélectionner genre
            if test['gender'] == "M":
                await page.click('label[for="tabthree"]', force=True)
            else:
                await page.click('label[for="tabtwo"]', force=True)
            await asyncio.sleep(1)
            
            # Sélectionner ethnie
            await page.select_option('select#xrace', test['ethnicity'])
            await asyncio.sleep(1)
            
            # Sélectionner âge
            await page.select_option('select#xage', test['age'])
            await asyncio.sleep(1)
            
            # Sélectionner émotion
            await page.select_option('select#xemotion', 'neutral')
            await asyncio.sleep(1)
            
            # Générer
            await page.click('label.reloadbtnx', force=True)
            print("⏳ Génération en cours...")
            await asyncio.sleep(8)
            
            # Récupérer les images
            images = await page.query_selector_all('img[alt*="Person Face"][alt*="That Not Exist"]')
            print(f"🖼️  {len(images)} images trouvées")
            
            # Télécharger
            for img_idx, img in enumerate(images[:8]):
                try:
                    src = await img.get_attribute('src')
                    if not src or src == '#':
                        continue
                    
                    filename = f"{test['continent']}_{ethnicity_clean}_{test['gender']}_{test['age'].replace('-', '_')}_{img_idx+1:04d}.jpg"
                    file_path = dir_path / filename
                    
                    # Télécharger avec l'API Request de Playwright
                    response = await context.request.get(src)
                    if response.ok:
                        content = await response.body()
                        with open(file_path, 'wb') as f:
                            f.write(content)
                        total_downloaded += 1
                        print(f"  ✅ {filename}")
                    else:
                        print(f"  ⚠️  Échec HTTP {response.status}")
                            
                except Exception as e:
                    print(f"  ⚠️  Erreur : {str(e)}")
                    
            # Pause entre lots
            await asyncio.sleep(3)
            
    except Exception as e:
        print(f"\n❌ Erreur : {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        await page.close()
        await context.close()
        await browser.close()
        await playwright.stop()
        
    print(f"\n✅ Test terminé : {total_downloaded} portraits téléchargés")
    print(f"📁 Dossier : {BASE_DIR}")
    
if __name__ == "__main__":
    asyncio.run(test_optimized_download())
