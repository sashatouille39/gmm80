"""
Script pour analyser la structure HTML de thispersonnotexist.org
"""
import asyncio
from playwright.async_api import async_playwright


async def analyze_page():
    """Analyse la structure de la page"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        try:
            print("📍 Navigation vers thispersonnotexist.org...")
            await page.goto("https://thispersonnotexist.org", wait_until='networkidle')
            await page.wait_for_timeout(5000)
            
            # Extraire le HTML
            html = await page.content()
            
            # Sauvegarder le HTML
            with open('/app/backend/static/portraits/test/page_structure.html', 'w', encoding='utf-8') as f:
                f.write(html)
            
            print("✓ HTML sauvegardé dans page_structure.html")
            
            # Chercher tous les boutons
            print("\n🔍 Recherche des boutons...")
            buttons = await page.query_selector_all('button')
            print(f"   Trouvé {len(buttons)} boutons")
            
            for i, button in enumerate(buttons[:20]):  # Premiers 20 boutons
                text = await button.inner_text()
                class_name = await button.get_attribute('class')
                print(f"   Button {i+1}: '{text}' (class: {class_name})")
            
            # Chercher les éléments avec le texte "Asian", "White", etc.
            print("\n🔍 Recherche d'éléments avec Race...")
            selectors_to_try = [
                '*:has-text("Asian")',
                '*:has-text("White")',
                '*:has-text("Black")',
                '*:has-text("Male")',
                '*:has-text("Female")'
            ]
            
            for selector in selectors_to_try:
                elements = await page.query_selector_all(selector)
                if elements:
                    elem = elements[0]
                    tag = await elem.evaluate('el => el.tagName')
                    class_name = await elem.get_attribute('class')
                    text = await elem.inner_text()
                    print(f"   '{text}': <{tag}> class='{class_name}'")
            
            print("\n✓ Analyse terminée")
            
        except Exception as e:
            print(f"❌ Erreur: {e}")
        finally:
            await browser.close()


if __name__ == "__main__":
    asyncio.run(analyze_page())
