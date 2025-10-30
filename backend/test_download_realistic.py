#!/usr/bin/env python3
"""
Script de test pour télécharger quelques portraits depuis thispersonnotexist.org
"""

import asyncio
import os
import time
from pathlib import Path
from playwright.async_api import async_playwright
import random

# Configuration de test
BASE_DIR = Path("/app/backend/static/realistic_portraits_test")
BASE_DIR.mkdir(parents=True, exist_ok=True)

async def test_download():
    """Test de téléchargement de quelques portraits"""
    print("🧪 Test de téléchargement depuis thispersonnotexist.org\n")
    
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
    
    try:
        # Test 1: Homme asiatique
        print("📸 Test 1: Homme asiatique, 21-35 ans, émotion neutre")
        await page.goto('https://thispersonnotexist.org/', wait_until='networkidle', timeout=30000)
        await asyncio.sleep(5)
        
        # Sélectionner homme (cliquer sur le label car l'input est caché)
        await page.click('label[for="tabthree"]', force=True)
        await asyncio.sleep(2)
        
        # Sélectionner asian
        await page.select_option('select#xrace', 'asian')
        await asyncio.sleep(1)
        
        # Sélectionner âge
        await page.select_option('select#xage', '21-35')
        await asyncio.sleep(1)
        
        # Sélectionner émotion neutre
        await page.select_option('select#xemotion', 'neutral')
        await asyncio.sleep(1)
        
        # Cliquer sur reload
        await page.click('label.reloadbtnx')
        print("⏳ Attente de la génération...")
        await asyncio.sleep(8)
        
        # Prendre une capture d'écran pour debug
        await page.screenshot(path=str(BASE_DIR / "screenshot_test1.png"))
        print("📸 Capture d'écran sauvegardée")
        
        # Chercher toutes les images
        images = await page.query_selector_all('img')
        print(f"🔍 Trouvé {len(images)} images sur la page")
        
        for idx, img in enumerate(images):
            src = await img.get_attribute('src')
            alt = await img.get_attribute('alt')
            print(f"  Image {idx}: src='{src[:50] if src else 'None'}...' alt='{alt}'")
        
        # Test 2: Femme blanche
        print("\n📸 Test 2: Femme blanche, 34-50 ans, émotion neutre")
        await page.goto('https://thispersonnotexist.org/', wait_until='domcontentloaded', timeout=30000)
        await asyncio.sleep(3)
        
        # Sélectionner femme
        await page.click('input#tabtwo')
        await asyncio.sleep(1)
        
        # Sélectionner white
        await page.select_option('select#xrace', 'white')
        await asyncio.sleep(1)
        
        # Sélectionner âge
        await page.select_option('select#xage', '34-50')
        await asyncio.sleep(1)
        
        # Sélectionner émotion neutre
        await page.select_option('select#xemotion', 'neutral')
        await asyncio.sleep(1)
        
        # Cliquer sur reload
        await page.click('label.reloadbtnx')
        print("⏳ Attente de la génération...")
        await asyncio.sleep(8)
        
        # Capture d'écran
        await page.screenshot(path=str(BASE_DIR / "screenshot_test2.png"))
        print("📸 Capture d'écran sauvegardée")
        
        # Chercher les images
        images = await page.query_selector_all('img')
        print(f"🔍 Trouvé {len(images)} images sur la page")
        
        for idx, img in enumerate(images):
            src = await img.get_attribute('src')
            alt = await img.get_attribute('alt')
            print(f"  Image {idx}: src='{src[:50] if src else 'None'}...' alt='{alt}'")
        
        print("\n✅ Tests terminés avec succès")
        print(f"📁 Captures d'écran dans : {BASE_DIR}")
        
    except Exception as e:
        print(f"\n❌ Erreur : {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        await page.close()
        await context.close()
        await browser.close()
        await playwright.stop()

if __name__ == "__main__":
    asyncio.run(test_download())
