"""
Test de génération d'un calque d'yeux pour déboguer
"""
import asyncio
import sys
import os
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from services.portrait_generator_service import PortraitGeneratorService
from dotenv import load_dotenv

load_dotenv()


async def test_eyes_generation():
    """Test de génération d'un calque yeux"""
    
    print("\n🧪 TEST DE GÉNÉRATION D'UN CALQUE YEUX")
    print("=" * 70)
    
    service = PortraitGeneratorService()
    
    try:
        print("\n🎨 Génération d'yeux européens marron...")
        
        prompt = """Create semi-realistic human eyes for a character portrait.
Style: Semi-realistic, detailed, professional illustration
Eye type: European/American - almond-shaped, medium size, visible eyelid crease
Eye color: brown iris (#5C3317)
View: Front view, both eyes, looking straight ahead
Background: Completely transparent (alpha channel)
Include: Both eyes with iris, pupils, eyelids, natural eyelashes
Exclude: Eyebrows, face, nose, other facial features
Quality: High detail with realistic iris texture
Expression: Neutral, friendly
Format: PNG with transparency"""

        images = await service.image_gen.generate_images(
            prompt=prompt,
            model="gpt-image-1",
            number_of_images=1
        )
        
        if images and len(images) > 0:
            print(f"✅ Yeux générés! Taille: {len(images[0])} bytes")
            
            # Sauvegarder
            test_path = "/app/backend/static/portraits/eyes/test_eyes_european_brown.png"
            os.makedirs(os.path.dirname(test_path), exist_ok=True)
            
            with open(test_path, 'wb') as f:
                f.write(images[0])
            
            print(f"✅ Image sauvegardée: {test_path}")
            print("\n🎉 TEST RÉUSSI!")
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
    asyncio.run(test_eyes_generation())
