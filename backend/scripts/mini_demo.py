"""
Mini-test : génère 1 portrait complet pour démonstration rapide
"""
import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from services.portrait_generator_service import PortraitGeneratorService
from dotenv import load_dotenv

load_dotenv()


async def mini_demo():
    service = PortraitGeneratorService()
    
    print("\n🎨 GÉNÉRATION MINI-DÉMO : 1 portrait complet")
    print("=" * 70)
    
    try:
        print("\n📝 Génération d'un portrait complet (Français, homme)...")
        
        layers = await service.generate_portrait_layers_set(
            nationality="Français",
            gender="male",
            age=25,
            set_id=1,
            layer_types=['base', 'eyes', 'hair', 'mouth', 'nose']
        )
        
        print(f"\n✅ Portrait généré avec succès !")
        print(f"\nCalques créés :")
        for layer_type, path in layers.items():
            print(f"   - {layer_type:10s}: {path}")
        
        # Tester l'assemblage
        print(f"\n🔀 Test d'assemblage aléatoire...")
        assembled = service.assemble_random_layers('western_european', 'male')
        
        if assembled:
            print(f"✅ Assemblage réussi : {len(assembled)} calques")
            for layer_type, path in assembled.items():
                print(f"   - {layer_type:10s}: ...{path[-50:]}")
        else:
            print("⚠️  Aucun calque trouvé pour assemblage")
        
        print("\n✨ Le système est maintenant prêt !")
        print("💡 Les joueurs générés dans le jeu auront des portraits par calques")
        
    except Exception as e:
        print(f"\n❌ Erreur : {str(e)}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    asyncio.run(mini_demo())
