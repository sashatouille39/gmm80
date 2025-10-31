#!/usr/bin/env python3
"""
Script de test rapide pour vérifier l'accès à Perchance
"""

import asyncio
from playwright.async_api import async_playwright


async def test_perchance():
    """Test rapide de la page Perchance"""
    print("🧪 Test d'accès à Perchance AI Face Generator\n")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox'])
        context = await browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = await context.new_page()
        
        try:
            print("📡 Navigation vers la page...")
            await page.goto("https://perchance.org/ai-face-generator", wait_until='domcontentloaded', timeout=30000)
            print("✅ Page chargée\n")
            
            await asyncio.sleep(3)
            
            # Prendre une capture d'écran
            print("📸 Capture d'écran...")
            await page.screenshot(path="/app/backend/perchance_test.png", full_page=False)
            print("   → Sauvegardée: /app/backend/perchance_test.png\n")
            
            # Vérifier les éléments clés
            print("🔍 Recherche des éléments clés:")
            
            # Textareas
            textareas = await page.query_selector_all("textarea")
            print(f"   ✓ {len(textareas)} textarea(s) trouvé(s)")
            
            # Boutons
            buttons = await page.query_selector_all("button")
            print(f"   ✓ {len(buttons)} bouton(s) trouvé(s)")
            
            # Inputs number
            number_inputs = await page.query_selector_all("input[type='number']")
            print(f"   ✓ {len(number_inputs)} input numérique(s) trouvé(s)")
            
            # Chercher texte "generate"
            generate_button = await page.query_selector("button:has-text('generate')")
            if generate_button:
                print(f"   ✓ Bouton 'generate' trouvé!")
            else:
                print(f"   ⚠️  Bouton 'generate' non trouvé")
            
            print("\n✅ Test terminé avec succès!")
            return True
            
        except Exception as e:
            print(f"\n❌ Erreur: {e}")
            return False
            
        finally:
            await context.close()
            await browser.close()


if __name__ == "__main__":
    result = asyncio.run(test_perchance())
    exit(0 if result else 1)
