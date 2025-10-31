#!/usr/bin/env python3
"""
Script automatique pour lancer la génération sans interaction
"""

import asyncio
import os
import random
from playwright.async_api import async_playwright
from pathlib import Path
import time

# Configuration
OUTPUT_DIR = "/app/backend/static/realistic_portraits/asia/asian/M"
BASE_URL = "https://perchance.org/ai-face-generator"

# Créer le dossier de sortie s'il n'existe pas
Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

async def generate_and_download():
    """Génère et télécharge 9 portraits"""
    async with async_playwright() as p:
        print("🚀 Lancement du navigateur...")
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
            print("🌐 Navigation vers perchance.org...")
            await page.goto(BASE_URL, wait_until='domcontentloaded', timeout=30000)
            await asyncio.sleep(5)
            
            # Prendre un screenshot pour déboguer
            await page.screenshot(path='/tmp/perchance_1_loaded.png')
            print("📸 Screenshot 1 : page chargée")
            
            # Choisir un âge aléatoire
            age = random.choice([20, 30, 40])
            age_range = "21_35" if age <= 35 else "34_50"
            
            # Construire le prompt
            prompt = f"face d'un homme asiatique de l'est qui a {age} ans en gros plan, tête droite de face, photo professionnelle sur fond blanc. on ne voit que la tête et rien en dessous du cou car la tete prend toute l'image"
            
            print(f"📝 Prompt avec âge {age} ans (range: {age_range})")
            
            # Attendre que la page soit complètement chargée
            await page.wait_for_load_state('networkidle', timeout=30000)
            await asyncio.sleep(3)
            
            # Essayer de trouver et remplir le textarea
            print("✍️  Recherche du champ prompt...")
            
            # Inspecter la page
            textareas = await page.query_selector_all('textarea')
            print(f"   Trouvé {len(textareas)} textarea(s)")
            
            if len(textareas) > 0:
                textarea = textareas[0]
                await textarea.fill(prompt)
                print(f"✅ Prompt rempli dans le premier textarea")
                await asyncio.sleep(2)
                
                # Screenshot après remplissage
                await page.screenshot(path='/tmp/perchance_2_prompt.png')
                print("📸 Screenshot 2 : prompt rempli")
            else:
                print("❌ Aucun textarea trouvé")
                await page.screenshot(path='/tmp/perchance_error.png')
                return
            
            # Chercher le sélecteur de forme (shape)
            print("📐 Recherche du sélecteur Shape...")
            selects = await page.query_selector_all('select')
            print(f"   Trouvé {len(selects)} select(s)")
            
            shape_set = False
            for idx, select in enumerate(selects):
                try:
                    # Obtenir les options disponibles
                    options = await select.query_selector_all('option')
                    option_values = []
                    for opt in options:
                        val = await opt.get_attribute('value')
                        if val:
                            option_values.append(val)
                    
                    print(f"   Select {idx}: {option_values}")
                    
                    # Si on trouve "square" dans les options
                    if 'square' in option_values:
                        await select.select_option(value='square')
                        print(f"✅ Format 'square' sélectionné dans select {idx}")
                        shape_set = True
                        await asyncio.sleep(1)
                        break
                except Exception as e:
                    continue
            
            if not shape_set:
                print("⚠️  Format square non trouvé, utilisation du défaut")
            
            # Chercher le nombre d'images
            print("🔢 Recherche du sélecteur 'How many'...")
            number_set = False
            for idx, select in enumerate(selects):
                try:
                    options = await select.query_selector_all('option')
                    option_values = []
                    for opt in options:
                        val = await opt.get_attribute('value')
                        if val:
                            option_values.append(val)
                    
                    # Si on trouve "9" dans les options
                    if '9' in option_values:
                        await select.select_option(value='9')
                        print(f"✅ Nombre '9' sélectionné dans select {idx}")
                        number_set = True
                        await asyncio.sleep(1)
                        break
                except Exception as e:
                    continue
            
            if not number_set:
                print("⚠️  Nombre 9 non sélectionné, utilisation du défaut")
            
            # Screenshot avant génération
            await page.screenshot(path='/tmp/perchance_3_configured.png')
            print("📸 Screenshot 3 : configuration complète")
            
            # Chercher et cliquer sur le bouton Generate
            print("🎨 Recherche du bouton Generate...")
            buttons = await page.query_selector_all('button')
            print(f"   Trouvé {len(buttons)} bouton(s)")
            
            generate_clicked = False
            for idx, button in enumerate(buttons):
                try:
                    text = await button.inner_text()
                    print(f"   Button {idx}: '{text}'")
                    if 'generate' in text.lower() or 'create' in text.lower():
                        await button.click()
                        print(f"✅ Bouton '{text}' cliqué")
                        generate_clicked = True
                        break
                except Exception as e:
                    continue
            
            if not generate_clicked:
                print("❌ Bouton Generate non trouvé")
                return
            
            # Attendre la génération
            print("⏳ Attente de la génération (90 secondes)...")
            await asyncio.sleep(90)
            
            # Screenshot des résultats
            await page.screenshot(path='/tmp/perchance_4_generated.png')
            print("📸 Screenshot 4 : images générées")
            
            # Chercher les images générées
            print("📥 Recherche des images générées...")
            images = await page.query_selector_all('img')
            print(f"   Trouvé {len(images)} image(s) total")
            
            # Filtrer pour ne garder que les images générées
            generated_images = []
            for img in images:
                src = await img.get_attribute('src')
                if src and ('blob:' in src or 'perchance' in src or 'data:image' not in src[:20]):
                    generated_images.append(img)
            
            print(f"   Images potentiellement générées: {len(generated_images)}")
            
            # Télécharger les images
            existing_files = list(Path(OUTPUT_DIR).glob(f"asia_asian_M_{age_range}_*.jpg"))
            if existing_files:
                existing_numbers = [int(f.stem.split('_')[-1]) for f in existing_files]
                next_number = max(existing_numbers) + 1
            else:
                next_number = 1
            
            downloaded = 0
            for idx, img in enumerate(generated_images[:9]):  # Max 9 images
                try:
                    # Prendre un screenshot de l'image
                    filename = f"asia_asian_M_{age_range}_{next_number + downloaded:04d}.jpg"
                    filepath = os.path.join(OUTPUT_DIR, filename)
                    
                    # Screenshot de l'élément image
                    await img.screenshot(path=filepath)
                    print(f"  ✅ {filename}")
                    downloaded += 1
                except Exception as e:
                    print(f"  ⚠️  Erreur image {idx + 1}: {e}")
                    continue
            
            print(f"\n✅ Génération terminée : {downloaded} images téléchargées")
            print(f"📁 Dossier : {OUTPUT_DIR}")
            
        except Exception as e:
            print(f"❌ Erreur : {e}")
            await page.screenshot(path='/tmp/perchance_error.png')
            import traceback
            traceback.print_exc()
        
        finally:
            print("🔒 Fermeture du navigateur...")
            await browser.close()

async def main():
    print("="*60)
    print("🎨 GÉNÉRATION AUTOMATIQUE DE PORTRAITS PERCHANCE")
    print("="*60)
    print("\n🚀 Lancement de la génération de 9 images...")
    await generate_and_download()
    print("\n✅ Script terminé!")

if __name__ == "__main__":
    asyncio.run(main())
