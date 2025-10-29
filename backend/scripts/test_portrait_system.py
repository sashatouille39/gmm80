"""
Script de test du système de portraits par calques
Teste la génération et l'assemblage de quelques portraits
"""
import asyncio
import sys
import os
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from services.portrait_generator_service import PortraitGeneratorService
from dotenv import load_dotenv

load_dotenv()


async def test_portrait_system():
    """Teste le système de portraits"""
    
    service = PortraitGeneratorService()
    
    print("\n🧪 TEST DU SYSTÈME DE PORTRAITS PAR CALQUES")
    print("=" * 70)
    
    # Test 1 : Générer quelques calques de test
    print("\n📝 Test 1 : Génération de calques de test")
    print("-" * 70)
    
    test_cases = [
        ('Français', 'male', 'western_european'),
        ('Japonais', 'female', 'east_asian'),
        ('Nigérian', 'male', 'african'),
    ]
    
    for nationality, gender, expected_region in test_cases:
        print(f"\n🎯 Test : {nationality} - {gender}")
        
        # Vérifier la région
        region = service.get_region_for_nationality(nationality)
        print(f"   Région détectée : {region} (attendu: {expected_region})")
        assert region == expected_region, f"Région incorrecte : {region} != {expected_region}"
        
        # Générer un set de calques complet
        print(f"   Génération de 5 calques...")
        try:
            layers = await service.generate_portrait_layers_set(
                nationality=nationality,
                gender=gender,
                age=25,
                set_id=1,
                layer_types=['base', 'eyes', 'hair', 'mouth', 'nose']
            )
            
            print(f"   ✅ Calques générés :")
            for layer_type, path in layers.items():
                print(f"      - {layer_type}: {path}")
                # Vérifier que le fichier existe
                full_path = f"/app/backend{path}"
                if os.path.exists(full_path):
                    size = os.path.getsize(full_path)
                    print(f"        ✓ Fichier existe ({size} bytes)")
                else:
                    print(f"        ✗ Fichier manquant!")
        
        except Exception as e:
            print(f"   ❌ Erreur : {str(e)}")
    
    # Test 2 : Tester l'assemblage aléatoire
    print("\n\n📝 Test 2 : Assemblage aléatoire de calques")
    print("-" * 70)
    
    for nationality, gender, expected_region in test_cases:
        print(f"\n🎯 Assemblage : {nationality} - {gender}")
        region = service.get_region_for_nationality(nationality)
        gender_param = 'male' if gender == 'male' else 'female'
        
        assembled = service.assemble_random_layers(region, gender_param)
        
        if assembled:
            print(f"   ✅ Calques assemblés : {len(assembled)} calques")
            for layer_type, path in assembled.items():
                print(f"      - {layer_type}: ...{path[-40:]}")
        else:
            print(f"   ⚠️  Aucun calque disponible (normal si bibliothèque non générée)")
    
    # Test 3 : Tester select_random_portrait_layers (méthode principale)
    print("\n\n📝 Test 3 : Sélection finale (select_random_portrait_layers)")
    print("-" * 70)
    
    for nationality, gender, _ in test_cases:
        print(f"\n🎯 Sélection : {nationality} - {gender}")
        
        selected = service.select_random_portrait_layers(nationality, gender)
        
        if selected:
            print(f"   ✅ Portrait sélectionné : {len(selected)} calques")
            for layer_type, path in selected.items():
                if path:
                    print(f"      - {layer_type}: ...{path[-40:]}")
        else:
            print(f"   ⚠️  Fallback sur système simple (normal si bibliothèque vide)")
    
    print("\n" + "=" * 70)
    print("✨ Tests terminés !")
    print("=" * 70)


if __name__ == "__main__":
    try:
        asyncio.run(test_portrait_system())
    except Exception as e:
        print(f"\n❌ Erreur : {str(e)}")
        import traceback
        traceback.print_exc()
