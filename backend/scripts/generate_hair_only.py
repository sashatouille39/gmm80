#!/usr/bin/env python3
"""
Script de génération UNIQUEMENT des cheveux manquants
Ne touche PAS aux autres calques déjà générés
"""
import os
import sys
import time
import asyncio
from pathlib import Path

# Ajouter le répertoire parent au PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent.parent))

from services.portrait_generator_service import PortraitGeneratorService

# Styles de cheveux pour génération
HAIR_STYLES_MALE = [
    "crew cut", "buzz cut", "undercut", "slicked back", "pompadour",
    "quiff", "side part", "textured crop", "messy", "wavy short",
    "spiky", "mohawk", "faux hawk", "long straight", "man bun",
    "dreadlocks", "afro", "curly short", "taper fade", "bald with beard shadow",
    "Caesar cut", "Ivy League", "comb over", "French crop", "brush up",
    "shaggy", "layered medium", "swept back", "tousled", "disheveled",
    "military cut", "flat top", "high and tight", "bowl cut", "mullet",
    "surfer hair", "hipster long", "samurai topknot", "Viking braids", "cornrows",
    "short curly", "medium wavy", "long flowing", "ponytail", "half-up bun",
    "side swept bangs", "textured quiff", "messy pompadour", "slick fade", "neat side part"
]

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

async def generate_hair_variations(service, gender: str, start_index: int = 1, target_count: int = 100):
    """Génère les variations de cheveux pour un genre"""
    styles = HAIR_STYLES_MALE if gender == "male" else HAIR_STYLES_FEMALE
    folder = f"hair_{gender}"
    
    count_to_generate = target_count - start_index + 1
    
    print(f"\n{'='*60}")
    print(f"GÉNÉRATION CHEVEUX {gender.upper()}")
    print(f"Indices: {start_index} à {target_count} ({count_to_generate} images)")
    print(f"{'='*60}\n")
    
    generated = 0
    failed = 0
    
    for i in range(start_index, target_count + 1):
        # Sélection du style et couleur (cyclique sur les listes)
        style_idx = (i - 1) % len(styles)
        color_idx = (i - 1) % len(HAIR_COLORS)
        style = styles[style_idx]
        color = HAIR_COLORS[color_idx]
        
        # Construire le prompt
        age_range = "20-40" if gender == "male" else "18-35"
        prompt = f"Professional isolated layer for portrait, {gender} aged {age_range}, {style} {color} hair hairstyle only. "
        prompt += f"""
Technical specifications for hair layer:
- Style: {style}
- Color: {color}
- Gender: {gender}
- Hair only, NO face, NO skin, NO forehead, NO ears
- Positioned naturally on a head (top portion)
- Natural hair texture with individual strands visible
- Professional studio quality
- High detail and realistic appearance
- Background: Completely transparent (PNG with alpha channel)
- Format: Clean hair silhouette ready for layering
- Resolution: High quality, suitable for portrait composition"""
        
        filename = f"hair_{gender}_{i}.png"
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
    print("GÉNÉRATION CHEVEUX MANQUANTS")
    print("="*60)
    
    # Initialiser le service
    service = PortraitGeneratorService()
    
    # Créer les dossiers si nécessaire
    os.makedirs(os.path.join(service.base_path, "hair_male"), exist_ok=True)
    os.makedirs(os.path.join(service.base_path, "hair_female"), exist_ok=True)
    
    # Compter les fichiers existants
    hair_male_existing = len(list(Path(service.base_path, "hair_male").glob("*.png")))
    hair_female_existing = len(list(Path(service.base_path, "hair_female").glob("*.png")))
    
    print(f"\nFichiers existants:")
    print(f"  Homme: {hair_male_existing}/100")
    print(f"  Femme: {hair_female_existing}/100")
    
    # Sauvegarder le PID
    with open('/tmp/portrait_hair_gen_pid.txt', 'w') as f:
        f.write(str(os.getpid()))
    
    print(f"\nPID: {os.getpid()}")
    print(f"Démarrage: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    start_total = time.time()
    
    male_ok = 0
    male_fail = 0
    female_ok = 0
    female_fail = 0
    
    # Générer cheveux homme (si besoin)
    if hair_male_existing < 100:
        male_ok, male_fail = await generate_hair_variations(
            service, "male", 
            start_index=hair_male_existing + 1,
            target_count=100
        )
    else:
        print(f"\n✅ Cheveux homme déjà complets ({hair_male_existing}/100)")
    
    # Générer cheveux femme (si besoin)
    if hair_female_existing < 100:
        female_ok, female_fail = await generate_hair_variations(
            service, "female",
            start_index=hair_female_existing + 1,
            target_count=100
        )
    else:
        print(f"\n✅ Cheveux femme déjà complets ({hair_female_existing}/100)")
    
    # Résumé
    elapsed_total = time.time() - start_total
    
    print("\n" + "="*60)
    print("GÉNÉRATION TERMINÉE")
    print("="*60)
    print(f"Cheveux homme: {hair_male_existing + male_ok}/100 ({male_ok} générés, {male_fail} échecs)")
    print(f"Cheveux femme: {hair_female_existing + female_ok}/100 ({female_ok} générés, {female_fail} échecs)")
    print(f"Total généré: {male_ok + female_ok} nouvelles images")
    print(f"Temps total: {elapsed_total/60:.1f} minutes")
    if (male_ok + female_ok) > 0:
        print(f"Moyenne: {elapsed_total/(male_ok + female_ok):.1f}s par image")
    
    # Nettoyer le PID
    try:
        os.remove('/tmp/portrait_hair_gen_pid.txt')
    except:
        pass

if __name__ == "__main__":
    asyncio.run(main())
