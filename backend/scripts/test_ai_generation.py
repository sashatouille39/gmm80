"""
Test rapide pour vérifier que la génération d'images IA fonctionne
"""
import asyncio
import sys
import os
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from emergentintegrations.llm.openai.image_generation import OpenAIImageGeneration
from dotenv import load_dotenv

load_dotenv()


async def test_image_generation():
    """Test de génération d'une image IA simple"""
    
    print("\n🧪 TEST DE GÉNÉRATION D'IMAGE IA")
    print("=" * 70)
    
    api_key = os.getenv('EMERGENT_LLM_KEY')
    if not api_key or api_key == 'sk-emergent-default':
        print("❌ ERREUR: EMERGENT_LLM_KEY non configurée dans .env")
        return False
    
    print(f"✅ Clé API trouvée: {api_key[:20]}...")
    
    try:
        print("\n🎨 Génération d'une image de test...")
        print("   Prompt: 'A simple red circle on transparent background'")
        
        image_gen = OpenAIImageGeneration(api_key=api_key)
        
        images = await image_gen.generate_image(
            prompt="A simple red circle on transparent background, PNG format",
            model="gpt-image-1",
            size="1024x1024",
            quality="standard",
            number_of_images=1
        )
        
        if images and len(images) > 0:
            print(f"✅ Image générée! Taille: {len(images[0])} bytes")
            
            # Sauvegarder pour vérification
            test_path = "/app/backend/static/portraits/test_ai_image.png"
            os.makedirs(os.path.dirname(test_path), exist_ok=True)
            
            with open(test_path, 'wb') as f:
                f.write(images[0])
            
            print(f"✅ Image sauvegardée: {test_path}")
            print("\n🎉 TEST RÉUSSI! La génération d'images IA fonctionne.")
            return True
        else:
            print("❌ Aucune image générée")
            return False
            
    except Exception as e:
        print(f"\n❌ ERREUR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    try:
        success = asyncio.run(test_image_generation())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⚠️  Test interrompu")
        sys.exit(1)
