#!/usr/bin/env python3
"""
Script d'automatisation OPTIMISÉ pour télécharger des portraits depuis Perchance AI Face Generator
Version améliorée avec gestion des iframes et du contenu dynamique
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
WAIT_TIME_GENERATION = 120  # Augmenté pour être sûr
MAX_CONSECUTIVE_FAILURES = 3

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
    
    async def download_batch(self, age: int, batch_number: int):
        """Télécharge un batch de 9 images pour un âge donné"""
        print(f"\n{'='*60}")
        print(f"📥 Batch #{batch_number} - Âge: {age} ans")
        print(f"{'='*60}")
        
        page = await self.context.new_page()
        
        try:
            # Naviguer vers Perchance
            print(f"🌐 Navigation vers Perchance...")
            try:
                await page.goto(PERCHANCE_URL, wait_until='networkidle', timeout=60000)
            except PlaywrightTimeoutError:
                await page.goto(PERCHANCE_URL, wait_until='domcontentloaded', timeout=30000)
            
            print("   ✅ Page chargée")
            
            # Attendre que le contenu soit chargé (important pour Perchance)
            print("   ⏳ Attente du chargement complet...")
            await asyncio.sleep(15)
            
            # Générer le prompt
            prompt = PROMPT_TEMPLATE.format(age=age)
            print(f"✍️  Prompt: {prompt[:80]}...")
            
            # Chercher dans toute la page ET dans les iframes
            print("🔍 Recherche des éléments d'interface...")
            
            # Essayer directement dans la page principale
            description_elem = None
            all_frames = [page] + page.frames
            
            for frame in all_frames:
                try:
                    # Chercher le textarea de description
                    textareas = await frame.query_selector_all("textarea")
                    for ta in textareas:
                        is_visible = await ta.is_visible()
                        if is_visible:
                            # Vérifier si c'est le bon textarea (pas le scratchpad)
                            parent_text = ""
                            try:
                                parent = await ta.evaluate_handle("el => el.parentElement")
                                parent_text = await parent.evaluate("el => el.textContent")
                            except:
                                pass
                            
                            if "description" in parent_text.lower() or not description_elem:
                                description_elem = ta
                                print(f"   ✅ Champ de description trouvé")
                                await description_elem.fill(prompt)
                                print(f"   ✅ Prompt saisi")
                                break
                    
                    if description_elem:
                        break
                except Exception as e:
                    continue
            
            if not description_elem:
                print("   ⚠️  Champ description non trouvé, essai avec JavaScript...")
                # Injection directe via JavaScript
                await page.evaluate(f"""
                    () => {{
                        const textareas = document.querySelectorAll('textarea');
                        for (const ta of textareas) {{
                            if (ta.offsetParent !== null) {{
                                ta.value = `{prompt}`;
                                ta.dispatchEvent(new Event('input', {{ bubbles: true }}));
                                return true;
                            }}
                        }}
                        return false;
                    }}
                """)
                print("   ✅ Prompt injecté via JavaScript")
            
            await asyncio.sleep(2)
            
            # Configurer le nombre d'images
            print(f"🔢 Configuration: {IMAGES_PER_BATCH} images...")
            
            # Chercher et sélectionner "9" dans le dropdown/select
            for frame in all_frames:
                try:
                    selects = await frame.query_selector_all("select")
                    for select in selects:
                        is_visible = await select.is_visible()
                        if is_visible:
                            options = await select.query_selector_all("option")
                            for opt in options:
                                value = await opt.get_attribute("value")
                                if value == "9" or value == str(IMAGES_PER_BATCH):
                                    await select.select_option(value)
                                    print(f"   ✅ Nombre configuré à {IMAGES_PER_BATCH}")
                                    break
                except Exception as e:
                    continue
            
            await asyncio.sleep(1)
            
            # Cliquer sur le bouton generate
            print("🎨 Lancement de la génération...")
            
            # Chercher le bouton avec ✨ ou "generate"
            generate_clicked = False
            for frame in all_frames:
                try:
                    # Essayer plusieurs sélecteurs
                    button = await frame.query_selector("button:has-text('✨')")
                    if not button:
                        buttons = await frame.query_selector_all("button")
                        for btn in buttons:
                            text = await btn.inner_text()
                            if "✨" in text or "generate" in text.lower():
                                button = btn
                                break
                    
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
                print("   ⚠️  Essai de clic via JavaScript...")
                await page.evaluate("""
                    () => {
                        const buttons = document.querySelectorAll('button');
                        for (const btn of buttons) {
                            if (btn.textContent.includes('✨') || btn.textContent.toLowerCase().includes('generate')) {
                                btn.click();
                                return true;
                            }
                        }
                        return false;
                    }
                """)
                generate_clicked = True
                print("   ✅ Clic via JavaScript")
            
            if not generate_clicked:
                print("   ❌ Impossible de cliquer sur generate")
                return 0
            
            # Attendre la génération
            print(f"⏳ Attente de la génération ({WAIT_TIME_GENERATION}s)...")
            await asyncio.sleep(WAIT_TIME_GENERATION)
            
            # Vérifier les erreurs
            page_content = await page.content()
            if "too many requests" in page_content.lower() or "quota" in page_content.lower():
                print("   ⛔ Crédits Perchance épuisés détectés!")
                return 0
            
            # Chercher les images générées
            print("📸 Recherche et téléchargement des images...")
            
            downloaded_count = 0
            all_images = await page.query_selector_all("img")
            
            print(f"   🔍 {len(all_images)} images trouvées sur la page")
            
            for i, img in enumerate(all_images):
                try:
                    # Vérifier si l'image est visible et assez grande
                    box = await img.bounding_box()
                    if not box or box['width'] < 100 or box['height'] < 100:
                        continue
                    
                    # Récupérer l'image via canvas
                    image_data = await img.evaluate("""
                        (img) => {
                            try {
                                const canvas = document.createElement('canvas');
                                canvas.width = img.naturalWidth || img.width;
                                canvas.height = img.naturalHeight || img.height;
                                const ctx = canvas.getContext('2d');
                                ctx.drawImage(img, 0, 0);
                                return canvas.toDataURL('image/jpeg', 0.95);
                            } catch (e) {
                                return null;
                            }
                        }
                    """)
                    
                    if image_data and image_data.startswith('data:image') and len(image_data) > 5000:
                        # Décoder l'image
                        image_bytes = base64.b64decode(image_data.split(',')[1])
                        
                        # Vérifier la taille (images IA sont généralement > 50 KB)
                        if len(image_bytes) < 50000:
                            continue
                        
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
                        print(f"   ✅ #{downloaded_count}: {filename} ({len(image_bytes) // 1024} KB)")
                        
                        if downloaded_count >= IMAGES_PER_BATCH:
                            break
                            
                except Exception as e:
                    continue
            
            print(f"\n✅ Batch terminé: {downloaded_count}/{IMAGES_PER_BATCH} images")
            return downloaded_count
            
        except Exception as e:
            error_msg = f"❌ Erreur batch #{batch_number}: {str(e)[:100]}"
            print(error_msg)
            self.errors.append(error_msg)
            return 0
            
        finally:
            await page.close()
    
    async def run(self):
        """Exécute le téléchargement en boucle jusqu'à épuisement des crédits"""
        print("\n" + "="*70)
        print("🎯 TÉLÉCHARGEMENT ILLIMITÉ - PERCHANCE AI FACE GENERATOR")
        print("🔄 Continue jusqu'à épuisement des crédits")
        print("="*70)
        print(f"📁 Cible: {self.target_dir}")
        print(f"🎭 Âges: {', '.join(map(str, AGES))} ans (rotation)")
        print(f"📊 Par batch: {IMAGES_PER_BATCH} images")
        print(f"⛔ Arrêt après {MAX_CONSECUTIVE_FAILURES} échecs consécutifs")
        print("="*70 + "\n")
        
        self.target_dir.mkdir(parents=True, exist_ok=True)
        await self.setup_browser()
        
        batch_number = 0
        consecutive_failures = 0
        
        try:
            while True:
                age = AGES[batch_number % len(AGES)]
                batch_number += 1
                
                print(f"\n{'🔄 '*35}")
                print(f"BATCH #{batch_number} | Âge: {age} ans | Total: {self.total_downloaded} images")
                print(f"{'🔄 '*35}")
                
                downloaded = await self.download_batch(age, batch_number)
                
                if downloaded == 0:
                    consecutive_failures += 1
                    print(f"\n⚠️  Échec #{consecutive_failures}/{MAX_CONSECUTIVE_FAILURES}")
                    
                    if consecutive_failures >= MAX_CONSECUTIVE_FAILURES:
                        print(f"\n🛑 ARRÊT: {MAX_CONSECUTIVE_FAILURES} échecs consécutifs")
                        print("   → Crédits Perchance probablement épuisés")
                        break
                else:
                    consecutive_failures = 0
                
                print(f"\n⏸️  Pause 5s...")
                await asyncio.sleep(5)
            
            # Résumé
            print("\n" + "="*70)
            print("📊 RÉSUMÉ FINAL")
            print("="*70)
            print(f"🔢 Batches traités: {batch_number}")
            print(f"✅ Images téléchargées: {self.total_downloaded}")
            print(f"📈 Moyenne/batch: {self.total_downloaded / max(batch_number - consecutive_failures, 1):.1f}")
            
            files = list(self.target_dir.glob("perchance_*.jpg"))
            print(f"📂 Fichiers Perchance: {len(files)}")
            
            print("\n🎉 TERMINÉ - CRÉDITS ÉPUISÉS!")
            print("="*70 + "\n")
            
        except KeyboardInterrupt:
            print(f"\n\n⚠️  Arrêt manuel ({self.total_downloaded} images)")
            raise
            
        finally:
            await self.close_browser()


async def main():
    downloader = PerchancePortraitDownloader()
    await downloader.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Au revoir!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erreur fatale: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
