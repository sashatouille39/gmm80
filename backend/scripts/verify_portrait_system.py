"""
Script de vérification du système de portraits une fois les calques générés
"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from services.portrait_generator_service import PortraitGeneratorService


def verify_library():
    """Vérifie que la bibliothèque de calques est complète"""
    
    print("\n🔍 VÉRIFICATION DE LA BIBLIOTHÈQUE DE CALQUES")
    print("=" * 70)
    
    service = PortraitGeneratorService()
    base_path = Path(service.base_path)
    
    # Vérifier chaque type de calque
    results = {}
    
    print("\n📂 INVENTAIRE DES CALQUES:")
    print("-" * 70)
    
    # Bases (teintes de peau)
    base_dir = base_path / 'base'
    base_files = list(base_dir.glob('skin_tone_*.png'))
    results['base'] = len(base_files)
    status = "✅" if results['base'] >= 8 else "⚠️"
    print(f"  {status} Bases (peau):  {results['base']}/10")
    
    # Yeux (formes et couleurs)
    eyes_dir = base_path / 'eyes'
    eyes_files = list(eyes_dir.glob('eyes_*.png'))
    results['eyes'] = len(eyes_files)
    status = "✅" if results['eyes'] >= 15 else "⚠️"
    print(f"  {status} Yeux:          {results['eyes']}/18")
    
    # Cheveux
    hair_dir = base_path / 'hair'
    male_hair = list(hair_dir.glob('hair_male_*.png'))
    female_hair = list(hair_dir.glob('hair_female_*.png'))
    results['hair_male'] = len(male_hair)
    results['hair_female'] = len(female_hair)
    results['hair_total'] = results['hair_male'] + results['hair_female']
    status = "✅" if results['hair_total'] >= 160 else "⚠️"
    print(f"  {status} Cheveux:       {results['hair_total']}/200")
    print(f"       - Homme:      {results['hair_male']}/100")
    print(f"       - Femme:      {results['hair_female']}/100")
    
    # Bouches
    mouth_dir = base_path / 'mouth'
    mouth_files = list(mouth_dir.glob('mouth_*.png'))
    results['mouth'] = len(mouth_files)
    status = "✅" if results['mouth'] >= 8 else "⚠️"
    print(f"  {status} Bouches:       {results['mouth']}/10")
    
    # Nez
    nose_dir = base_path / 'nose'
    nose_files = list(nose_dir.glob('nose_*.png'))
    results['nose'] = len(nose_files)
    status = "✅" if results['nose'] >= 8 else "⚠️"
    print(f"  {status} Nez:           {results['nose']}/10")
    
    # Total
    total = results['base'] + results['eyes'] + results['hair_total'] + results['mouth'] + results['nose']
    percentage = (total / 248) * 100
    
    print("\n" + "-" * 70)
    print(f"  🎯 TOTAL: {total}/248 ({percentage:.1f}%)")
    
    # Calculer les combinaisons possibles
    if total > 0:
        combinations = (
            max(results['base'], 1) *
            max(results['eyes'], 1) *
            max(results['hair_total'], 1) *
            max(results['mouth'], 1) *
            max(results['nose'], 1)
        )
        print(f"  🎲 COMBINAISONS POSSIBLES: {combinations:,}")
    
    print("\n" + "=" * 70)
    
    # Verdict final
    if percentage >= 80:
        print("✅ SUCCÈS! La bibliothèque de calques est complète!")
        print("   Le système peut générer des centaines de milliers de portraits uniques.")
        return True
    elif percentage >= 50:
        print("⚠️  PARTIEL: La bibliothèque est utilisable mais incomplète.")
        print("   Le système fonctionnera avec moins de variété.")
        return True
    else:
        print("❌ INSUFFISANT: Trop peu de calques générés.")
        print("   Relancer la génération ou vérifier les erreurs.")
        return False


def test_assembly():
    """Test l'assemblage aléatoire d'un portrait"""
    
    print("\n🧪 TEST D'ASSEMBLAGE DE PORTRAIT")
    print("=" * 70)
    
    service = PortraitGeneratorService()
    
    # Tester quelques régions
    test_cases = [
        ('western_european', 'male', 'Français homme'),
        ('western_european', 'female', 'Français femme'),
        ('east_asian', 'male', 'Japonais homme'),
        ('african', 'female', 'Nigérienne femme'),
    ]
    
    print("\n🎨 ASSEMBLAGE DE PORTRAITS TEST:")
    print("-" * 70)
    
    success = 0
    for region, gender, description in test_cases:
        try:
            portrait = service.select_random_portrait_layers(region, gender)
            
            # Vérifier que tous les calques sont présents
            required_keys = ['base', 'eyes', 'hair', 'mouth', 'nose']
            has_all = all(portrait.get(key) for key in required_keys)
            
            if has_all:
                print(f"  ✅ {description}: OK")
                success += 1
            else:
                missing = [k for k in required_keys if not portrait.get(k)]
                print(f"  ⚠️  {description}: Calques manquants - {missing}")
                
        except Exception as e:
            print(f"  ❌ {description}: Erreur - {str(e)}")
    
    print("\n" + "-" * 70)
    print(f"  🎯 RÉSULTAT: {success}/{len(test_cases)} portraits assemblés avec succès")
    
    return success == len(test_cases)


if __name__ == "__main__":
    print("\n" + "🎨" * 35)
    print("  VÉRIFICATION DU SYSTÈME DE PORTRAITS")
    print("🎨" * 35)
    
    # Vérifier la bibliothèque
    library_ok = verify_library()
    
    # Tester l'assemblage
    assembly_ok = test_assembly()
    
    print("\n" + "=" * 70)
    if library_ok and assembly_ok:
        print("🎉 SYSTÈME DE PORTRAITS COMPLÈTEMENT FONCTIONNEL!")
        print("   Les joueurs du jeu auront maintenant des portraits uniques.")
    elif library_ok:
        print("⚠️  SYSTÈME OPÉRATIONNEL avec quelques limitations.")
    else:
        print("❌ PROBLÈME DÉTECTÉ - Vérifier les logs de génération.")
    print("=" * 70 + "\n")
    
    sys.exit(0 if (library_ok and assembly_ok) else 1)
