"""
Script pour générer une bibliothèque personnalisée de calques
Configuration spécifique: 200 cheveux, 10 nez, 10 bouches, 18 yeux, 10 bases
"""
import asyncio
import sys
import os
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from services.portrait_generator_service import PortraitGeneratorService
from dotenv import load_dotenv

load_dotenv()


# Configuration personnalisée des calques à générer
CUSTOM_CONFIG = {
    'base': {
        'count': 10,
        'description': '10 teintes de peau (brun foncé à beige clair)'
    },
    'eyes': {
        'count': 18,  # 3 formes × 6 couleurs
        'description': '3 formes yeux (européen, asiatique, eurasien) × 6 couleurs',
        'forms': ['european', 'asian', 'eurasian'],
        'colors': ['brown', 'blue', 'green', 'hazel', 'gray', 'amber']
    },
    'hair': {
        'count': 200,  # 100 homme + 100 femme
        'description': '100 coupes homme + 100 coupes femme',
        'male': 100,
        'female': 100
    },
    'mouth': {
        'count': 10,
        'description': '10 formes de bouche réalistes'
    },
    'nose': {
        'count': 10,
        'description': '10 formes de nez réalistes'
    }
}


async def generate_base_layers(service: PortraitGeneratorService):
    """Génère 10 teintes de peau différentes (brun foncé à beige clair)"""
    
    print("\n🎨 GÉNÉRATION DES BASES (teintes de peau)")
    print("-" * 70)
    
    # Teintes de peau de brun foncé à beige clair
    skin_tones = [
        ('dark brown', '#3D2817', 'Brun très foncé'),
        ('brown', '#4A3728', 'Brun foncé'),
        ('medium brown', '#6B4A3A', 'Brun moyen'),
        ('tan brown', '#8B6F47', 'Brun clair'),
        ('tan', '#A67C52', 'Bronzé'),
        ('medium tan', '#C9A375', 'Beige bronzé'),
        ('light tan', '#D4B896', 'Beige moyen'),
        ('beige', '#E8C9A8', 'Beige'),
        ('light beige', '#F3DBC3', 'Beige clair'),
        ('fair', '#FBE7D6', 'Très clair')
    ]
    
    success_count = 0
    
    for idx, (tone_name, hex_color, description_fr) in enumerate(skin_tones, 1):
        try:
            print(f"  [{idx}/10] Génération teinte '{description_fr}' ({hex_color})... ", end='', flush=True)
            
            prompt = f"""Create a semi-realistic human head base layer (face shape only, no features).
Style: Semi-realistic, clean, professional character portrait.
Skin tone: {tone_name} ({hex_color})
View: Front view, neutral, centered
Background: Completely transparent (alpha channel)
Include: Head shape, basic face contour, ears
Exclude: Eyes, nose, mouth, hair, eyebrows, facial hair
Quality: High detail, smooth skin texture
Format: PNG with transparency"""

            images = await service.image_gen.generate_image(
                prompt=prompt,
                model="gpt-image-1",
                size="1024x1024",
                quality="standard",
                number_of_images=1
            )
            
            if images and len(images) > 0:
                # Sauvegarder avec nomenclature: skin_tone_X_base.png
                filename = f"skin_tone_{idx}_base.png"
                filepath = os.path.join(service.base_path, 'base', filename)
                
                with open(filepath, 'wb') as f:
                    f.write(images[0])
                
                success_count += 1
                print(f"✅")
            else:
                print(f"❌ Aucune image générée")
                
        except Exception as e:
            print(f"❌ Erreur: {str(e)}")
            continue
    
    print(f"\n✨ Bases générées: {success_count}/10")
    return success_count


async def generate_eyes_layers(service: PortraitGeneratorService):
    """Génère 18 calques yeux: 3 formes × 6 couleurs"""
    
    print("\n👁️  GÉNÉRATION DES YEUX (formes et couleurs)")
    print("-" * 70)
    
    eye_forms = [
        ('european', 'European/American - almond-shaped, medium size, visible eyelid crease'),
        ('asian', 'East Asian - slightly narrower, monolid or subtle crease, elegant shape'),
        ('eurasian', 'Eurasian/Mixed - blend of features, medium-large, defined but soft crease')
    ]
    
    eye_colors = [
        ('brown', '#5C3317', 'Marron'),
        ('blue', '#4682B4', 'Bleu'),
        ('green', '#2E8B57', 'Vert'),
        ('hazel', '#8E7618', 'Noisette'),
        ('gray', '#708090', 'Gris'),
        ('amber', '#FFBF00', 'Ambre')
    ]
    
    success_count = 0
    total = len(eye_forms) * len(eye_colors)
    current = 0
    
    for form_key, form_desc in eye_forms:
        for color_key, hex_color, color_fr in eye_colors:
            current += 1
            try:
                print(f"  [{current}/{total}] {form_key.capitalize()} - {color_fr}... ", end='', flush=True)
                
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

                images = await service.image_gen.generate_image(
                    prompt=prompt,
                    model="gpt-image-1",
                    size="1024x1024",
                    quality="standard",
                    number_of_images=1
                )
                
                if images and len(images) > 0:
                    filename = f"eyes_{form_key}_{color_key}.png"
                    filepath = os.path.join(service.base_path, 'eyes', filename)
                    
                    with open(filepath, 'wb') as f:
                        f.write(images[0])
                    
                    success_count += 1
                    print(f"✅")
                else:
                    print(f"❌")
                    
            except Exception as e:
                print(f"❌ {str(e)[:30]}")
                continue
    
    print(f"\n✨ Yeux générés: {success_count}/{total}")
    return success_count


async def generate_hair_layers(service: PortraitGeneratorService):
    """Génère 200 coupes de cheveux: 100 homme + 100 femme"""
    
    print("\n💇 GÉNÉRATION DES CHEVEUX (100 homme + 100 femme)")
    print("-" * 70)
    
    # Styles de cheveux variés pour hommes
    male_styles = [
        'short crew cut', 'buzz cut', 'classic short', 'side part', 'slicked back',
        'messy short', 'textured crop', 'modern quiff', 'pompadour', 'undercut',
        'fade', 'comb over', 'fringe', 'spiky', 'wavy short',
        'curly short', 'afro short', 'dreadlocks short', 'mohawk', 'faux hawk'
    ]
    
    # Styles de cheveux variés pour femmes
    female_styles = [
        'long straight', 'long wavy', 'long curly', 'shoulder length', 'bob cut',
        'pixie cut', 'layered medium', 'ponytail', 'bun', 'braids',
        'side swept', 'bangs', 'beach waves', 'ringlets', 'afro',
        'box braids', 'cornrows', 'updo', 'half up half down', 'shag cut'
    ]
    
    # Couleurs de cheveux variées
    hair_colors = [
        ('black', '#0A0A0A'),
        ('dark brown', '#2C1810'),
        ('brown', '#3E2723'),
        ('light brown', '#5D4037'),
        ('auburn', '#6D2C10'),
        ('red', '#8B2500'),
        ('blonde', '#E1B87F'),
        ('light blonde', '#F5DEB3'),
        ('gray', '#696969'),
        ('white', '#DCDCDC')
    ]
    
    success_count = 0
    
    # Générer 100 cheveux pour hommes
    print("\n  👨 CHEVEUX HOMME (100 variations)")
    for i in range(1, 101):
        style = male_styles[(i - 1) % len(male_styles)]
        color, hex_color = hair_colors[(i - 1) % len(hair_colors)]
        
        try:
            print(f"    [{i}/100] {style} - {color}... ", end='', flush=True)
            
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

            images = await service.image_gen.generate_image(
                prompt=prompt,
                model="gpt-image-1",
                size="1024x1024",
                quality="standard",
                number_of_images=1
            )
            
            if images and len(images) > 0:
                filename = f"hair_male_{i:03d}.png"
                filepath = os.path.join(service.base_path, 'hair', filename)
                
                with open(filepath, 'wb') as f:
                    f.write(images[0])
                
                success_count += 1
                print(f"✅")
            else:
                print(f"❌")
                
        except Exception as e:
            print(f"❌ {str(e)[:20]}")
            continue
    
    # Générer 100 cheveux pour femmes
    print("\n  👩 CHEVEUX FEMME (100 variations)")
    for i in range(1, 101):
        style = female_styles[(i - 1) % len(female_styles)]
        color, hex_color = hair_colors[(i - 1) % len(hair_colors)]
        
        try:
            print(f"    [{i}/100] {style} - {color}... ", end='', flush=True)
            
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

            images = await service.image_gen.generate_image(
                prompt=prompt,
                model="gpt-image-1",
                size="1024x1024",
                quality="standard",
                number_of_images=1
            )
            
            if images and len(images) > 0:
                filename = f"hair_female_{i:03d}.png"
                filepath = os.path.join(service.base_path, 'hair', filename)
                
                with open(filepath, 'wb') as f:
                    f.write(images[0])
                
                success_count += 1
                print(f"✅")
            else:
                print(f"❌")
                
        except Exception as e:
            print(f"❌ {str(e)[:20]}")
            continue
    
    print(f"\n✨ Cheveux générés: {success_count}/200")
    return success_count


async def generate_mouth_layers(service: PortraitGeneratorService):
    """Génère 10 formes de bouche réalistes"""
    
    print("\n👄 GÉNÉRATION DES BOUCHES (10 variations)")
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
    
    success_count = 0
    
    for idx, (mouth_name, description) in enumerate(mouth_types, 1):
        try:
            print(f"  [{idx}/10] {mouth_name.capitalize()}... ", end='', flush=True)
            
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

            images = await service.image_gen.generate_image(
                prompt=prompt,
                model="gpt-image-1",
                size="1024x1024",
                quality="standard",
                number_of_images=1
            )
            
            if images and len(images) > 0:
                filename = f"mouth_{idx:02d}.png"
                filepath = os.path.join(service.base_path, 'mouth', filename)
                
                with open(filepath, 'wb') as f:
                    f.write(images[0])
                
                success_count += 1
                print(f"✅")
            else:
                print(f"❌")
                
        except Exception as e:
            print(f"❌ {str(e)[:30]}")
            continue
    
    print(f"\n✨ Bouches générées: {success_count}/10")
    return success_count


async def generate_nose_layers(service: PortraitGeneratorService):
    """Génère 10 formes de nez réalistes"""
    
    print("\n👃 GÉNÉRATION DES NEZ (10 variations)")
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
    
    success_count = 0
    
    for idx, (nose_name, description) in enumerate(nose_types, 1):
        try:
            print(f"  [{idx}/10] {nose_name.capitalize()}... ", end='', flush=True)
            
            prompt = f"""Create a semi-realistic human nose for a character portrait.
Style: Semi-realistic, detailed, professional illustration
Nose type: {description}
View: Front view, centered
Background: Completely transparent (alpha channel)
Include: Nose with natural skin tone (medium neutral), nostrils, bridge
Exclude: Eyes, mouth, cheeks, other facial features
Quality: High detail with natural nose structure
Format: PNG with transparency"""

            images = await service.image_gen.generate_image(
                prompt=prompt,
                model="gpt-image-1",
                size="1024x1024",
                quality="standard",
                number_of_images=1
            )
            
            if images and len(images) > 0:
                filename = f"nose_{idx:02d}.png"
                filepath = os.path.join(service.base_path, 'nose', filename)
                
                with open(filepath, 'wb') as f:
                    f.write(images[0])
                
                success_count += 1
                print(f"✅")
            else:
                print(f"❌")
                
        except Exception as e:
            print(f"❌ {str(e)[:30]}")
            continue
    
    print(f"\n✨ Nez générés: {success_count}/10")
    return success_count


async def generate_custom_library():
    """Génère la bibliothèque personnalisée complète"""
    
    service = PortraitGeneratorService()
    
    print("\n" + "🎨" * 35)
    print("  GÉNÉRATEUR DE BIBLIOTHÈQUE PERSONNALISÉE")
    print("🎨" * 35)
    
    print("\n📊 CONFIGURATION:")
    print("-" * 70)
    for layer_type, config in CUSTOM_CONFIG.items():
        print(f"  • {layer_type.upper()}: {config['count']} calques - {config['description']}")
    
    total_to_generate = sum(config['count'] for config in CUSTOM_CONFIG.values())
    print(f"\n  📈 TOTAL: {total_to_generate} calques à générer")
    
    # Calculer les combinaisons possibles
    combinations = (
        CUSTOM_CONFIG['base']['count'] *
        CUSTOM_CONFIG['eyes']['count'] *
        CUSTOM_CONFIG['hair']['count'] *
        CUSTOM_CONFIG['mouth']['count'] *
        CUSTOM_CONFIG['nose']['count']
    )
    print(f"  🎯 COMBINAISONS POSSIBLES: {combinations:,}")
    
    print("\n" + "=" * 70)
    input("\n⏸️  Appuyez sur ENTRÉE pour commencer la génération...")
    print("=" * 70)
    
    # Compteurs de succès
    results = {}
    
    # Générer chaque type de calque
    results['base'] = await generate_base_layers(service)
    results['eyes'] = await generate_eyes_layers(service)
    results['hair'] = await generate_hair_layers(service)
    results['mouth'] = await generate_mouth_layers(service)
    results['nose'] = await generate_nose_layers(service)
    
    # Résumé final
    print("\n" + "=" * 70)
    print("🎉 GÉNÉRATION TERMINÉE!")
    print("=" * 70)
    
    total_generated = sum(results.values())
    print(f"\n📊 RÉSULTATS:")
    for layer_type, count in results.items():
        expected = CUSTOM_CONFIG[layer_type]['count']
        percentage = (count / expected * 100) if expected > 0 else 0
        status = "✅" if percentage >= 80 else "⚠️"
        print(f"  {status} {layer_type.upper()}: {count}/{expected} ({percentage:.1f}%)")
    
    print(f"\n  🎯 TOTAL: {total_generated}/{total_to_generate} calques générés")
    
    if total_generated >= total_to_generate * 0.8:
        print("\n✨ Succès! Le système peut maintenant assembler des portraits uniques!")
    else:
        print("\n⚠️  Certains calques n'ont pas pu être générés. Le système utilisera des fallbacks.")
    
    print("=" * 70)


if __name__ == "__main__":
    try:
        asyncio.run(generate_custom_library())
    except KeyboardInterrupt:
        print("\n\n⚠️  Génération interrompue par l'utilisateur")
    except Exception as e:
        print(f"\n\n❌ Erreur fatale: {str(e)}")
        import traceback
        traceback.print_exc()
