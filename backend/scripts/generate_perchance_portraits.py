#!/usr/bin/env python3
"""
Script pour générer des portraits d'hommes asiatiques depuis perchance.org
et les télécharger dans le dossier approprié.
"""

import asyncio
import os
import random
from playwright.async_api import async_playwright
from pathlib import Path
import time
import base64

# Configuration
OUTPUT_DIR = "/app/backend/static/realistic_portraits/asia/asian/M"
BASE_URL = "https://perchance.org/ai-face-generator"

# Créer le dossier de sortie s'il n'existe pas
Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

async def generate_and_download_portraits(num_batches=1):
    """
    Génère et télécharge des portraits depuis perchance.org
    
    Args:
        num_batches: Nombre de lots de 9 images à générer
    """
    async with async_playwright() as p:
        print("🚀 Lancement du navigateur...")
        browser = await p.chromium.launch(
            headless=False,  # Mode visible pour débogage
            args=['--no-sandbox', '--disable-setuid-sandbox']
        )
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        page = await context.new_page()
        
        try:
            for batch_num in range(1, num_batches + 1):
                print(f"\n{'='*60}")
                print(f"📦 BATCH {batch_num}/{num_batches}")
                print(f"{'='*60}")
                
                # Naviguer vers la page
                print("🌐 Navigation vers perchance.org...")
                await page.goto(BASE_URL, wait_until='networkidle', timeout=60000)
                await asyncio.sleep(3)
                
                # Choisir un âge aléatoire
                age = random.choice([20, 30, 40])
                age_range = "21_35" if age <= 35 else "34_50"
                
                # Construire le prompt
                prompt = f"face d'un homme asiatique de l'est qui a {age} ans en gros plan, tête droite de face, photo professionnelle sur fond blanc. on ne voit que la tête et rien en dessous du cou car la tete prend toute l'image"
                
                print(f"📝 Prompt : {prompt[:80]}...")
                print(f"👤 Âge : {age} ans (range: {age_range})")
                
                # Trouver et remplir le champ de prompt
                print("✍️  Remplissage du prompt...")
                try:
                    # Essayer différents sélecteurs possibles
                    prompt_selectors = [
                        'textarea[placeholder*="prompt"]',
                        'textarea[placeholder*="Prompt"]',
                        'textarea',
                        'input[type="text"]',
                        '#prompt',
                        '.prompt-input'
                    ]
                    
                    prompt_filled = False
                    for selector in prompt_selectors:
                        try:
                            await page.wait_for_selector(selector, timeout=5000)
                            await page.fill(selector, prompt)
                            prompt_filled = True
                            print(f"✅ Prompt rempli avec le sélecteur : {selector}")
                            break
                        except:
                            continue
                    
                    if not prompt_filled:
                        print("❌ Impossible de trouver le champ de prompt")
                        continue
                    
                    await asyncio.sleep(1)
                except Exception as e:
                    print(f"❌ Erreur lors du remplissage du prompt : {e}")
                    continue
                
                # Sélectionner le format "square"
                print("📐 Sélection du format 'square'...")
                try:
                    shape_selectors = [
                        'select[name*="shape"]',
                        'select[name*="Shape"]',
                        '#shape',
                        'select'
                    ]
                    
                    shape_selected = False
                    for selector in shape_selectors:
                        try:
                            await page.wait_for_selector(selector, timeout=5000)
                            await page.select_option(selector, value='square')
                            shape_selected = True
                            print(f"✅ Format 'square' sélectionné avec le sélecteur : {selector}")
                            break
                        except:
                            try:
                                await page.select_option(selector, label='square')
                                shape_selected = True
                                print(f"✅ Format 'square' sélectionné (par label) avec : {selector}")
                                break
                            except:
                                continue
                    
                    if not shape_selected:
                        print("⚠️  Impossible de sélectionner le format square")
                    
                    await asyncio.sleep(1)
                except Exception as e:
                    print(f"⚠️  Erreur lors de la sélection du format : {e}")
                
                # Sélectionner 9 images dans "how many"
                print("🔢 Sélection de 9 images...")
                try:
                    # Essayer différents sélecteurs pour le nombre d'images
                    number_selectors = [
                        'select',
                        'input[type="number"]',
                        '#howMany',
                        '#number',
                        'select[name*="count"]',
                        'select[name*="number"]'
                    ]
                    
                    number_selected = False
                    for selector in number_selectors:
                        try:
                            await page.wait_for_selector(selector, timeout=5000)
                            await page.select_option(selector, value='9')
                            number_selected = True
                            print(f"✅ Nombre sélectionné (9) avec le sélecteur : {selector}")
                            break
                        except:
                            try:
                                await page.fill(selector, '9')
                                number_selected = True
                                print(f"✅ Nombre rempli (9) avec le sélecteur : {selector}")
                                break
                            except:
                                continue
                    
                    if not number_selected:
                        print("⚠️  Impossible de sélectionner le nombre, utilisation de la valeur par défaut")
                    
                    await asyncio.sleep(1)
                except Exception as e:
                    print(f"⚠️  Erreur lors de la sélection du nombre : {e}")
                
                # Cliquer sur le bouton de génération
                print("🎨 Génération des images...")
                try:
                    generate_selectors = [
                        'button:has-text("Generate")',
                        'button:has-text("Create")',
                        'button[type="submit"]',
                        '.generate-button',
                        '#generate'
                    ]
                    
                    generated = False
                    for selector in generate_selectors:
                        try:
                            await page.click(selector, timeout=5000)
                            generated = True
                            print(f"✅ Bouton de génération cliqué : {selector}")
                            break
                        except:
                            continue
                    
                    if not generated:
                        print("❌ Impossible de trouver le bouton de génération")
                        continue
                    
                    # Attendre la génération des images
                    print("⏳ Attente de la génération des images (60s)...")
                    await asyncio.sleep(60)
                    
                except Exception as e:
                    print(f"❌ Erreur lors de la génération : {e}")
                    continue
                
                # Télécharger les images
                print("📥 Téléchargement des images...")
                try:
                    # Trouver toutes les images générées
                    images = await page.query_selector_all('img[src^="data:image"], img[src^="http"]')
                    
                    downloaded_count = 0
                    for idx, img in enumerate(images):
                        try:
                            # Obtenir l'URL de l'image
                            src = await img.get_attribute('src')
                            
                            if not src or 'data:image' in src[:20]:
                                # Image base64, la télécharger différemment
                                continue
                            
                            # Trouver le prochain numéro disponible
                            existing_files = list(Path(OUTPUT_DIR).glob(f"asia_asian_M_{age_range}_*.jpg"))
                            if existing_files:
                                existing_numbers = [int(f.stem.split('_')[-1]) for f in existing_files]
                                next_number = max(existing_numbers) + 1
                            else:
                                next_number = 1
                            
                            filename = f"asia_asian_M_{age_range}_{next_number + downloaded_count:04d}.jpg"
                            filepath = os.path.join(OUTPUT_DIR, filename)
                            
                            # Télécharger l'image
                            async with page.context.expect_page() as new_page_info:
                                await page.evaluate(f'window.open("{src}", "_blank")')
                            new_page = await new_page_info.value
                            
                            # Sauvegarder l'image
                            await new_page.screenshot(path=filepath, full_page=True)
                            await new_page.close()
                            
                            downloaded_count += 1
                            print(f"  ✅ {filename}")
                            
                        except Exception as e:
                            print(f"  ⚠️  Erreur lors du téléchargement de l'image {idx + 1} : {e}")
                            continue
                    
                    print(f"\n📊 Batch {batch_num} terminé : {downloaded_count} images téléchargées")
                    
                except Exception as e:
                    print(f"❌ Erreur lors du téléchargement des images : {e}")
                    continue
                
                # Pause entre les batchs
                if batch_num < num_batches:
                    print(f"\n⏸️  Pause de 5 secondes avant le prochain batch...")
                    await asyncio.sleep(5)
        
        finally:
            print("\n🔒 Fermeture du navigateur...")
            await browser.close()
    
    print(f"\n✅ Script terminé !")
    print(f"📁 Dossier de sortie : {OUTPUT_DIR}")

async def main():
    """Point d'entrée principal"""
    print("="*60)
    print("🎨 GÉNÉRATEUR DE PORTRAITS PERCHANCE")
    print("="*60)
    
    # Demander le nombre de batchs
    try:
        num_batches = int(input("\n💬 Combien de lots de 9 images voulez-vous générer ? (défaut: 1) : ") or "1")
    except:
        num_batches = 1
    
    print(f"\n📋 Configuration :")
    print(f"  • Nombre de batchs : {num_batches}")
    print(f"  • Images par batch : 9")
    print(f"  • Total estimé : {num_batches * 9} images")
    print(f"  • Dossier de sortie : {OUTPUT_DIR}")
    
    input("\n⏸️  Appuyez sur Entrée pour commencer...")
    
    await generate_and_download_portraits(num_batches)

if __name__ == "__main__":
    asyncio.run(main())
