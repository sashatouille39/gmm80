#!/usr/bin/env python3
"""
Script d'automatisation optimisé pour télécharger des portraits depuis Perchance AI Face Generator
Pour des hommes asiatiques de l'est de différents âges (20, 30, 40 ans)

Basé sur la structure réelle de la page Perchance:
- Champ "Description" pour le prompt
- Champ "How many?" pour le nombre (3, 6, ou 9)
- Bouton "generate" pour lancer
"""

import asyncio
import os
import time
import base64
from pathlib import Path
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
import sys

# Configuration
TARGET_DIR = Path("/app/backend/static/realistic_portraits/asia/asian/M")
PERCHANCE_URL = "https://perchance.org/ai-face-generator"
AGES = [20, 30, 40]
IMAGES_PER_BATCH = 9
WAIT_TIME_GENERATION = 90  # Temps d'attente pour la génération (secondes)
MAX_CONSECUTIVE_FAILURES = 3  # Arrêt après 3 échecs consécutifs (probablement plus de crédits)

# Prompt template
PROMPT_TEMPLATE = """face d'un homme asiatique de l'est qui a {age} ans en gros plan, tête droite de face, photo professionnelle sur fond blanc. on ne voit que la tête et rien en dessous du cou car la tete prend toute l'image"""


class PerchancePortraitDownloader:
    def __init__(self):
        self.target_dir = TARGET_DIR
        self.total_downloaded = 0
        self.errors = []
        self.playwright = None
        self.browser = None
        self.context = None
        
    async def setup_browser(self):
        """Initialise le navigateur Playwright"""
        print("🚀 Initialisation du navigateur...")
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-setuid-sandbox']
        )
        self.context = await self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        print("✅ Navigateur initialisé")
        
    async def close_browser(self):
        """Ferme le navigateur"""
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        print("🔚 Navigateur fermé")
    
    async def wait_for_images_to_load(self, page, expected_count=9, max_wait=120):
        """Attend que toutes les images soient chargées"""
        print(f"   ⏳ Attente du chargement de {expected_count} images...")
        start_time = time.time()
        
        while time.time() - start_time < max_wait:
            # Compter les images qui semblent être des portraits générés
            images = await page.query_selector_all("img")
            
            # Filtrer pour ne garder que les vraies images générées
            valid_images = []
            for img in images:
                src = await img.get_attribute('src')
                if src and (src.startswith('data:image') or 'blob:' in src or src.startswith('http')):
                    # Vérifier la taille de l'image
                    box = await img.bounding_box()
                    if box and box['width'] > 100 and box['height'] > 100:
                        valid_images.append(img)
            
            count = len(valid_images)
            if count >= expected_count:
                print(f"   ✅ {count} images détectées et chargées!")
                return valid_images
            
            # Afficher la progression
            if int(time.time() - start_time) % 10 == 0:
                print(f"      ... {count}/{expected_count} images chargées ({int(time.time() - start_time)}s)")
            
            await asyncio.sleep(2)
        
        print(f"   ⚠️  Timeout: seulement {len(valid_images)}/{expected_count} images chargées")
        return valid_images
        
    async def download_batch(self, age: int, batch_number: int):
        """Télécharge un batch de 9 images pour un âge donné"""
        print(f"\n{'='*60}")
        print(f"📥 Batch {batch_number}/{len(AGES)} - Âge: {age} ans")
        print(f"{'='*60}")
        
        page = await self.context.new_page()
        
        try:
            # Naviguer vers Perchance avec un timeout plus court
            print(f"🌐 Navigation vers Perchance...")
            try:
                await page.goto(PERCHANCE_URL, wait_until='domcontentloaded', timeout=30000)
            except PlaywrightTimeoutError:
                print("   ⚠️  Timeout de navigation, mais on continue...")
            
            await asyncio.sleep(3)
            print("   ✅ Page chargée")
            
            # Générer le prompt
            prompt = PROMPT_TEMPLATE.format(age=age)
            print(f"✍️  Configuration du prompt...")
            print(f"   → {prompt[:80]}...")
            
            # Chercher le champ de description et le remplir
            # Essayer plusieurs sélecteurs possibles
            description_selectors = [
                "textarea",
                "input[placeholder*='escription']",
                "textarea[placeholder*='escription']",
                "#description",
                ".description"
            ]
            
            description_filled = False
            for selector in description_selectors:
                try:
                    elements = await page.query_selector_all(selector)
                    if elements:
                        # Prendre le premier élément visible
                        for elem in elements:
                            is_visible = await elem.is_visible()
                            if is_visible:
                                await elem.fill(prompt)
                                print(f"   ✅ Prompt saisi (sélecteur: {selector})")
                                description_filled = True
                                break
                        if description_filled:
                            break
                except Exception as e:
                    continue
            
            if not description_filled:
                print("   ⚠️  Attention: Champ de description non trouvé!")
            
            await asyncio.sleep(1)
            
            # Configurer le nombre d'images à 9
            print(f"🔢 Configuration: {IMAGES_PER_BATCH} images...")
            
            # Chercher le champ "How many?"
            number_selectors = [
                "input[type='number']",
                "select",
                "input[value='9']",
                "button:has-text('9')"
            ]
            
            number_configured = False
            for selector in number_selectors:
                try:
                    elements = await page.query_selector_all(selector)
                    if elements:
                        for elem in elements:
                            is_visible = await elem.is_visible()
                            if is_visible:
                                tag = await elem.evaluate("el => el.tagName")
                                
                                if tag.lower() == 'input':
                                    await elem.fill(str(IMAGES_PER_BATCH))
                                elif tag.lower() == 'select':
                                    await elem.select_option(str(IMAGES_PER_BATCH))
                                elif tag.lower() == 'button':
                                    await elem.click()
                                
                                print(f"   ✅ Nombre configuré à {IMAGES_PER_BATCH}")
                                number_configured = True
                                break
                        if number_configured:
                            break
                except Exception as e:
                    continue
            
            if not number_configured:
                print(f"   ⚠️  Note: Champ 'How many' non configuré (valeur par défaut utilisée)")
            
            await asyncio.sleep(1)
            
            # Cliquer sur le bouton de génération
            print("🎨 Lancement de la génération...")
            
            generate_selectors = [
                "button:has-text('generate')",
                "button:has-text('✨')",
                "input[type='submit']",
                "button[type='submit']"
            ]
            
            generate_clicked = False
            for selector in generate_selectors:
                try:
                    button = await page.query_selector(selector)
                    if button:
                        is_visible = await button.is_visible()
                        if is_visible:
                            await button.click()
                            print(f"   ✅ Bouton 'generate' cliqué")
                            generate_clicked = True
                            break
                except Exception as e:
                    continue
            
            if not generate_clicked:
                print("   ⚠️  Attention: Bouton 'generate' non trouvé!")
                return 0
            
            # Attendre que les images soient générées et chargées
            print(f"⏳ Attente de la génération ({WAIT_TIME_GENERATION}s)...")
            await asyncio.sleep(WAIT_TIME_GENERATION)
            
            # Attendre explicitement le chargement des images
            valid_images = await self.wait_for_images_to_load(page, IMAGES_PER_BATCH)
            
            if not valid_images:
                print("   ❌ Aucune image générée détectée!")
                return 0
            
            # Télécharger les images
            print(f"📸 Téléchargement de {len(valid_images)} images...")
            downloaded_count = 0
            
            for i, img in enumerate(valid_images[:IMAGES_PER_BATCH]):
                try:
                    # Récupérer l'image en base64
                    image_data = await img.evaluate("""
                        (img) => {
                            const canvas = document.createElement('canvas');
                            canvas.width = img.naturalWidth;
                            canvas.height = img.naturalHeight;
                            const ctx = canvas.getContext('2d');
                            ctx.drawImage(img, 0, 0);
                            return canvas.toDataURL('image/jpeg');
                        }
                    """)
                    
                    if image_data and image_data.startswith('data:image'):
                        # Décoder l'image
                        image_bytes = base64.b64decode(image_data.split(',')[1])
                        
                        # Générer le nom de fichier
                        existing_files = list(self.target_dir.glob(f"perchance_asia_asian_M_{age}_*.jpg"))
                        next_num = len(existing_files) + 1
                        filename = f"perchance_asia_asian_M_{age}_{next_num:04d}.jpg"
                        filepath = self.target_dir / filename
                        
                        # Sauvegarder
                        with open(filepath, 'wb') as f:
                            f.write(image_bytes)
                        
                        downloaded_count += 1
                        self.total_downloaded += 1
                        print(f"   ✅ Image {i+1}/{len(valid_images)}: {filename} ({len(image_bytes) // 1024} KB)")
                    else:
                        print(f"   ⚠️  Image {i+1}: données invalides")
                        
                except Exception as e:
                    print(f"   ❌ Erreur image {i+1}: {str(e)[:50]}")
                    continue
            
            print(f"\n✅ Batch terminé: {downloaded_count}/{IMAGES_PER_BATCH} images sauvegardées")
            return downloaded_count
            
        except Exception as e:
            error_msg = f"❌ Erreur batch {batch_number} (âge {age}): {e}"
            print(error_msg)
            self.errors.append(error_msg)
            
            # Prendre une capture d'écran pour déboguer
            try:
                screenshot_path = f"/app/backend/error_screenshot_age{age}.png"
                await page.screenshot(path=screenshot_path)
                print(f"   📸 Capture d'écran sauvegardée: {screenshot_path}")
            except:
                pass
            
            return 0
            
        finally:
            await page.close()
    
    async def run(self):
        """Exécute le téléchargement complet en boucle jusqu'à épuisement des crédits"""
        print("\n" + "="*70)
        print("🎯 TÉLÉCHARGEMENT AUTOMATIQUE - PERCHANCE AI FACE GENERATOR")
        print("🔄 MODE ILLIMITÉ : Continue jusqu'à épuisement des crédits")
        print("="*70)
        print(f"📁 Dossier cible: {self.target_dir}")
        print(f"🎭 Âges en rotation: {', '.join(map(str, AGES))} ans")
        print(f"📊 Images par batch: {IMAGES_PER_BATCH}")
        print(f"🕐 Temps de génération: ~{WAIT_TIME_GENERATION}s par batch")
        print(f"⛔ Arrêt après {MAX_CONSECUTIVE_FAILURES} échecs consécutifs")
        print("="*70 + "\n")
        
        # Créer le dossier si nécessaire
        self.target_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialiser le navigateur
        await self.setup_browser()
        
        batch_number = 0
        consecutive_failures = 0
        
        try:
            # Boucle infinie jusqu'à échec critique
            while True:
                # Alterner entre les âges
                age = AGES[batch_number % len(AGES)]
                batch_number += 1
                
                print(f"\n{'='*70}")
                print(f"🔄 BATCH #{batch_number} - Âge: {age} ans")
                print(f"📊 Statistiques: {self.total_downloaded} images téléchargées au total")
                print(f"{'='*70}")
                
                downloaded = await self.download_batch(age, batch_number)
                
                if downloaded == 0:
                    consecutive_failures += 1
                    print(f"\n⚠️  Échec #{consecutive_failures}/{MAX_CONSECUTIVE_FAILURES}")
                    
                    if consecutive_failures >= MAX_CONSECUTIVE_FAILURES:
                        print(f"\n🛑 ARRÊT: {MAX_CONSECUTIVE_FAILURES} échecs consécutifs détectés")
                        print("   Probablement plus de crédits Perchance disponibles.")
                        break
                else:
                    # Réinitialiser le compteur d'échecs si succès
                    consecutive_failures = 0
                
                # Pause entre les batches
                pause_time = 5
                print(f"\n⏸️  Pause de {pause_time} secondes avant le prochain batch...")
                await asyncio.sleep(pause_time)
            
            # Résumé final
            print("\n" + "="*70)
            print("📊 RÉSUMÉ FINAL")
            print("="*70)
            print(f"🔢 Total de batches traités: {batch_number}")
            print(f"✅ Total d'images téléchargées: {self.total_downloaded}")
            print(f"📈 Moyenne par batch réussi: {self.total_downloaded / max(batch_number - consecutive_failures, 1):.1f} images")
            print(f"❌ Échecs consécutifs finaux: {consecutive_failures}")
            print(f"⚠️  Erreurs rencontrées: {len(self.errors)}")
            
            if self.errors:
                print("\n📝 Dernières erreurs:")
                for error in self.errors[-5:]:  # Afficher seulement les 5 dernières
                    print(f"   - {error}")
            
            # Vérifier les fichiers créés
            print(f"\n📂 Vérification du dossier {self.target_dir}...")
            files = list(self.target_dir.glob("perchance_*.jpg"))
            print(f"   {len(files)} fichier(s) Perchance trouvé(s)")
            
            print("\n🎉 TÉLÉCHARGEMENT TERMINÉ - CRÉDITS ÉPUISÉS!")
            print("="*70 + "\n")
            
        except KeyboardInterrupt:
            print("\n\n⚠️  Arrêt manuel par l'utilisateur")
            print(f"📊 {self.total_downloaded} images téléchargées avant l'arrêt")
            raise
            
        finally:
            await self.close_browser()


async def main():
    """Point d'entrée principal"""
    downloader = PerchancePortraitDownloader()
    await downloader.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Téléchargement interrompu par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Erreur fatale: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
