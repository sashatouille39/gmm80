#!/usr/bin/env python3
"""
Script d'automatisation pour télécharger des portraits depuis Perchance AI Face Generator
Pour des hommes asiatiques de l'est de différents âges (20, 30, 40 ans)

Le script :
1. Va sur https://perchance.org/ai-face-generator
2. Entre le prompt avec variations d'âge
3. Génère 9 photos par batch
4. Télécharge toutes les photos
5. Les sauvegarde dans backend/static/realistic_portraits/asia/asian/M
"""

import asyncio
import os
import time
from pathlib import Path
from playwright.async_api import async_playwright
import sys

# Configuration
TARGET_DIR = Path("/app/backend/static/realistic_portraits/asia/asian/M")
PERCHANCE_URL = "https://perchance.org/ai-face-generator"
AGES = [20, 30, 40]
IMAGES_PER_BATCH = 9
TOTAL_BATCHES = 3  # Un batch par âge

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
            headless=False,  # Mode visible pour déboguer
            args=['--no-sandbox', '--disable-setuid-sandbox']
        )
        self.context = await self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            accept_downloads=True
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
        print(f"📥 Téléchargement du batch {batch_number} pour l'âge {age} ans")
        print(f"{'='*60}")
        
        page = await self.context.new_page()
        
        try:
            # Naviguer vers Perchance
            print(f"🌐 Navigation vers {PERCHANCE_URL}...")
            await page.goto(PERCHANCE_URL, wait_until='networkidle', timeout=60000)
            await asyncio.sleep(2)
            
            # Trouver et remplir le champ de prompt
            print(f"✍️  Saisie du prompt pour l'âge {age} ans...")
            prompt = PROMPT_TEMPLATE.format(age=age)
            
            # Chercher le textarea ou input pour le prompt
            prompt_selector = "textarea, input[type='text']"
            await page.wait_for_selector(prompt_selector, timeout=10000)
            await page.fill(prompt_selector, prompt)
            print(f"   Prompt: {prompt}")
            
            # Trouver et remplir le champ "how many" avec 9
            print(f"🔢 Configuration pour {IMAGES_PER_BATCH} images...")
            # Chercher un input numérique ou un champ avec "how many"
            number_inputs = await page.query_selector_all("input[type='number']")
            for input_elem in number_inputs:
                # Vérifier si c'est le bon champ (probablement le premier)
                await input_elem.fill(str(IMAGES_PER_BATCH))
                await asyncio.sleep(0.5)
                break
            
            # Cliquer sur le bouton de génération
            print("🎨 Lancement de la génération...")
            generate_buttons = await page.query_selector_all("button, input[type='submit']")
            for button in generate_buttons:
                button_text = await button.inner_text()
                if button_text and any(word in button_text.lower() for word in ['generate', 'create', 'make', 'go']):
                    await button.click()
                    print(f"   Cliqué sur: {button_text}")
                    break
            
            # Attendre que les images soient générées
            print("⏳ Attente de la génération des images (peut prendre 30-60 secondes)...")
            await asyncio.sleep(60)  # Temps généreux pour la génération
            
            # Chercher toutes les images générées
            print("🔍 Recherche des images générées...")
            images = await page.query_selector_all("img")
            downloaded_count = 0
            
            for i, img in enumerate(images):
                try:
                    # Récupérer l'URL de l'image
                    img_src = await img.get_attribute('src')
                    if not img_src or img_src.startswith('data:') or 'icon' in img_src.lower():
                        continue
                    
                    # Télécharger l'image
                    print(f"   📸 Téléchargement de l'image {i+1}...")
                    
                    if img_src.startswith('//'):
                        img_src = 'https:' + img_src
                    elif img_src.startswith('/'):
                        img_src = PERCHANCE_URL + img_src
                    
                    # Télécharger avec fetch
                    image_data = await page.evaluate(f"""
                        async () => {{
                            const response = await fetch('{img_src}');
                            const blob = await response.blob();
                            return new Promise((resolve) => {{
                                const reader = new FileReader();
                                reader.onloadend = () => resolve(reader.result);
                                reader.readAsDataURL(blob);
                            }});
                        }}
                    """)
                    
                    # Sauvegarder l'image
                    if image_data and image_data.startswith('data:image'):
                        import base64
                        # Extraire les données de l'image
                        image_bytes = base64.b64decode(image_data.split(',')[1])
                        
                        # Générer le nom de fichier
                        existing_files = list(self.target_dir.glob(f"asia_asian_M_{age}_*.jpg"))
                        next_num = len(existing_files) + 1
                        filename = f"asia_asian_M_{age}_{next_num:04d}.jpg"
                        filepath = self.target_dir / filename
                        
                        # Sauvegarder
                        with open(filepath, 'wb') as f:
                            f.write(image_bytes)
                        
                        downloaded_count += 1
                        self.total_downloaded += 1
                        print(f"   ✅ Sauvegardé: {filename}")
                        
                        if downloaded_count >= IMAGES_PER_BATCH:
                            break
                            
                except Exception as e:
                    print(f"   ⚠️  Erreur lors du téléchargement de l'image {i+1}: {e}")
                    continue
            
            print(f"✅ Batch terminé: {downloaded_count} images téléchargées")
            return downloaded_count
            
        except Exception as e:
            error_msg = f"❌ Erreur lors du batch {batch_number} (âge {age}): {e}"
            print(error_msg)
            self.errors.append(error_msg)
            return 0
            
        finally:
            await page.close()
    
    async def run(self):
        """Exécute le téléchargement complet"""
        print("\n" + "="*60)
        print("🎯 DÉBUT DU TÉLÉCHARGEMENT DES PORTRAITS PERCHANCE")
        print("="*60)
        print(f"📁 Dossier cible: {self.target_dir}")
        print(f"🎭 Âges à générer: {AGES}")
        print(f"📊 Images par batch: {IMAGES_PER_BATCH}")
        print(f"📦 Total de batches: {TOTAL_BATCHES}")
        print("="*60 + "\n")
        
        # Créer le dossier si nécessaire
        self.target_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialiser le navigateur
        await self.setup_browser()
        
        try:
            # Télécharger pour chaque âge
            for batch_num, age in enumerate(AGES, 1):
                downloaded = await self.download_batch(age, batch_num)
                
                # Pause entre les batches
                if batch_num < len(AGES):
                    print(f"\n⏸️  Pause de 5 secondes avant le prochain batch...")
                    await asyncio.sleep(5)
            
            # Résumé final
            print("\n" + "="*60)
            print("📊 RÉSUMÉ FINAL")
            print("="*60)
            print(f"✅ Total d'images téléchargées: {self.total_downloaded}")
            print(f"❌ Erreurs rencontrées: {len(self.errors)}")
            
            if self.errors:
                print("\n⚠️  Liste des erreurs:")
                for error in self.errors:
                    print(f"   - {error}")
            
            print("\n🎉 TÉLÉCHARGEMENT TERMINÉ!")
            print("="*60 + "\n")
            
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
        sys.exit(1)
