#!/usr/bin/env python3
"""
Script amélioré pour générer des portraits depuis perchance.org
Version avec gestion optimisée des timeouts
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
Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

async def generate_portraits():
    """Génère 9 portraits automatiquement"""
    async with async_playwright() as p:
        print("🚀 Démarrage du navigateur Chromium...")
        browser = await p.chromium.launch(
            headless=True,
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-blink-features=AutomationControlled'
            ]
        )
        
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        page = await context.new_page()
        
        try:
            # Choix de l'âge
            age = random.choice([20, 30, 40])
            age_range = "21_35" if age <= 35 else "34_50"
            prompt = f"face d'un homme asiatique de l'est qui a {age} ans en gros plan, tête droite de face, photo professionnelle sur fond blanc. on ne voit que la tête et rien en dessous du cou car la tete prend toute l'image"
            
            print(f"📝 Configuration : âge {age} ans, range {age_range}")
            print(f"🌐 Navigation vers {BASE_URL}...")
            
            # Navigation sans attendre networkidle
            await page.goto(BASE_URL, wait_until='domcontentloaded', timeout=60000)
            print("✅ Page chargée (domcontentloaded)")
            
            # Attente simple
            await asyncio.sleep(8)
            
            # Screenshot initial
            await page.screenshot(path='/tmp/step1_loaded.png', full_page=False)
            print("📸 Screenshot 1 sauvegardé")
            
            # Trouver et remplir le prompt
            print("\n✍️  Remplissage du prompt...")
            textareas = await page.query_selector_all('textarea')
            
            if not textareas:
                print("❌ Aucun textarea trouvé")
                inputs = await page.query_selector_all('input[type="text"]')
                print(f"   Trouvé {len(inputs)} input text à la place")
                if inputs:
                    await inputs[0].fill(prompt)
                    print("✅ Prompt rempli dans input")
                else:
                    return
            else:
                await textareas[0].click()
                await asyncio.sleep(0.5)
                await textareas[0].fill("")
                await asyncio.sleep(0.5)
                await textareas[0].type(prompt, delay=10)
                print(f"✅ Prompt rempli : '{prompt[:50]}...'")
            
            await asyncio.sleep(2)
            await page.screenshot(path='/tmp/step2_prompt.png', full_page=False)
            print("📸 Screenshot 2 sauvegardé")
            
            # Gérer les select
            print("\n🔧 Configuration des paramètres...")
            selects = await page.query_selector_all('select')
            print(f"   Trouvé {len(selects)} select(s)")
            
            for idx, select in enumerate(selects):
                try:
                    options = await select.query_selector_all('option')
                    values = []
                    for opt in options:
                        val = await opt.get_attribute('value')
                        text = await opt.inner_text()
                        values.append(f"{val}:{text}")
                    
                    print(f"   Select #{idx}: {', '.join(values[:5])}")
                    
                    # Essayer de sélectionner square
                    try:
                        await select.select_option(value='square')
                        print(f"   ✅ 'square' sélectionné dans select #{idx}")
                    except:
                        pass
                    
                    # Essayer de sélectionner 9
                    try:
                        await select.select_option(value='9')
                        print(f"   ✅ '9' sélectionné dans select #{idx}")
                    except:
                        pass
                        
                except Exception as e:
                    continue
            
            await asyncio.sleep(2)
            await page.screenshot(path='/tmp/step3_configured.png', full_page=False)
            print("📸 Screenshot 3 sauvegardé")
            
            # Trouver et cliquer sur Generate
            print("\n🎨 Lancement de la génération...")
            buttons = await page.query_selector_all('button')
            
            clicked = False
            for button in buttons:
                try:
                    text = await button.inner_text()
                    if 'generate' in text.lower():
                        await button.click()
                        print(f"✅ Bouton '{text}' cliqué")
                        clicked = True
                        break
                except:
                    continue
            
            if not clicked:
                # Essayer avec d'autres sélecteurs
                try:
                    await page.click('text=Generate', timeout=5000)
                    print("✅ Bouton Generate cliqué (sélecteur text)")
                    clicked = True
                except:
                    pass
            
            if not clicked:
                print("❌ Impossible de cliquer sur Generate")
                return
            
            # Attendre la génération
            print("⏳ Génération en cours (120 secondes)...")
            await asyncio.sleep(120)
            
            await page.screenshot(path='/tmp/step4_generated.png', full_page=True)
            print("📸 Screenshot 4 sauvegardé (page complète)")
            
            # Récupérer les images
            print("\n📥 Récupération des images...")
            
            # Chercher les images avec différents critères
            all_images = await page.query_selector_all('img')
            print(f"   Total d'images dans la page: {len(all_images)}")
            
            # Filtrer les images générées (généralement les plus grandes)
            generated_imgs = []
            for img in all_images:
                try:
                    # Vérifier la taille de l'image
                    box = await img.bounding_box()
                    if box and box['width'] > 200 and box['height'] > 200:
                        src = await img.get_attribute('src')
                        if src and 'logo' not in src.lower() and 'icon' not in src.lower():
                            generated_imgs.append(img)
                except:
                    continue
            
            print(f"   Images candidates (>200px): {len(generated_imgs)}")
            
            # Télécharger les images
            next_num = 1
            existing = list(Path(OUTPUT_DIR).glob(f"asia_asian_M_{age_range}_*.jpg"))
            if existing:
                next_num = max([int(f.stem.split('_')[-1]) for f in existing]) + 1
            
            downloaded = 0
            for idx, img in enumerate(generated_imgs[:9]):
                try:
                    filename = f"asia_asian_M_{age_range}_{next_num + downloaded:04d}.jpg"
                    filepath = os.path.join(OUTPUT_DIR, filename)
                    
                    await img.screenshot(path=filepath, timeout=10000)
                    
                    # Vérifier la taille du fichier
                    size = os.path.getsize(filepath)
                    if size > 5000:  # Au moins 5KB
                        print(f"   ✅ {filename} ({size//1024}KB)")
                        downloaded += 1
                    else:
                        os.remove(filepath)
                        print(f"   ⚠️  Image {idx+1} trop petite, ignorée")
                        
                except Exception as e:
                    print(f"   ⚠️  Erreur image {idx+1}: {str(e)[:50]}")
                    continue
            
            print(f"\n✅ Téléchargement terminé: {downloaded} images sauvegardées")
            print(f"📁 Dossier: {OUTPUT_DIR}")
            
        except Exception as e:
            print(f"\n❌ Erreur générale: {e}")
            import traceback
            traceback.print_exc()
            await page.screenshot(path='/tmp/error_full.png', full_page=True)
            print("📸 Screenshot d'erreur sauvegardé")
            
        finally:
            print("\n🔒 Fermeture du navigateur...")
            await browser.close()

async def main():
    print("="*70)
    print(" 🎨 GÉNÉRATEUR AUTOMATIQUE DE PORTRAITS PERCHANCE v2")
    print("="*70)
    print()
    await generate_portraits()
    print()
    print("="*70)
    print("✅ Terminé!")
    print()
    print("📸 Screenshots disponibles dans /tmp/ pour débogage")
    print("   - step1_loaded.png : Page initiale")
    print("   - step2_prompt.png : Après remplissage du prompt")
    print("   - step3_configured.png : Après configuration")
    print("   - step4_generated.png : Résultat final")
    print("="*70)

if __name__ == "__main__":
    asyncio.run(main())
