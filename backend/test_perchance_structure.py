#!/usr/bin/env python3
"""
Script de test pour analyser la structure de la page Perchance AI Face Generator
"""

import asyncio
from playwright.async_api import async_playwright


async def analyze_perchance():
    """Analyse la structure de la page Perchance"""
    print("🔍 Analyse de la page Perchance AI Face Generator...\n")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=['--no-sandbox', '--disable-setuid-sandbox']
        )
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080}
        )
        page = await context.new_page()
        
        try:
            # Naviguer vers la page
            print(f"📡 Navigation vers https://perchance.org/ai-face-generator...")
            await page.goto("https://perchance.org/ai-face-generator", wait_until='networkidle', timeout=60000)
            print("✅ Page chargée\n")
            
            # Attendre un peu pour que tout se charge
            await asyncio.sleep(3)
            
            # Analyser les inputs texte
            print("📝 Recherche des champs de texte...")
            text_inputs = await page.query_selector_all("textarea, input[type='text']")
            print(f"   Trouvé {len(text_inputs)} champ(s) de texte")
            for i, input_elem in enumerate(text_inputs):
                placeholder = await input_elem.get_attribute('placeholder')
                name = await input_elem.get_attribute('name')
                id_attr = await input_elem.get_attribute('id')
                print(f"   {i+1}. placeholder='{placeholder}', name='{name}', id='{id_attr}'")
            
            # Analyser les inputs numériques
            print("\n🔢 Recherche des champs numériques...")
            number_inputs = await page.query_selector_all("input[type='number']")
            print(f"   Trouvé {len(number_inputs)} champ(s) numérique(s)")
            for i, input_elem in enumerate(number_inputs):
                placeholder = await input_elem.get_attribute('placeholder')
                name = await input_elem.get_attribute('name')
                id_attr = await input_elem.get_attribute('id')
                value = await input_elem.input_value()
                print(f"   {i+1}. placeholder='{placeholder}', name='{name}', id='{id_attr}', value='{value}'")
            
            # Analyser les boutons
            print("\n🔘 Recherche des boutons...")
            buttons = await page.query_selector_all("button")
            print(f"   Trouvé {len(buttons)} bouton(s)")
            for i, button in enumerate(buttons):
                text = await button.inner_text()
                class_name = await button.get_attribute('class')
                print(f"   {i+1}. text='{text}', class='{class_name}'")
            
            # Prendre une capture d'écran
            print("\n📸 Capture d'écran de la page...")
            await page.screenshot(path="/app/backend/perchance_screenshot.png", full_page=True)
            print("   Sauvegardée: /app/backend/perchance_screenshot.png")
            
            # Attendre pour observer
            print("\n⏸️  Pause de 10 secondes pour observer la page...")
            await asyncio.sleep(10)
            
        finally:
            await context.close()
            await browser.close()
            print("\n✅ Analyse terminée!")


if __name__ == "__main__":
    asyncio.run(analyze_perchance())
