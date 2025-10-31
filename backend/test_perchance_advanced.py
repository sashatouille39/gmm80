#!/usr/bin/env python3
"""
Script de test avancé pour Perchance avec attente du chargement JavaScript
"""

import asyncio
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError


async def test_perchance_advanced():
    """Test avancé de la page Perchance avec attentes"""
    print("🧪 Test avancé d'accès à Perchance AI Face Generator\n")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox'])
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        page = await context.new_page()
        
        try:
            print("📡 Navigation vers la page (networkidle)...")
            try:
                await page.goto("https://perchance.org/ai-face-generator", wait_until='networkidle', timeout=60000)
                print("✅ Page chargée avec networkidle\n")
            except PlaywrightTimeoutError:
                print("⚠️  Timeout networkidle, mais on continue...\n")
            
            # Attendre explicitement que le JavaScript se charge
            print("⏳ Attente du chargement complet (20 secondes)...")
            await asyncio.sleep(20)
            
            # Prendre une capture d'écran
            print("\n📸 Capture d'écran après attente...")
            await page.screenshot(path="/app/backend/perchance_test_advanced.png", full_page=True)
            print("   → Sauvegardée: /app/backend/perchance_test_advanced.png\n")
            
            # Obtenir le HTML de la page
            print("📄 Récupération du HTML...")
            html_content = await page.content()
            with open("/app/backend/perchance_page.html", "w", encoding="utf-8") as f:
                f.write(html_content)
            print(f"   → HTML sauvegardé: /app/backend/perchance_page.html")
            print(f"   → Taille: {len(html_content)} caractères\n")
            
            # Vérifier les éléments clés avec attentes
            print("🔍 Recherche des éléments clés (avec attentes):\n")
            
            # Textareas
            print("   Recherche des textareas...")
            textareas = await page.query_selector_all("textarea")
            print(f"   ✓ {len(textareas)} textarea(s)")
            if textareas:
                for i, ta in enumerate(textareas[:3]):
                    placeholder = await ta.get_attribute('placeholder')
                    print(f"      {i+1}. placeholder: {placeholder}")
            
            # Tous les inputs
            print("\n   Recherche de tous les inputs...")
            all_inputs = await page.query_selector_all("input")
            print(f"   ✓ {len(all_inputs)} input(s)")
            
            # Inputs number
            print("\n   Recherche des inputs numériques...")
            number_inputs = await page.query_selector_all("input[type='number']")
            print(f"   ✓ {len(number_inputs)} input numérique(s)")
            if number_inputs:
                for i, inp in enumerate(number_inputs[:3]):
                    value = await inp.input_value()
                    placeholder = await inp.get_attribute('placeholder')
                    print(f"      {i+1}. value: {value}, placeholder: {placeholder}")
            
            # Boutons
            print("\n   Recherche des boutons...")
            buttons = await page.query_selector_all("button")
            print(f"   ✓ {len(buttons)} bouton(s)")
            if buttons:
                for i, btn in enumerate(buttons[:5]):
                    text = await btn.inner_text()
                    print(f"      {i+1}. text: '{text[:50]}'")
            
            # Chercher texte "generate" n'importe où
            print("\n   Recherche du texte 'generate'...")
            try:
                generate_elements = await page.query_selector_all("*:has-text('generate')")
                print(f"   ✓ {len(generate_elements)} élément(s) contenant 'generate'")
            except:
                print(f"   ⚠️  Selector :has-text() non supporté")
            
            # Chercher par XPath
            print("\n   Recherche par XPath...")
            generate_xpath = await page.query_selector_all("xpath=//button[contains(text(), 'generate') or contains(text(), 'Generate')]")
            print(f"   ✓ {len(generate_xpath)} bouton(s) 'generate' (XPath)")
            
            print("\n✅ Test terminé avec succès!")
            return True
            
        except Exception as e:
            print(f"\n❌ Erreur: {e}")
            import traceback
            traceback.print_exc()
            return False
            
        finally:
            await context.close()
            await browser.close()


if __name__ == "__main__":
    result = asyncio.run(test_perchance_advanced())
    exit(0 if result else 1)
