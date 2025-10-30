"""
Générateur de portraits réalistes avec gpt-image-1
Génère 1200 portraits par continent jusqu'à épuisement du crédit (garder 0.50)
"""
import os
import time
import base64
import asyncio
from pathlib import Path
from typing import Dict, List
from emergentintegrations.llm.openai.image_generation import OpenAIImageGeneration
from dotenv import load_dotenv

load_dotenv()


class AIPortraitGenerator:
    """Génère des portraits réalistes avec gpt-image-1"""
    
    # Configuration des continents et leurs caractéristiques ethniques
    CONTINENT_CONFIGS = {
        'africa': {
            'name': 'Afrique',
            'ethnicities': [
                'African',
                'Sub-Saharan African',
                'West African',
                'East African',
                'North African'
            ],
            'skin_tones': ['dark brown', 'deep brown', 'rich brown', 'ebony'],
        },
        'asia': {
            'name': 'Asie',
            'ethnicities': [
                'East Asian',
                'Southeast Asian',
                'South Asian',
                'Chinese',
                'Japanese',
                'Korean',
                'Vietnamese',
                'Thai',
                'Indian'
            ],
            'skin_tones': ['light', 'fair', 'tan', 'olive', 'brown'],
        },
        'europe': {
            'name': 'Europe',
            'ethnicities': [
                'European',
                'Caucasian',
                'Northern European',
                'Southern European',
                'Mediterranean'
            ],
            'skin_tones': ['pale', 'fair', 'light', 'olive', 'tan'],
        },
        'north_america': {
            'name': 'Amérique du Nord',
            'ethnicities': [
                'North American',
                'Caucasian',
                'Latino',
                'Hispanic',
                'Mixed ethnicity'
            ],
            'skin_tones': ['fair', 'light', 'tan', 'olive', 'brown'],
        },
        'south_america': {
            'name': 'Amérique du Sud',
            'ethnicities': [
                'Latino',
                'Hispanic',
                'South American',
                'Brazilian',
                'Mixed ethnicity'
            ],
            'skin_tones': ['tan', 'olive', 'light brown', 'bronze'],
        },
        'oceania': {
            'name': 'Océanie',
            'ethnicities': [
                'Pacific Islander',
                'Polynesian',
                'Aboriginal Australian',
                'Maori',
                'Mixed Asian-European'
            ],
            'skin_tones': ['tan', 'olive', 'brown', 'fair'],
        }
    }
    
    GENDERS = ['male', 'female']
    TARGET_PER_GENDER = 600  # 600 hommes + 600 femmes = 1200 par continent
    MIN_CREDIT_RESERVE = 0.50  # Garder 0.50 de crédit
    
    def __init__(self, api_key: str, base_path: str = "/app/backend/static/portraits"):
        self.api_key = api_key
        self.base_path = Path(base_path)
        self.image_generator = OpenAIImageGeneration(api_key=api_key)
        self.total_generated = 0
        self.failed_count = 0
        
        # Créer la structure de dossiers
        self.create_directory_structure()
    
    def create_directory_structure(self):
        """Crée la structure de dossiers pour tous les continents"""
        print("\n📁 Création de la structure de dossiers...")
        for continent in self.CONTINENT_CONFIGS.keys():
            for gender in self.GENDERS:
                dir_path = self.base_path / continent / gender
                dir_path.mkdir(parents=True, exist_ok=True)
                print(f"   ✓ {dir_path}")
    
    def build_prompt(self, continent: str, gender: str, index: int) -> str:
        """Construit le prompt pour générer un portrait"""
        config = self.CONTINENT_CONFIGS[continent]
        
        # Sélectionner aléatoirement une ethnicité et un teint
        import random
        ethnicity = random.choice(config['ethnicities'])
        skin_tone = random.choice(config['skin_tones'])
        
        # Âge entre 20 et 50 ans
        age = random.randint(20, 50)
        
        # Construire le prompt
        gender_term = "man" if gender == "male" else "woman"
        
        prompt = f"""A highly detailed, semi-realistic portrait photograph of a {age}-year-old {ethnicity} {gender_term}.
Face features: {skin_tone} skin tone, natural facial features typical of {ethnicity} descent.
Photography: Professional headshot, neutral expression, soft studio lighting, clean background.
Style: Semi-realistic, detailed facial features, natural skin texture, photographic quality.
Composition: Head and shoulders portrait, centered, facing camera, high resolution.
Quality: Sharp focus, professional photography, natural colors, realistic rendering."""
        
        return prompt
    
    async def generate_single_portrait(self, continent: str, gender: str, index: int) -> bool:
        """Génère un seul portrait"""
        save_dir = self.base_path / continent / gender
        save_path = save_dir / f"portrait_{index:04d}.png"
        
        # Si le fichier existe déjà, passer
        if save_path.exists():
            return True
        
        try:
            # Construire le prompt
            prompt = self.build_prompt(continent, gender, index)
            
            # Générer l'image avec gpt-image-1
            print(f"      Génération via gpt-image-1...", end='', flush=True)
            
            result = await asyncio.to_thread(
                self.image_generator.generate_images,
                prompt=prompt,
                model="gpt-image-1",
                number_of_images=1,
                quality="low"  # low pour économiser le crédit
            )
            
            # result est une liste de bytes
            if result and len(result) > 0:
                image_bytes = result[0]
                with open(save_path, 'wb') as f:
                    f.write(image_bytes)
                print(" ✓", flush=True)
                return True
            else:
                print(" ✗ (pas de données)", flush=True)
                return False
            
        except Exception as e:
            error_msg = str(e)
            if 'insufficient_quota' in error_msg or 'quota' in error_msg.lower():
                print(f" ✗ QUOTA ÉPUISÉ", flush=True)
                return False
            print(f" ✗ ({error_msg[:50]})", flush=True)
            return False
    
    async def generate_portraits_for_continent(self, continent: str, gender: str):
        """Génère tous les portraits pour un continent et un genre"""
        continent_name = self.CONTINENT_CONFIGS[continent]['name']
        
        print(f"\n🌍 {continent_name} - {gender.upper()}")
        print(f"   Objectif: {self.TARGET_PER_GENDER} portraits")
        print(f"   " + "=" * 70)
        
        save_dir = self.base_path / continent / gender
        
        # Compter les images existantes
        existing = len(list(save_dir.glob("portrait_*.png")))
        print(f"   ℹ️ {existing} portraits déjà générés")
        
        generated = existing
        consecutive_failures = 0
        max_consecutive_failures = 3
        
        for i in range(existing + 1, self.TARGET_PER_GENDER + 1):
            print(f"\n   [{i}/{self.TARGET_PER_GENDER}] Portrait #{i:04d}")
            
            success = await self.generate_single_portrait(continent, gender, i)
            
            if success:
                generated += 1
                consecutive_failures = 0
                self.total_generated += 1
                
                # Pause pour ne pas surcharger l'API
                await asyncio.sleep(1)
            else:
                consecutive_failures += 1
                self.failed_count += 1
                
                if consecutive_failures >= max_consecutive_failures:
                    print(f"\n   ⛔ {consecutive_failures} échecs consécutifs")
                    print(f"   💡 Crédit probablement épuisé ou problème API")
                    return False
                
                await asyncio.sleep(3)
        
        print(f"\n   ✅ Terminé: {generated}/{self.TARGET_PER_GENDER} portraits")
        return True
    
    async def generate_all_portraits(self):
        """Génère tous les portraits pour tous les continents"""
        print("=" * 80)
        print("🎨 GÉNÉRATION DE PORTRAITS RÉALISTES PAR IA")
        print("=" * 80)
        print(f"\n🤖 Modèle: gpt-image-1 (OpenAI)")
        print(f"📁 Destination: {self.base_path}")
        print(f"🎯 Objectif: 1200 portraits par continent (600M + 600F)")
        print(f"💰 Arrêt: Quand crédit ≤ {self.MIN_CREDIT_RESERVE}")
        print("\n" + "=" * 80)
        
        start_time = time.time()
        
        try:
            # Générer pour chaque continent et genre
            for continent, config in self.CONTINENT_CONFIGS.items():
                for gender in self.GENDERS:
                    success = await self.generate_portraits_for_continent(continent, gender)
                    
                    if not success:
                        print(f"\n⚠️ Arrêt pour {config['name']} - {gender}")
                        print("   Raison probable: Crédit épuisé")
                        raise Exception("Crédit épuisé")
                    
                    # Petite pause entre les catégories
                    print(f"\n   ⏸️ Pause de 5 secondes...")
                    await asyncio.sleep(5)
        
        except Exception as e:
            print(f"\n⚠️ Génération interrompue: {e}")
        
        # Statistiques finales
        elapsed = time.time() - start_time
        
        print("\n" + "=" * 80)
        print("📊 STATISTIQUES FINALES")
        print("=" * 80)
        
        # Compter les images générées par continent
        total_images = 0
        for continent, config in self.CONTINENT_CONFIGS.items():
            male_count = len(list((self.base_path / continent / 'male').glob("portrait_*.png")))
            female_count = len(list((self.base_path / continent / 'female').glob("portrait_*.png")))
            continent_total = male_count + female_count
            total_images += continent_total
            
            status = "✅" if continent_total >= 1200 else "⏸️"
            print(f"   {status} {config['name']:20} : {continent_total:4} / 1200 ({male_count:4}M, {female_count:4}F)")
        
        print("\n" + "-" * 80)
        print(f"   📊 TOTAL: {total_images} portraits générés")
        print(f"   ⏱️ Temps: {elapsed/60:.1f} minutes")
        print(f"   ⚡ Moyenne: {elapsed/total_images if total_images > 0 else 0:.1f}s par portrait")
        print(f"   ✗ Échecs: {self.failed_count}")
        
        target_total = 7200
        if total_images >= target_total:
            print(f"\n🎉 OBJECTIF ATTEINT : {target_total} portraits générés !")
        else:
            missing = target_total - total_images
            print(f"\n⏸️ Génération arrêtée à {total_images}/{target_total} portraits")
            print(f"   💰 Crédit probablement épuisé (réservé: {self.MIN_CREDIT_RESERVE})")
        
        print("\n📁 Les portraits sont disponibles dans:")
        print(f"   {self.base_path}")
        print("=" * 80)


async def main():
    """Point d'entrée principal"""
    print("\n🚀 GÉNÉRATEUR DE PORTRAITS RÉALISTES PAR IA\n")
    
    # Récupérer la clé API
    api_key = os.getenv('EMERGENT_LLM_KEY', 'sk-emergent-376483c6134A69bAb0')
    
    if not api_key:
        print("❌ Erreur: Clé EMERGENT_LLM_KEY non trouvée")
        print("   Ajoutez-la dans le fichier .env")
        return
    
    print(f"✅ Clé API chargée")
    print(f"🎨 Modèle: gpt-image-1")
    print(f"⏰ Génération jusqu'à épuisement du crédit (garde 0.50)\n")
    
    generator = AIPortraitGenerator(api_key=api_key)
    await generator.generate_all_portraits()


if __name__ == "__main__":
    asyncio.run(main())
