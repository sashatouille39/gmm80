"""
Script de génération de bibliothèque de calques de portraits
Génère des centaines de calques individuels (base, yeux, cheveux, bouche, nez)
qui seront assemblés aléatoirement pour créer des milliers de combinaisons uniques
"""
import asyncio
import sys
import os
from pathlib import Path

# Ajouter le chemin parent pour l'import
sys.path.append(str(Path(__file__).parent.parent))

from services.portrait_generator_service import PortraitGeneratorService
from dotenv import load_dotenv

load_dotenv()


async def generate_library():
    """Génère une bibliothèque complète de calques variés"""
    
    service = PortraitGeneratorService()
    
    print("🎨 Génération de la bibliothèque de calques de portraits...")
    print("=" * 70)
    
    # Configuration : nombre de variations par type de calque
    # Plus de cheveux pour avoir beaucoup de coupes différentes
    CALQUES_CONFIG = {
        'base': 40,      # 40 bases par région/sexe (différentes formes de visage/teintes)
        'eyes': 30,      # 30 types d'yeux (différentes formes/couleurs)
        'hair': 100,     # 100 coupes de cheveux variées (le plus important pour la diversité)
        'mouth': 25,     # 25 bouches
        'nose': 25       # 25 nez
    }
    
    # Régions principales à couvrir
    REGIONS = [
        'nordic', 'western_european', 'mediterranean', 'eastern_european',
        'east_asian', 'south_asian', 'southeast_asian',
        'middle_eastern', 'north_african', 'african', 'latino', 'mixed'
    ]
    
    GENDERS = ['male', 'female']
    
    total_generated = 0
    total_to_generate = len(REGIONS) * len(GENDERS) * sum(CALQUES_CONFIG.values())
    
    print(f"📊 Configuration :")
    print(f"   - Régions : {len(REGIONS)}")
    print(f"   - Genres : {len(GENDERS)}")
    print(f"   - Calques par type : {CALQUES_CONFIG}")
    print(f"   - Total à générer : ~{total_to_generate} calques")
    print()
    
    for region in REGIONS:
        print(f"\n🌍 Région : {region.upper()}")
        print("-" * 70)
        
        for gender in GENDERS:
            gender_label = "Homme" if gender == 'male' else "Femme"
            print(f"\n  👤 {gender_label}")
            
            # Générer chaque type de calque
            for layer_type, count in CALQUES_CONFIG.items():
                print(f"    🎭 Génération de {count} calques '{layer_type}'... ", end='', flush=True)
                
                success_count = 0
                for variation_id in range(1, count + 1):
                    try:
                        # Générer un seul type de calque
                        layers = await service.generate_portrait_layers_set(
                            nationality=service.get_nationality_for_region(region),
                            gender=gender,
                            age=25,
                            set_id=variation_id,
                            layer_types=[layer_type]  # Générer uniquement ce type
                        )
                        
                        if layers and layer_type in layers:
                            success_count += 1
                            total_generated += 1
                            
                            # Afficher progression
                            if variation_id % 10 == 0:
                                print(f"{variation_id}...", end='', flush=True)
                    
                    except Exception as e:
                        print(f"\n    ❌ Erreur variation {variation_id}: {str(e)}")
                        continue
                
                print(f" ✅ {success_count}/{count} générés")
    
    print("\n" + "=" * 70)
    print(f"✨ Génération terminée ! {total_generated} calques générés")
    print("=" * 70)


# Méthode helper pour obtenir une nationalité exemple par région
def get_nationality_for_region(service, region):
    """Retourne une nationalité exemple pour une région"""
    region_to_nationality = {
        'nordic': 'Suédois',
        'western_european': 'Français',
        'mediterranean': 'Italien',
        'eastern_european': 'Russe',
        'east_asian': 'Japonais',
        'south_asian': 'Indien',
        'southeast_asian': 'Thaïlandais',
        'middle_eastern': 'Turc',
        'north_african': 'Marocain',
        'african': 'Nigérian',
        'latino': 'Mexicain',
        'mixed': 'Américain'
    }
    return region_to_nationality.get(region, 'Américain')


# Ajouter la méthode au service
PortraitGeneratorService.get_nationality_for_region = lambda self, region: get_nationality_for_region(self, region)


if __name__ == "__main__":
    print("\n" + "🎨" * 35)
    print("  GÉNÉRATEUR DE BIBLIOTHÈQUE DE PORTRAITS PAR CALQUES")
    print("🎨" * 35 + "\n")
    
    try:
        asyncio.run(generate_library())
    except KeyboardInterrupt:
        print("\n\n⚠️  Génération interrompue par l'utilisateur")
    except Exception as e:
        print(f"\n\n❌ Erreur fatale : {str(e)}")
        import traceback
        traceback.print_exc()
