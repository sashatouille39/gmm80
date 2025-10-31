#!/usr/bin/env python3
"""
Script de débogage pour comprendre pourquoi les images ne sont pas trouvées
"""

import asyncio
from playwright.async_api import async_playwright
from pathlib import Path

PERCHANCE_URL = "https://perchance.org/ai-face-generator"
PROMPT = "face d'un homme asiatique de l'est qui a 20 ans en gros plan, tête droite de face, photo professionnelle sur fond blanc"


async def debug_perchance():
    print("🔍 DEBUG PERCHANCE - Analyse détaillée\n")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=['--no-sandbox'])
        context = await browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = await context.new_page()
        
        try:
            print("1️⃣ Navigation...")
            await page.goto(PERCHANCE_URL, wait_until='networkidle', timeout=60000)
            await asyncio.sleep(20)
            
            # Capture avant interaction
            await page.screenshot(path="/app/backend/debug_1_initial.png")
            print("   ✅ Capture 1: Page initiale")
            
            print("\n2️⃣ Remplissage du prompt...")
            textareas = await page.query_selector_all("textarea")
            for ta in textareas:
                if await ta.is_visible():
                    await ta.fill(PROMPT)
                    print(f"   ✅ Prompt saisi")
                    break
            
            await asyncio.sleep(2)
            await page.screenshot(path="/app/backend/debug_2_prompt_filled.png")
            print("   ✅ Capture 2: Prompt rempli")
            
            print("\n3️⃣ Clic sur generate...")
            buttons = await page.query_selector_all("button")
            for btn in buttons:
                text = await btn.inner_text()
                if "✨" in text:
                    await btn.click()
                    print(f"   ✅ Cliqué sur generate")
                    break
            
            await asyncio.sleep(5)
            await page.screenshot(path="/app/backend/debug_3_after_click.png")
            print("   ✅ Capture 3: Juste après le clic")
            
            print("\n4️⃣ Attente 60 secondes...")
            await asyncio.sleep(60)
            await page.screenshot(path="/app/backend/debug_4_after_60s.png", full_page=True)
            print("   ✅ Capture 4: Après 60 secondes")
            
            print("\n5️⃣ Attente 60 secondes supplémentaires...")
            await asyncio.sleep(60)
            await page.screenshot(path="/app/backend/debug_5_after_120s.png", full_page=True)
            print("   ✅ Capture 5: Après 120 secondes")
            
            print("\n6️⃣ Analyse du contenu...")
            
            # Compter toutes les images
            all_imgs = await page.query_selector_all("img")
            print(f"   📊 Total images sur la page: {len(all_imgs)}")
            
            # Analyser chaque image
            for i, img in enumerate(all_imgs[:20]):
                try:
                    src = await img.get_attribute('src')
                    box = await img.bounding_box()
                    if box:
                        print(f"   {i+1}. Taille: {int(box['width'])}x{int(box['height'])}, src: {src[:60] if src else 'None'}...")
                except:
                    pass
            
            # Sauvegarder le HTML
            html = await page.content()
            with open("/app/backend/debug_page.html", "w") as f:
                f.write(html)
            print(f"\n   ✅ HTML sauvegardé ({len(html)} caractères)")
            
            # Chercher des messages d'erreur
            print("\n7️⃣ Recherche d'erreurs...")
            if "too many" in html.lower():
                print("   ⚠️  Texte 'too many' trouvé dans la page")
            if "error" in html.lower():
                print("   ⚠️  Texte 'error' trouvé dans la page")
            if "limit" in html.lower():
                print("   ⚠️  Texte 'limit' trouvé dans la page")
            
            # Chercher des divs de résultats
            print("\n8️⃣ Structure de la page...")
            result_divs = await page.query_selector_all("div[class*='result'], div[class*='output'], div[class*='image']")
            print(f"   📦 Divs de résultats potentiels: {len(result_divs)}")
            
            print("\n✅ Debug terminé!")
            print("\n📂 Fichiers créés:")
            print("   - /app/backend/debug_1_initial.png")
            print("   - /app/backend/debug_2_prompt_filled.png")
            print("   - /app/backend/debug_3_after_click.png")
            print("   - /app/backend/debug_4_after_60s.png")
            print("   - /app/backend/debug_5_after_120s.png")
            print("   - /app/backend/debug_page.html")
            
        finally:
            await context.close()
            await browser.close()


if __name__ == "__main__":
    asyncio.run(debug_perchance())
