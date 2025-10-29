#!/usr/bin/env python3
"""
Génère uniquement le fichier hair_male_71 manquant
"""
import os
import sys
import asyncio
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from services.portrait_generator_service import PortraitGeneratorService

async def main():
    print("🔧 Génération du fichier manquant hair_male_71.png")
    
    service = PortraitGeneratorService()
    
    # Style et couleur pour index 71
    styles = ["crew cut", "buzz cut", "undercut", "slicked back", "pompadour",
              "quiff", "side part", "textured crop", "messy", "wavy short",
              "spiky", "mohawk", "faux hawk", "long straight", "man bun",
              "dreadlocks", "afro", "curly short", "taper fade", "bald with beard shadow",
              "Caesar cut"]  # Index 70 (71-1 % 21 = 70 % 21 = 7)
    
    colors = ["black", "dark brown", "light brown", "blonde", "red", 
              "auburn", "gray", "white", "silver", "platinum"]
    
    idx = 71
    style_idx = (idx - 1) % len(styles)
    color_idx = (idx - 1) % len(colors)
    style = styles[style_idx]
    color = colors[color_idx]
    
    print(f"Style: {style}")
    print(f"Color: {color}")
    
    prompt = f"Professional isolated layer for portrait, male aged 20-40, {style} {color} hair hairstyle only. "
    prompt += f"""
Technical specifications for hair layer:
- Style: {style}
- Color: {color}
- Gender: male
- Hair only, NO face, NO skin, NO forehead, NO ears
- Positioned naturally on a head (top portion)
- Natural hair texture with individual strands visible
- Professional studio quality
- High detail and realistic appearance
- Background: Completely transparent (PNG with alpha channel)
- Format: Clean hair silhouette ready for layering
- Resolution: High quality, suitable for portrait composition"""
    
    try:
        print("\n🎨 Génération en cours...")
        images = await service.image_gen.generate_images(
            prompt=prompt,
            model="gpt-image-1",
            number_of_images=1
        )
        
        if images and len(images) > 0:
            filepath = os.path.join(service.base_path, "hair_male", f"hair_male_{idx}.png")
            with open(filepath, 'wb') as f:
                f.write(images[0])
            print(f"✅ Fichier créé: {filepath}")
            print(f"📊 Taille: {len(images[0]) / 1024 / 1024:.1f} MB")
        else:
            print("❌ Aucune image générée")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    asyncio.run(main())
