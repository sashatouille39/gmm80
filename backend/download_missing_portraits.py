#!/usr/bin/env python3
"""
Script pour télécharger les 2 portraits manquants qui ont des numéros manquants dans la séquence.
"""

import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

BASE_DIR = Path("/app/backend/static/realistic_portraits")

# Fichiers manquants à télécharger
MISSING_PORTRAITS = [
    {
        "continent": "asia",
        "ethnicity": "asian",
        "gender": "M",
        "age": "21-35",
        "number": 129,
        "ethnicity_selector": "Asian"
    },
    {
        "continent": "middle_east",
        "ethnicity": "middle_eastern",
        "gender": "M",
        "age": "21-35",
        "number": 297,
        "ethnicity_selector": "Middle Eastern"
    }
]

async def download_missing_portrait(portrait_info):
    """Télécharge un portrait manquant"""
    continent = portrait_info["continent"]
    ethnicity = portrait_info["ethnicity"]
    gender = portrait_info["gender"]
    age = portrait_info["age"]
    number = portrait_info["number"]
    ethnicity_selector = portrait_info["ethnicity_selector"]
    
    print(f"\n🔄 Téléchargement de {continent}/{ethnicity}/{gender}/{age} #{number}")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
        )
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        page = await context.new_page()
        
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
            await page.select_option('select#xrace', ethnicity_selector)
            await asyncio.sleep(1)
            
            # Sélectionner l'âge
            await page.select_option('select#xage', age)
            await asyncio.sleep(1)
            
            # Sélectionner l'émotion neutre
            await page.select_option('select#xemotion', 'neutral')
            await asyncio.sleep(1)
            
            # Cliquer sur reload pour générer les images
            await page.click('label.reloadbtnx', force=True)
            await asyncio.sleep(8)  # Attendre la génération
            
            # Récupérer la première image générée
            images = await page.query_selector_all('img[alt*="Person Face"][alt*="That Not Exist"]')
            
            if len(images) == 0:
                print(f"❌ Aucune image trouvée")
                return False
                
            # Prendre la première image
            img = images[0]
            src = await img.get_attribute('src')
            
            if not src or src == '#':
                print(f"❌ URL d'image invalide")
                return False
                
            # Télécharger l'image
            age_pattern = age.replace('-', '_')
            filename = f"{continent}_{ethnicity}_{gender}_{age_pattern}_{number:04d}.jpg"
            file_path = BASE_DIR / continent / ethnicity / gender / filename
            
            # Télécharger avec l'API Request de Playwright
            response = await context.request.get(src)
            if response.ok:
                content = await response.body()
                with open(file_path, 'wb') as f:
                    f.write(content)
                print(f"✅ {filename} téléchargé avec succès")
                return True
            else:
                print(f"❌ Échec HTTP {response.status}")
                return False
                
        except Exception as e:
            print(f"❌ Erreur: {str(e)}")
            return False
        finally:
            await context.close()
            await browser.close()

async def main():
    print("🚀 Téléchargement des 2 portraits manquants")
    print("=" * 70)
    
    success_count = 0
    for portrait_info in MISSING_PORTRAITS:
        result = await download_missing_portrait(portrait_info)
        if result:
            success_count += 1
        await asyncio.sleep(3)  # Pause entre les téléchargements
    
    print("\n" + "=" * 70)
    print(f"📊 Résultat : {success_count}/{len(MISSING_PORTRAITS)} portraits téléchargés")
    
    if success_count == len(MISSING_PORTRAITS):
        print("✅ Tous les portraits manquants ont été téléchargés !")
        print("🎉 Collection complète : 7200/7200 portraits")
    else:
        print(f"⚠️  {len(MISSING_PORTRAITS) - success_count} portrait(s) n'a/ont pas pu être téléchargé(s)")

if __name__ == "__main__":
    asyncio.run(main())
