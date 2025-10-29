"""
Script pour générer rapidement des portraits simples avec Pillow
Pour tester l'affichage pendant que la génération IA se fait
"""
import os
import sys

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.simple_portrait_generator import simple_portrait_gen
from services.portrait_generator_service import portrait_service

def generate_simple_portraits():
    """Génère des portraits simples pour les tests"""
    
    print("=" * 80)
    print("🎨 GÉNÉRATEUR RAPIDE DE PORTRAITS SIMPLES (Pillow)")
    print("=" * 80)
    print("\n📊 Génération de 6 portraits de test avec calques simples")
    print("   ⚡ Instantané (pas de délai d'IA)\n")
    print("=" * 80)
    
    # Nationalités de test avec leurs régions
    test_cases = [
        ('Suédois', 'nordic', 'M', '#F5E6D3', '#E6C266', '#4169E1', '🇸🇪 Homme suédois'),
        ('Suédois', 'nordic', 'F', '#F5E6D3', '#E6C266', '#87CEEB', '🇸🇪 Femme suédoise'),
        ('Japonais', 'east_asian', 'M', '#F5D5B3', '#000000', '#654321', '🇯🇵 Homme japonais'),
        ('Japonais', 'east_asian', 'F', '#F5D5B3', '#000000', '#654321', '🇯🇵 Femme japonaise'),
        ('Nigérian', 'african', 'M', '#8B4513', '#000000', '#654321', '🇳🇬 Homme nigérian'),
        ('Nigérian', 'african', 'F', '#8B4513', '#000000', '#654321', '🇳🇬 Femme nigériane'),
    ]
    
    total_generated = 0
    
    for nationality, region, gender, skin_color, hair_color, eye_color, label in test_cases:
        print(f"\n📸 {label}")
        
        try:
            # Générer le portrait simple
            layers = simple_portrait_gen.generate_complete_portrait(
                nationality=nationality,
                region=region,
                gender=gender,
                skin_color=skin_color,
                hair_color=hair_color,
                eye_color=eye_color,
                eye_shape='Amande',
                set_id=1
            )
            
            if layers:
                print(f"   ✅ Portrait généré avec {len(layers)} calques")
                for layer_type, path in layers.items():
                    print(f"      • {layer_type}: {path}")
                total_generated += 1
            else:
                print(f"   ❌ Échec de la génération")
                
        except Exception as e:
            print(f"   ❌ Erreur: {str(e)}")
            continue
    
    print(f"\n{'='*80}")
    print("🎉 GÉNÉRATION RAPIDE TERMINÉE!")
    print(f"{'='*80}")
    print(f"✅ Portraits générés avec succès: {total_generated}/{len(test_cases)}")
    print(f"\n📁 Emplacement: /app/backend/static/portraits/")
    print(f"\n💡 Portraits simples prêts pour les tests!")
    print(f"   Vous pouvez maintenant lancer la génération IA pour de meilleurs résultats:")
    print(f"   python generate_demo_portraits.py")
    print("=" * 80)


if __name__ == "__main__":
    print("🎨 Générateur rapide de portraits simples\n")
    generate_simple_portraits()
