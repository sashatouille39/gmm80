#!/usr/bin/env python3
"""
Script de génération UNIQUEMENT des cheveux FEMME
À lancer manuellement après les cheveux homme
"""
import os
import sys
import time
import asyncio
from pathlib import Path

# Ajouter le répertoire parent au PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent.parent))

from services.portrait_generator_service import PortraitGeneratorService

# Styles de cheveux pour femmes
HAIR_STYLES_FEMALE = [
    "long straight", "long wavy", "long curly", "shoulder length straight", "shoulder length wavy",
    "shoulder length curly", "pixie cut", "bob cut", "lob", "shag",
    "layers", "bangs with long hair", "side swept", "center part", "deep side part",
    "ponytail high", "ponytail low", "messy bun", "sleek bun", "braided crown",
    "french braid", "fishtail braid", "Dutch braids", "space buns", "half-up half-down",
    "beach waves", "tight curls", "loose curls", "pin curls", "vintage waves",
    "updo elegant", "bouffant", "chignon", "twist updo", "braided updo",
    "afro", "dreadlocks", "box braids", "cornrows", "bantu knots",
    "asymmetrical bob", "blunt cut", "feathered", "choppy layers", "curtain bangs",
    "wispy bangs", "micro bangs", "side bangs", "grown out bangs", "no bangs sleek"
]

HAIR_COLORS = ["black", "dark brown", "light brown", "blonde", "red", "auburn", "gray", "white", "silver", "platinum"]

async def generate_hair_female(service, start_index: int = 1, target_count: int = 100):
    """Génère les variations de cheveux pour femmes"""
    folder = "hair_female"
    
    count_to_generate = target_count - start_index + 1
    
    print(f"\n{'='*60}")
    print(f"GÉNÉRATION CHEVEUX FEMME")
    print(f"Indices: {start_index} à {target_count} ({count_to_generate} images)")
    print(f"{'='*60}\n")
    
    generated = 0
    failed = 0
    
    for i in range(start_index, target_count + 1):
        # Sélection du style et couleur (cyclique sur les listes)
        style_idx = (i - 1) % len(HAIR_STYLES_FEMALE)
        color_idx = (i - 1) % len(HAIR_COLORS)
        style = HAIR_STYLES_FEMALE[style_idx]
        color = HAIR_COLORS[color_idx]
        
        # Construire le prompt
        prompt = f"Professional isolated layer for portrait, female aged 18-35, {style} {color} hair hairstyle only. "
        prompt += f"""
Technical specifications for hair layer:
- Style: {style}
- Color: {color}
- Gender: female
- Hair only, NO face, NO skin, NO forehead, NO ears
- Positioned naturally on a head (top portion)
- Natural hair texture with individual strands visible
- Feminine styling and volume
- Professional studio quality
- High detail and realistic appearance
- Background: Completely transparent (PNG with alpha channel)
- Format: Clean hair silhouette ready for layering
- Resolution: High quality, suitable for portrait composition"""
        
        filename = f"hair_female_{i}.png"
        current = i - start_index + 1
        
        try:
            print(f"[{i}/{target_count}] Génération: {style} {color}...", end=" ", flush=True)
            start = time.time()
            
            # Générer l'image (méthode async)
            images = await service.image_gen.generate_images(
                prompt=prompt,
                model="gpt-image-1",
                number_of_images=1
            )
            
            if images and len(images) > 0:
                # Sauvegarder l'image
                filepath = os.path.join(service.base_path, folder, filename)
                with open(filepath, 'wb') as f:
                    f.write(images[0])
                
                elapsed = time.time() - start
                generated += 1
                print(f"✅ ({elapsed:.1f}s)")
            else:
                failed += 1
                print(f"❌ Aucune image")
                
        except Exception as e:
            failed += 1
            print(f"❌ Erreur: {str(e)}")
            
        # Pause entre générations pour éviter rate limits
        if current % 10 == 0:
            print(f"\n⏸️  Pause 5s (progression: {generated}/{count_to_generate})...\n")
            await asyncio.sleep(5)
        else:
            await asyncio.sleep(1)
    
    return generated, failed

async def main():
    print("\n" + "="*60)
    print("GÉNÉRATION CHEVEUX FEMME UNIQUEMENT")
    print("="*60)
    
    # Initialiser le service
    service = PortraitGeneratorService()
    
    # Créer le dossier si nécessaire
    os.makedirs(os.path.join(service.base_path, "hair_female"), exist_ok=True)
    
    # Compter les fichiers existants
    hair_female_existing = len(list(Path(service.base_path, "hair_female").glob("*.png")))
    
    print(f"\nFichiers existants: {hair_female_existing}/100")
    
    if hair_female_existing >= 100:
        print("✅ Cheveux femme déjà complets!")
        return
    
    # Sauvegarder le PID
    with open('/tmp/portrait_hair_female_gen_pid.txt', 'w') as f:
        f.write(str(os.getpid()))
    
    print(f"PID: {os.getpid()}")
    print(f"Démarrage: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    start_total = time.time()
    
    # Générer cheveux femme
    female_ok, female_fail = await generate_hair_female(
        service,
        start_index=hair_female_existing + 1,
        target_count=100
    )
    
    # Résumé
    elapsed_total = time.time() - start_total
    
    print("\n" + "="*60)
    print("GÉNÉRATION TERMINÉE")
    print("="*60)
    print(f"Cheveux femme: {hair_female_existing + female_ok}/100 ({female_ok} générés, {female_fail} échecs)")
    print(f"Temps total: {elapsed_total/60:.1f} minutes")
    if female_ok > 0:
        print(f"Moyenne: {elapsed_total/female_ok:.1f}s par image")
    
    # Nettoyer le PID
    try:
        os.remove('/tmp/portrait_hair_female_gen_pid.txt')
    except:
        pass

if __name__ == "__main__":
    asyncio.run(main())
