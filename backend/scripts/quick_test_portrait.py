"""
Test rapide - génère un seul calque pour vérifier que le système fonctionne
"""
import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from services.portrait_generator_service import PortraitGeneratorService
from dotenv import load_dotenv

load_dotenv()


async def quick_test():
    service = PortraitGeneratorService()
    
    print("\n🧪 TEST RAPIDE - Génération d'un seul calque")
    print("=" * 70)
    
    print("\n📝 Génération d'un calque 'base' pour tester l'API...")
    
    try:
        layers = await service.generate_portrait_layers_set(
            nationality="Français",
            gender="male",
            age=25,
            set_id=1,
            layer_types=['base']  # Un seul calque pour test rapide
        )
        
        print(f"✅ Calque généré avec succès!")
        print(f"   Chemin : {layers.get('base', 'N/A')}")
        
        # Vérifier que le fichier existe
        if 'base' in layers:
            import os
            full_path = f"/app/backend{layers['base']}"
            if os.path.exists(full_path):
                size = os.path.getsize(full_path)
                print(f"   Fichier existe : {size} bytes")
                print("\n✨ Le système de génération d'images fonctionne!")
            else:
                print(f"   ⚠️  Fichier non trouvé : {full_path}")
        else:
            print("   ⚠️  Pas de calque 'base' retourné")
    
    except Exception as e:
        print(f"❌ Erreur : {str(e)}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    asyncio.run(quick_test())
