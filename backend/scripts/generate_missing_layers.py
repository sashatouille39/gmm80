"""
Script optimisé pour générer SEULEMENT les calques manquants
Inventaire actuel: 11 bases, 5 yeux, 22 cheveux, 1 bouche, 1 nez
"""
import asyncio
import sys
import os
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from services.portrait_generator_service import PortraitGeneratorService
from dotenv import load_dotenv

load_dotenv()

# État actuel des calques
CURRENT_STATE = {
    'base': 11,  # Target: 10 - DÉJÀ COMPLET
    'eyes': 5,   # Target: 18 - Manque 13
    'hair': 22,  # Target: 200 - Manque 178
    'mouth': 1,  # Target: 10 - Manque 9
    'nose': 1    # Target: 10 - Manque 9
}

TARGETS = {
    'base': 10,
    'eyes': 18,
    'hair': 200,
    'mouth': 10,
    'nose': 10
}


async def generate_missing_eyes(service: PortraitGeneratorService):
    """Génère les 13 yeux manquants (5 → 18)"""
    
    print("\n👁️ GÉNÉRATION DES YEUX MANQUANTS (5/18 → 18/18)")
    print("-" * 70)
    
    forms = ['european', 'asian', 'eurasian']
    colors = ['brown', 'blue', 'green', 'hazel', 'gray', 'amber']
    
    # Générer les combinaisons (3 formes × 6 couleurs = 18 total)
    combinations = []
    for form in forms:
        for color in colors:
            combinations.append((form, color))
    
    # On commence à partir de l'index 6 (car déjà 5 générés)
    start_idx = CURRENT_STATE['eyes'] + 1
    success_count = 0
    
    for idx in range(start_idx, TARGETS['eyes'] + 1):
        form, color = combinations[idx - 1]
        
        try:
            print(f"  [{idx}/18] Génération yeux '{form}' couleur '{color}'... ", end='', flush=True)
            
            prompt = f"""Create semi-realistic human eyes layer (eyes only, no other features).
Style: Semi-realistic, expressive, professional character portrait.
Eye shape: {form}
Eye color: {color}
View: Front view, looking forward
Background: Completely transparent (alpha channel)
Include: Both eyes with iris, pupils, eyelids, subtle eye highlights
Exclude: Eyebrows, surrounding skin, nose, other facial features
Quality: High detail, natural eye expression
Format: PNG with transparency"""

            images = await service.image_gen.generate_images(
                prompt=prompt,
                model="gpt-image-1",
                number_of_images=1
            )
            
            if images and len(images) > 0:
                filename = f"eyes_{form}_{color}_{idx}.png"
                filepath = os.path.join(service.base_path, 'eyes', filename)
                
                with open(filepath, 'wb') as f:
                    f.write(images[0])
                
                success_count += 1
                print(f"✅")
                
                # Pause courte entre chaque génération
                await asyncio.sleep(2)
            else:
                print(f"❌ Aucune image générée")
                
        except Exception as e:
            print(f"❌ Erreur: {str(e)[:100]}")
            continue
    
    print(f"\n✅ Yeux générés: {success_count}/13")
    return success_count


async def generate_missing_hair(service: PortraitGeneratorService):
    """Génère les 178 cheveux manquants (22 → 200)"""
    
    print("\n💇 GÉNÉRATION DES CHEVEUX MANQUANTS (22/200 → 200/200)")
    print("-" * 70)
    
    # Styles de coupe variés
    male_styles = [
        'buzz cut', 'crew cut', 'fade', 'undercut', 'pompadour',
        'quiff', 'slick back', 'side part', 'messy', 'spiky',
        'curly top', 'mohawk', 'faux hawk', 'caesar cut', 'ivy league',
        'textured crop', 'fringe', 'comb over', 'long on top', 'short sides'
    ]
    
    female_styles = [
        'long straight', 'wavy', 'curly', 'bob', 'pixie cut',
        'layered', 'bangs', 'side swept', 'updo', 'ponytail',
        'braids', 'messy bun', 'sleek', 'beach waves', 'shag',
        'lob', 'asymmetric', 'blunt cut', 'textured', 'feathered'
    ]
    
    hair_colors = ['black', 'dark brown', 'brown', 'light brown', 'blonde', 'red', 'auburn', 'gray']
    
    start_idx = CURRENT_STATE['hair'] + 1
    success_count = 0
    
    # Générer cheveux homme (jusqu'à 100)
    if start_idx <= 100:
        print("\n🧔 Cheveux homme...")
        for idx in range(start_idx, min(101, TARGETS['hair'] + 1)):
            style = male_styles[(idx - 1) % len(male_styles)]
            color = hair_colors[(idx - 1) % len(hair_colors)]
            
            try:
                print(f"  [HOMME {idx}/100] Style '{style}' couleur '{color}'... ", end='', flush=True)
                
                prompt = f"""Create semi-realistic male hair layer (hair only, no face features).
Style: {style}
Color: {color}
Gender: Male
View: Front view, natural hair flow
Background: Completely transparent (alpha channel)
Include: Hair strands, natural hair texture, realistic volume
Exclude: Face, forehead, ears, eyebrows, facial features
Quality: High detail, natural hair flow
Format: PNG with transparency"""

                images = await service.image_gen.generate_images(
                    prompt=prompt,
                    model="gpt-image-1",
                    number_of_images=1
                )
                
                if images and len(images) > 0:
                    filename = f"hair_male_{style.replace(' ', '_')}_{color.replace(' ', '_')}_{idx}.png"
                    filepath = os.path.join(service.base_path, 'hair', filename)
                    
                    with open(filepath, 'wb') as f:
                        f.write(images[0])
                    
                    success_count += 1
                    print(f"✅")
                    
                    # Pause courte
                    await asyncio.sleep(2)
                else:
                    print(f"❌")
                    
            except Exception as e:
                print(f"❌ Erreur: {str(e)[:100]}")
                continue
    
    # Générer cheveux femme (101 à 200)
    if TARGETS['hair'] > 100:
        print("\n👩 Cheveux femme...")
        start_female = max(101, start_idx)
        
        for idx in range(start_female, TARGETS['hair'] + 1):
            female_idx = idx - 100
            style = female_styles[(female_idx - 1) % len(female_styles)]
            color = hair_colors[(female_idx - 1) % len(hair_colors)]
            
            try:
                print(f"  [FEMME {female_idx}/100] Style '{style}' couleur '{color}'... ", end='', flush=True)
                
                prompt = f"""Create semi-realistic female hair layer (hair only, no face features).
Style: {style}
Color: {color}
Gender: Female
View: Front view, natural hair flow
Background: Completely transparent (alpha channel)
Include: Hair strands, natural hair texture, realistic volume
Exclude: Face, forehead, ears, eyebrows, facial features
Quality: High detail, natural hair flow
Format: PNG with transparency"""

                images = await service.image_gen.generate_images(
                    prompt=prompt,
                    model="gpt-image-1",
                    number_of_images=1
                )
                
                if images and len(images) > 0:
                    filename = f"hair_female_{style.replace(' ', '_')}_{color.replace(' ', '_')}_{idx}.png"
                    filepath = os.path.join(service.base_path, 'hair', filename)
                    
                    with open(filepath, 'wb') as f:
                        f.write(images[0])
                    
                    success_count += 1
                    print(f"✅")
                    
                    # Pause courte
                    await asyncio.sleep(2)
                else:
                    print(f"❌")
                    
            except Exception as e:
                print(f"❌ Erreur: {str(e)[:100]}")
                continue
    
    print(f"\n✅ Cheveux générés: {success_count}/178")
    return success_count


async def generate_missing_mouths(service: PortraitGeneratorService):
    """Génère les 9 bouches manquantes (1 → 10)"""
    
    print("\n👄 GÉNÉRATION DES BOUCHES MANQUANTES (1/10 → 10/10)")
    print("-" * 70)
    
    mouth_types = [
        ('neutral', 'bouche neutre, détendue'),
        ('slight smile', 'léger sourire, amical'),
        ('smile', 'sourire naturel'),
        ('wide smile', 'grand sourire'),
        ('serious', 'bouche sérieuse, fermée'),
        ('determined', 'bouche déterminée'),
        ('thin lips', 'lèvres fines, naturelles'),
        ('full lips', 'lèvres pulpeuses, naturelles'),
        ('slight frown', 'léger froncement'),
        ('pursed', 'lèvres pincées')
    ]
    
    start_idx = CURRENT_STATE['mouth'] + 1
    success_count = 0
    
    for idx in range(start_idx, TARGETS['mouth'] + 1):
        mouth_type, description = mouth_types[idx - 1]
        
        try:
            print(f"  [{idx}/10] Génération bouche '{description}'... ", end='', flush=True)
            
            prompt = f"""Create semi-realistic human mouth layer (mouth only, no other features).
Style: Semi-realistic, natural, professional character portrait.
Mouth type: {mouth_type} ({description})
View: Front view, centered
Background: Completely transparent (alpha channel)
Include: Lips with natural color, subtle highlights
Exclude: Nose, chin, cheeks, teeth (unless smiling), surrounding skin
Quality: High detail, natural lip texture
Format: PNG with transparency"""

            images = await service.image_gen.generate_images(
                prompt=prompt,
                model="gpt-image-1",
                number_of_images=1
            )
            
            if images and len(images) > 0:
                filename = f"mouth_{mouth_type.replace(' ', '_')}_{idx}.png"
                filepath = os.path.join(service.base_path, 'mouth', filename)
                
                with open(filepath, 'wb') as f:
                    f.write(images[0])
                
                success_count += 1
                print(f"✅")
                
                # Pause courte
                await asyncio.sleep(2)
            else:
                print(f"❌ Aucune image générée")
                
        except Exception as e:
            print(f"❌ Erreur: {str(e)[:100]}")
            continue
    
    print(f"\n✅ Bouches générées: {success_count}/9")
    return success_count


async def generate_missing_noses(service: PortraitGeneratorService):
    """Génère les 9 nez manquants (1 → 10)"""
    
    print("\n👃 GÉNÉRATION DES NEZ MANQUANTS (1/10 → 10/10)")
    print("-" * 70)
    
    nose_types = [
        ('straight', 'nez droit, classique'),
        ('aquiline', 'nez aquilin, légèrement courbé'),
        ('roman', 'nez romain, fort'),
        ('snub', 'nez retroussé'),
        ('button', 'petit nez arrondi'),
        ('hawk', 'nez en bec d\'aigle'),
        ('greek', 'nez grec, fin'),
        ('wide', 'nez large, fort'),
        ('flat', 'nez plat, large base'),
        ('pointed', 'nez pointu, fin')
    ]
    
    start_idx = CURRENT_STATE['nose'] + 1
    success_count = 0
    
    for idx in range(start_idx, TARGETS['nose'] + 1):
        nose_type, description = nose_types[idx - 1]
        
        try:
            print(f"  [{idx}/10] Génération nez '{description}'... ", end='', flush=True)
            
            prompt = f"""Create semi-realistic human nose layer (nose only, no other features).
Style: Semi-realistic, natural, professional character portrait.
Nose type: {nose_type} ({description})
View: Front view, centered
Background: Completely transparent (alpha channel)
Include: Nose bridge, nostrils, nose tip with natural shading
Exclude: Eyes, mouth, cheeks, forehead, surrounding skin
Quality: High detail, natural nose structure
Format: PNG with transparency"""

            images = await service.image_gen.generate_images(
                prompt=prompt,
                model="gpt-image-1",
                number_of_images=1
            )
            
            if images and len(images) > 0:
                filename = f"nose_{nose_type.replace(' ', '_')}_{idx}.png"
                filepath = os.path.join(service.base_path, 'nose', filename)
                
                with open(filepath, 'wb') as f:
                    f.write(images[0])
                
                success_count += 1
                print(f"✅")
                
                # Pause courte
                await asyncio.sleep(2)
            else:
                print(f"❌ Aucune image générée")
                
        except Exception as e:
            print(f"❌ Erreur: {str(e)[:100]}")
            continue
    
    print(f"\n✅ Nez générés: {success_count}/9")
    return success_count


async def main():
    """Fonction principale"""
    
    print("=" * 80)
    print("🎨 GÉNÉRATION DES CALQUES MANQUANTS - OPTIMISÉE")
    print("=" * 80)
    
    print("\n📊 INVENTAIRE ACTUEL:")
    for layer_type, count in CURRENT_STATE.items():
        target = TARGETS[layer_type]
        missing = max(0, target - count)
        status = "✅ COMPLET" if missing == 0 else f"❌ Manque {missing}"
        print(f"  • {layer_type.capitalize()}: {count}/{target} {status}")
    
    total_missing = sum(max(0, TARGETS[k] - CURRENT_STATE[k]) for k in TARGETS.keys())
    print(f"\n🎯 TOTAL À GÉNÉRER: {total_missing} calques manquants")
    print("=" * 80)
    
    # Initialiser le service
    service = PortraitGeneratorService()
    
    results = {
        'eyes': 0,
        'hair': 0,
        'mouth': 0,
        'nose': 0
    }
    
    # Générer seulement ce qui manque
    try:
        # 1. Yeux (si manquants)
        if CURRENT_STATE['eyes'] < TARGETS['eyes']:
            results['eyes'] = await generate_missing_eyes(service)
        else:
            print("\n👁️ Yeux: ✅ Déjà complet")
        
        # 2. Bouches (si manquantes)
        if CURRENT_STATE['mouth'] < TARGETS['mouth']:
            results['mouth'] = await generate_missing_mouths(service)
        else:
            print("\n👄 Bouches: ✅ Déjà complet")
        
        # 3. Nez (si manquants)
        if CURRENT_STATE['nose'] < TARGETS['nose']:
            results['nose'] = await generate_missing_noses(service)
        else:
            print("\n👃 Nez: ✅ Déjà complet")
        
        # 4. Cheveux (si manquants) - EN DERNIER car le plus long
        if CURRENT_STATE['hair'] < TARGETS['hair']:
            results['hair'] = await generate_missing_hair(service)
        else:
            print("\n💇 Cheveux: ✅ Déjà complet")
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Génération interrompue par l'utilisateur")
    except Exception as e:
        print(f"\n\n❌ Erreur fatale: {str(e)}")
    
    # Résumé final
    print("\n" + "=" * 80)
    print("📊 RÉSUMÉ DE LA GÉNÉRATION")
    print("=" * 80)
    
    for layer_type, count in results.items():
        target_missing = max(0, TARGETS[layer_type] - CURRENT_STATE[layer_type])
        if target_missing > 0:
            percentage = (count / target_missing * 100) if target_missing > 0 else 0
            print(f"  • {layer_type.capitalize()}: {count}/{target_missing} générés ({percentage:.1f}%)")
    
    total_generated = sum(results.values())
    print(f"\n🎯 TOTAL GÉNÉRÉ: {total_generated}/{total_missing} calques")
    
    # État final
    final_state = {k: CURRENT_STATE[k] + results.get(k, 0) for k in CURRENT_STATE.keys()}
    print("\n📊 ÉTAT FINAL:")
    for layer_type, count in final_state.items():
        target = TARGETS[layer_type]
        percentage = (count / target * 100) if target > 0 else 0
        print(f"  • {layer_type.capitalize()}: {count}/{target} ({percentage:.1f}%)")
    
    total_final = sum(final_state.values())
    total_target = sum(TARGETS.values())
    global_percentage = (total_final / total_target * 100) if total_target > 0 else 0
    
    print(f"\n✅ PROGRESSION GLOBALE: {total_final}/{total_target} ({global_percentage:.1f}%)")


if __name__ == "__main__":
    asyncio.run(main())
