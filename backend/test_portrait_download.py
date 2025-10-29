"""
Script de test pour télécharger quelques portraits et vérifier que tout fonctionne
"""
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright


async def test_download():
    """Test rapide pour télécharger 2-3 images"""
    test_dir = Path("/app/backend/static/portraits/test")
    test_dir.mkdir(parents=True, exist_ok=True)
    
    print("🧪 Test de téléchargement depuis thispersonnotexist.org\n")
    
    async with async_playwright() as p:
        print("🌐 Lancement du navigateur...")
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080}
        )
        page = await context.new_page()
        
        try:
            # Aller sur le site
            print(f"📍 Navigation vers thispersonnotexist.org...")
            await page.goto("https://thispersonnotexist.org", wait_until='networkidle')
            await page.wait_for_timeout(3000)
            
            print("✓ Page chargée\n")
            
            # Test 1: Homme asiatique
            print("Test 1: Homme asiatique 21-35 ans")
            print("   Sélection race: Asian...", end='')
            await page.click("button:has-text('Asian')")
            await page.wait_for_timeout(1000)
            print(" ✓")
            
            print("   Sélection âge: 21-35...", end='')
            await page.click("button:has-text('21-35')")
            await page.wait_for_timeout(1000)
            print(" ✓")
            
            print("   Sélection genre: Male...", end='')
            await page.click("button:has-text('Male')")
            await page.wait_for_timeout(3000)
            print(" ✓")
            
            print("   Attente de l'image...", end='')
            await page.wait_for_timeout(2000)
            print(" ✓")
            
            # Prendre un screenshot de la page entière
            print("   Capture d'écran de la page...")
            screenshot = await page.screenshot()
            save_path = test_dir / "test_1_asian_male.png"
            with open(save_path, 'wb') as f:
                f.write(screenshot)
            print(f"   ✓ Sauvegardé: {save_path}\n")
            
            # Test 2: Femme noire
            print("Test 2: Femme noire 35-50 ans")
            await page.reload(wait_until='networkidle')
            await page.wait_for_timeout(2000)
            
            print("   Sélection race: Black...", end='')
            await page.click("button:has-text('Black')")
            await page.wait_for_timeout(1000)
            print(" ✓")
            
            print("   Sélection âge: 35-50...", end='')
            await page.click("button:has-text('35-50')")
            await page.wait_for_timeout(1000)
            print(" ✓")
            
            print("   Sélection genre: Female...", end='')
            await page.click("button:has-text('Female')")
            await page.wait_for_timeout(3000)
            print(" ✓")
            
            print("   Attente de l'image...", end='')
            await page.wait_for_timeout(2000)
            print(" ✓")
            
            screenshot = await page.screenshot()
            save_path = test_dir / "test_2_black_female.png"
            with open(save_path, 'wb') as f:
                f.write(screenshot)
            print(f"   ✓ Sauvegardé: {save_path}\n")
            
            print("=" * 60)
            print("✅ Test terminé avec succès!")
            print(f"📁 Images de test sauvegardées dans: {test_dir}")
            print("=" * 60)
            
        except Exception as e:
            print(f"\n❌ Erreur: {e}")
            
            # Screenshot en cas d'erreur
            error_shot = await page.screenshot()
            error_path = test_dir / "error_screenshot.png"
            with open(error_path, 'wb') as f:
                f.write(error_shot)
            print(f"Screenshot d'erreur sauvegardé: {error_path}")
            
        finally:
            await browser.close()


if __name__ == "__main__":
    asyncio.run(test_download())
