"""
Script pour générer un échantillon de calques de test
Génère quelques calques pour voir le système en action dans le jeu
"""
import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from services.portrait_generator_service import PortraitGeneratorService
from dotenv import load_dotenv

load_dotenv()


async def generate_sample_library():
    """Génère un échantillon de calques pour tester"""
    
    service = PortraitGeneratorService()
    
    print("\n🎨 GÉNÉRATION D'ÉCHANTILLON DE CALQUES POUR TEST")
    print("=" * 70)
    print("⚡ Mode rapide : génère seulement quelques calques par région")
    print()
    
    # Quelques nationalités principales pour test
    test_nationalities = [
        ('Français', 'male', 'western_european'),
        ('Français', 'female', 'western_european'),
        ('Japonais', 'male', 'east_asian'),
        ('Japonais', 'female', 'east_asian'),
        ('Nigérian', 'male', 'african'),
        ('Nigérian', 'female', 'african'),
    ]
    
    # Générer 3 variations de chaque type de calque par nationalité/genre
    VARIATIONS = 3
    LAYER_TYPES = ['base', 'eyes', 'hair', 'mouth', 'nose']
    
    total_generated = 0
    
    for nationality, gender, region in test_nationalities:
        gender_label = "Homme" if gender == 'male' else "Femme"
        print(f"\n🌍 {nationality} - {gender_label} (région: {region})")
        print("-" * 70)
        
        for layer_type in LAYER_TYPES:
            print(f"  🎭 Génération {VARIATIONS} calques '{layer_type}'... ", end='', flush=True)
            
            success_count = 0
            for i in range(1, VARIATIONS + 1):
                try:
                    layers = await service.generate_portrait_layers_set(
                        nationality=nationality,
                        gender=gender,
                        age=25,
                        set_id=i,
                        layer_types=[layer_type]
                    )
                    
                    if layers and layer_type in layers:
                        success_count += 1
                        total_generated += 1
                
                except Exception as e:
                    print(f"\n  ❌ Erreur variation {i}: {str(e)}")
                    continue
            
            print(f"✅ {success_count}/{VARIATIONS}")
    
    print("\n" + "=" * 70)
    print(f"✨ Échantillon généré ! {total_generated} calques créés")
    print(f"💡 Le système va maintenant assembler ces calques aléatoirement")
    print("=" * 70)


if __name__ == "__main__":
    print("\n" + "🎨" * 35)
    print("  GÉNÉRATEUR D'ÉCHANTILLON DE CALQUES DE TEST")
    print("🎨" * 35 + "\n")
    
    try:
        asyncio.run(generate_sample_library())
    except KeyboardInterrupt:
        print("\n\n⚠️  Génération interrompue par l'utilisateur")
    except Exception as e:
        print(f"\n\n❌ Erreur fatale : {str(e)}")
        import traceback
        traceback.print_exc()
