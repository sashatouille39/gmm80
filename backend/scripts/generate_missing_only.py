"""
Script optimisé pour générer SEULEMENT les calques manquants
Vérifie ce qui existe déjà et génère le reste
"""
import asyncio
import sys
import os
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from services.portrait_generator_service import PortraitGeneratorService
from dotenv import load_dotenv

load_dotenv()


def get_existing_layers(base_path):
    """Compte les calques existants"""
    counts = {
        'base': len(list(Path(base_path, 'base').glob('skin_tone_*.png'))),
        'eyes': len(list(Path(base_path, 'eyes').glob('eyes_*.png'))),
        'hair_male': len(list(Path(base_path, 'hair').glob('hair_male_*.png'))),
        'hair_female': len(list(Path(base_path, 'hair').glob('hair_female_*.png'))),
        'mouth': len(list(Path(base_path, 'mouth').glob('mouth_*.png'))),
        'nose': len(list(Path(base_path, 'nose').glob('nose_*.png'))),
    }
    return counts


async def generate_missing_layers():
    """Génère seulement les calques manquants"""
    
    service = PortraitGeneratorService()
    
    print("\n" + "🎨" * 35)
    print("  GÉNÉRATION DES CALQUES MANQUANTS")
    print("🎨" * 35)
    
    # Vérifier l'existant
    existing = get_existing_layers(service.base_path)
    
    print("\n📊 CALQUES EXISTANTS:")
    print("-" * 70)
    print(f"  • Bases (peau):  {existing['base']}/10")
    print(f"  • Yeux:          {existing['eyes']}/18")
    print(f"  • Cheveux homme: {existing['hair_male']}/100")
    print(f"  • Cheveux femme: {existing['hair_female']}/100")
    print(f"  • Bouches:       {existing['mouth']}/10")
    print(f"  • Nez:           {existing['nose']}/10")
    
    total_existing = sum(existing.values())
    total_needed = 248
    missing = total_needed - total_existing
    
    print(f"\n  🎯 TOTAL: {total_existing}/248 existants")
    print(f"  ⚡ À GÉNÉRER: {missing} calques manquants")
    
    if missing == 0:
        print("\n✅ TOUS LES CALQUES SONT DÉJÀ GÉNÉRÉS!")
        return
    
    print("\n" + "=" * 70)
    print("\n🚀 GÉNÉRATION DES CALQUES MANQUANTS...")
    print("=" * 70)
    
    results = {}
    
    # 1. YEUX (si manquants)
    if existing['eyes'] < 18:
        print(f"\n👁️  GÉNÉRATION DES YEUX ({existing['eyes']}/18 → 18/18)")
        print("-" * 70)
        
        eye_forms = [
            ('european', 'European/American - almond-shaped, medium size, visible eyelid crease'),
            ('asian', 'East Asian - slightly narrower, monolid or subtle crease, elegant shape'),
            ('eurasian', 'Eurasian/Mixed - blend of features, medium-large, defined but soft crease')
        ]
        
        eye_colors = [
            ('brown', '#5C3317'), ('blue', '#4682B4'), ('green', '#2E8B57'),
            ('hazel', '#8E7618'), ('gray', '#708090'), ('amber', '#FFBF00')
        ]
        
        success = 0
        for form_key, form_desc in eye_forms:
            for color_key, hex_color in eye_colors:
                filename = f"eyes_{form_key}_{color_key}.png"
                filepath = os.path.join(service.base_path, 'eyes', filename)
                
                if os.path.exists(filepath):
                    print(f"  ⏭️  {form_key}-{color_key} (existe déjà)")
                    success += 1
                    continue
                
                try:
                    print(f"  [{success+1}/18] {form_key}-{color_key}... ", end='', flush=True)
                    
                    prompt = f"""Create semi-realistic human eyes for a character portrait.
Style: Semi-realistic, detailed, professional illustration
Eye type: {form_desc}
Eye color: {color_key} iris ({hex_color})
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
                        with open(filepath, 'wb') as f:
                            f.write(images[0])
                        success += 1
                        print(f"✅")
                    else:
                        print(f"❌")
                        
                except Exception as e:
                    print(f"❌ {str(e)[:50]}")
                    continue
        
        results['eyes'] = success
        print(f"\n✨ Yeux: {success}/18")
    
    # 2. CHEVEUX HOMME (compléter)
    if existing['hair_male'] < 100:
        start_idx = existing['hair_male'] + 1
        print(f"\n👨 CHEVEUX HOMME ({existing['hair_male']}/100 → 100/100)")
        print("-" * 70)
        
        male_styles = [
            'short crew cut', 'buzz cut', 'classic short', 'side part', 'slicked back',
            'messy short', 'textured crop', 'modern quiff', 'pompadour', 'undercut',
            'fade', 'comb over', 'fringe', 'spiky', 'wavy short',
            'curly short', 'afro short', 'dreadlocks short', 'mohawk', 'faux hawk'
        ]
        
        hair_colors = [
            ('black', '#0A0A0A'), ('dark brown', '#2C1810'), ('brown', '#3E2723'),
            ('light brown', '#5D4037'), ('auburn', '#6D2C10'), ('red', '#8B2500'),
            ('blonde', '#E1B87F'), ('light blonde', '#F5DEB3'), ('gray', '#696969'), ('white', '#DCDCDC')
        ]
        
        success = existing['hair_male']
        for i in range(start_idx, 101):
            style = male_styles[(i - 1) % len(male_styles)]
            color, hex_color = hair_colors[(i - 1) % len(hair_colors)]
            
            try:
                print(f"  [{i}/100] {style}-{color}... ", end='', flush=True)
                
                prompt = f"""Create semi-realistic male hair for a character portrait.
Style: Semi-realistic, detailed, professional illustration
Hair style: {style}
Hair color: {color} ({hex_color})
View: Front view, centered
Background: Completely transparent (alpha channel)
Include: Hair only, natural texture and volume
Exclude: Face, forehead, ears, facial features
Quality: High detail with individual hair strands visible
Format: PNG with transparency"""

                images = await service.image_gen.generate_images(
                    prompt=prompt,
                    model="gpt-image-1",
                    number_of_images=1
                )
                
                if images and len(images) > 0:
                    filename = f"hair_male_{i:03d}.png"
                    filepath = os.path.join(service.base_path, 'hair', filename)
                    
                    with open(filepath, 'wb') as f:
                        f.write(images[0])
                    success += 1
                    print(f"✅")
                else:
                    print(f"❌")
                    
            except Exception as e:
                print(f"❌ {str(e)[:30]}")
                continue
        
        results['hair_male'] = success
        print(f"\n✨ Cheveux homme: {success}/100")
    
    # 3. CHEVEUX FEMME
    if existing['hair_female'] < 100:
        print(f"\n👩 CHEVEUX FEMME ({existing['hair_female']}/100 → 100/100)")
        print("-" * 70)
        
        female_styles = [
            'long straight', 'long wavy', 'long curly', 'shoulder length', 'bob cut',
            'pixie cut', 'layered medium', 'ponytail', 'bun', 'braids',
            'side swept', 'bangs', 'beach waves', 'ringlets', 'afro',
            'box braids', 'cornrows', 'updo', 'half up half down', 'shag cut'
        ]
        
        hair_colors = [
            ('black', '#0A0A0A'), ('dark brown', '#2C1810'), ('brown', '#3E2723'),
            ('light brown', '#5D4037'), ('auburn', '#6D2C10'), ('red', '#8B2500'),
            ('blonde', '#E1B87F'), ('light blonde', '#F5DEB3'), ('gray', '#696969'), ('white', '#DCDCDC')
        ]
        
        success = 0
        for i in range(1, 101):
            style = female_styles[(i - 1) % len(female_styles)]
            color, hex_color = hair_colors[(i - 1) % len(hair_colors)]
            
            try:
                print(f"  [{i}/100] {style}-{color}... ", end='', flush=True)
                
                prompt = f"""Create semi-realistic female hair for a character portrait.
Style: Semi-realistic, detailed, professional illustration
Hair style: {style}
Hair color: {color} ({hex_color})
View: Front view, centered
Background: Completely transparent (alpha channel)
Include: Hair only, natural texture and volume
Exclude: Face, forehead, ears, facial features
Quality: High detail with flowing hair texture
Format: PNG with transparency"""

                images = await service.image_gen.generate_images(
                    prompt=prompt,
                    model="gpt-image-1",
                    number_of_images=1
                )
                
                if images and len(images) > 0:
                    filename = f"hair_female_{i:03d}.png"
                    filepath = os.path.join(service.base_path, 'hair', filename)
                    
                    with open(filepath, 'wb') as f:
                        f.write(images[0])
                    success += 1
                    print(f"✅")
                else:
                    print(f"❌")
                    
            except Exception as e:
                print(f"❌ {str(e)[:30]}")
                continue
        
        results['hair_female'] = success
        print(f"\n✨ Cheveux femme: {success}/100")
    
    # 4. BOUCHES
    if existing['mouth'] < 10:
        print(f"\n👄 BOUCHES ({existing['mouth']}/10 → 10/10)")
        print("-" * 70)
        
        mouth_types = [
            ('full lips', 'Full, plump lips with defined cupid\'s bow'),
            ('thin lips', 'Thin, delicate lips with subtle shape'),
            ('medium lips', 'Medium, balanced lips with natural fullness'),
            ('wide smile', 'Wide mouth with natural smile lines'),
            ('small mouth', 'Small, petite mouth with soft curves'),
            ('heart shaped', 'Heart-shaped lips with prominent cupid\'s bow'),
            ('straight lips', 'Straight, even lips with minimal curve'),
            ('downturned', 'Slightly downturned corners, neutral expression'),
            ('upturned', 'Slightly upturned corners, friendly expression'),
            ('asymmetric', 'Naturally asymmetric, realistic variation')
        ]
        
        success = 0
        for idx, (mouth_name, description) in enumerate(mouth_types, 1):
            filename = f"mouth_{idx:02d}.png"
            filepath = os.path.join(service.base_path, 'mouth', filename)
            
            if os.path.exists(filepath):
                print(f"  ⏭️  [{idx}/10] {mouth_name} (existe déjà)")
                success += 1
                continue
            
            try:
                print(f"  [{idx}/10] {mouth_name}... ", end='', flush=True)
                
                prompt = f"""Create a semi-realistic human mouth for a character portrait.
Style: Semi-realistic, detailed, professional illustration
Mouth type: {description}
Expression: Neutral, relaxed, closed mouth
View: Front view, centered
Background: Completely transparent (alpha channel)
Include: Lips with natural color (neutral pink-rose tone), subtle texture
Exclude: Teeth, tongue, nose, chin, other facial features
Quality: High detail with natural lip texture
Format: PNG with transparency"""

                images = await service.image_gen.generate_images(
                    prompt=prompt,
                    model="gpt-image-1",
                    number_of_images=1
                )
                
                if images and len(images) > 0:
                    with open(filepath, 'wb') as f:
                        f.write(images[0])
                    success += 1
                    print(f"✅")
                else:
                    print(f"❌")
                    
            except Exception as e:
                print(f"❌ {str(e)[:30]}")
                continue
        
        results['mouth'] = success
        print(f"\n✨ Bouches: {success}/10")
    
    # 5. NEZ
    if existing['nose'] < 10:
        print(f"\n👃 NEZ ({existing['nose']}/10 → 10/10)")
        print("-" * 70)
        
        nose_types = [
            ('straight', 'Straight, narrow nose with defined bridge'),
            ('button', 'Small, upturned button nose with round tip'),
            ('roman', 'Roman nose with prominent bridge and slight curve'),
            ('snub', 'Short, slightly upturned snub nose'),
            ('hawk', 'Hooked/aquiline nose with curved bridge'),
            ('wide', 'Wide nose with broad nostrils'),
            ('narrow', 'Narrow, refined nose with thin bridge'),
            ('flat bridge', 'Flat or low nasal bridge, common in Asian features'),
            ('broad round', 'Broad nose with rounded tip, African features'),
            ('greek', 'Greek nose - straight, continuing forehead line')
        ]
        
        success = 0
        for idx, (nose_name, description) in enumerate(nose_types, 1):
            filename = f"nose_{idx:02d}.png"
            filepath = os.path.join(service.base_path, 'nose', filename)
            
            if os.path.exists(filepath):
                print(f"  ⏭️  [{idx}/10] {nose_name} (existe déjà)")
                success += 1
                continue
            
            try:
                print(f"  [{idx}/10] {nose_name}... ", end='', flush=True)
                
                prompt = f"""Create a semi-realistic human nose for a character portrait.
Style: Semi-realistic, detailed, professional illustration
Nose type: {description}
View: Front view, centered
Background: Completely transparent (alpha channel)
Include: Nose with natural skin tone (medium neutral), nostrils, bridge
Exclude: Eyes, mouth, cheeks, other facial features
Quality: High detail with natural nose structure
Format: PNG with transparency"""

                images = await service.image_gen.generate_images(
                    prompt=prompt,
                    model="gpt-image-1",
                    number_of_images=1
                )
                
                if images and len(images) > 0:
                    with open(filepath, 'wb') as f:
                        f.write(images[0])
                    success += 1
                    print(f"✅")
                else:
                    print(f"❌")
                    
            except Exception as e:
                print(f"❌ {str(e)[:30]}")
                continue
        
        results['nose'] = success
        print(f"\n✨ Nez: {success}/10")
    
    # Résumé final
    print("\n" + "=" * 70)
    print("🎉 GÉNÉRATION TERMINÉE!")
    print("=" * 70)
    
    final_counts = get_existing_layers(service.base_path)
    total_final = sum(final_counts.values())
    
    print(f"\n📊 RÉSULTATS FINAUX:")
    print(f"  • Bases:         {final_counts['base']}/10")
    print(f"  • Yeux:          {final_counts['eyes']}/18")
    print(f"  • Cheveux homme: {final_counts['hair_male']}/100")
    print(f"  • Cheveux femme: {final_counts['hair_female']}/100")
    print(f"  • Bouches:       {final_counts['mouth']}/10")
    print(f"  • Nez:           {final_counts['nose']}/10")
    print(f"\n  🎯 TOTAL: {total_final}/248 ({total_final*100/248:.1f}%)")
    
    if total_final >= 248 * 0.8:
        combinations = (
            final_counts['base'] *
            final_counts['eyes'] *
            (final_counts['hair_male'] + final_counts['hair_female']) *
            final_counts['mouth'] *
            final_counts['nose']
        )
        print(f"  🎲 COMBINAISONS: {combinations:,}")
        print("\n✅ SYSTÈME OPÉRATIONNEL!")
    
    print("=" * 70)


if __name__ == "__main__":
    try:
        asyncio.run(generate_missing_layers())
    except KeyboardInterrupt:
        print("\n\n⚠️  Génération interrompue")
    except Exception as e:
        print(f"\n\n❌ Erreur: {str(e)}")
        import traceback
        traceback.print_exc()
