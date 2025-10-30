#!/usr/bin/env python3
"""
Script de test pour le système d'assignation unique de portraits
"""
import sys
sys.path.append('/app/backend')

from services.portrait_assignment_service import PortraitAssignmentService
from services.game_service import GameService

def test_unique_assignments():
    """Test que les portraits assignés sont uniques"""
    print("🧪 TEST : Assignation unique de portraits")
    print("=" * 70)
    
    assignment_service = PortraitAssignmentService()
    
    # Test 1 : Générer 10 joueurs français
    print("\n📋 Test 1 : Générer 10 joueurs français (hommes)")
    print("-" * 70)
    
    portraits = []
    for i in range(10):
        portrait = assignment_service.get_unique_portrait("Français", "M")
        portraits.append(portrait)
        print(f"  Joueur {i+1}: {portrait}")
    
    # Vérifier l'unicité
    unique_portraits = set(portraits)
    print(f"\n✅ Résultat : {len(unique_portraits)}/10 portraits uniques")
    
    if len(unique_portraits) == 10:
        print("✅ TEST RÉUSSI : Tous les portraits sont uniques !")
    else:
        print("❌ TEST ÉCHOUÉ : Des doublons ont été détectés")
        duplicates = [p for p in portraits if portraits.count(p) > 1]
        print(f"   Doublons : {set(duplicates)}")
    
    # Test 2 : Stats d'assignation
    print("\n📋 Test 2 : Statistiques d'assignation")
    print("-" * 70)
    
    stats = assignment_service.get_assignment_stats()
    total_assigned = assignment_service.get_total_assigned()
    total_remaining = assignment_service.get_total_remaining()
    
    print(f"  Total assigné : {total_assigned}")
    print(f"  Total restant : {total_remaining}")
    print(f"  Utilisation : {(total_assigned/7200*100):.2f}%")
    
    if stats:
        print("\n  Détail par catégorie :")
        for continent, ethnicities in stats.items():
            for ethnicity, genders in ethnicities.items():
                for gender, data in genders.items():
                    if data['assigned'] > 0:
                        print(f"    {continent}/{ethnicity}/{gender}: {data['assigned']}/{data['available']} ({data['usage_percent']}%)")
    
    # Test 3 : Tester avec différentes nationalités
    print("\n📋 Test 3 : Tester avec différentes nationalités")
    print("-" * 70)
    
    test_nationalities = [
        ("Français", "M"),
        ("Chinoise", "F"),
        ("Nigérian", "M"),
        ("Américaine", "F"),
        ("Indien", "M")
    ]
    
    for nationality, gender in test_nationalities:
        portrait = assignment_service.get_unique_portrait(nationality, gender)
        continent, ethnicity = assignment_service.realistic_service.get_continent_and_ethnicity(nationality)
        print(f"  {nationality} ({gender}): {continent}/{ethnicity}")
        print(f"    → {portrait}")
    
    # Test 4 : Génération de joueurs avec GameService
    print("\n📋 Test 4 : Génération de joueurs complets")
    print("-" * 70)
    
    print("  Génération de 3 joueurs...")
    for i in range(3):
        player = GameService.generate_random_player(i+1)
        print(f"\n  Joueur {i+1}:")
        print(f"    Nom: {player.name}")
        print(f"    Nationalité: {player.nationality}")
        print(f"    Sexe: {player.gender}")
        print(f"    Portrait réaliste: {player.portrait.realistic_portrait or 'Non assigné'}")
    
    print("\n" + "=" * 70)
    print("✅ Tests terminés !")

if __name__ == "__main__":
    test_unique_assignments()
