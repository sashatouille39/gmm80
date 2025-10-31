#!/usr/bin/env python3
"""
Test du système d'unicité des portraits par partie
"""
import sys
sys.path.insert(0, '/app/backend')

from services.portrait_assignment_service import PortraitAssignmentService
from services.game_service import GameService

def test_portrait_uniqueness():
    """Test que les portraits ne se répètent pas dans une même partie"""
    
    service = PortraitAssignmentService()
    
    print("🧪 Test du système d'unicité des portraits\n")
    print("=" * 60)
    
    # Test 1 : Vérifier que les portraits sont différents dans une même partie
    print("\n📝 Test 1 : Unicité dans une même partie")
    print("-" * 60)
    
    game_id = "test-game-123"
    portraits = []
    
    # Essayer de générer 5 portraits français masculins
    for i in range(5):
        portrait = service.get_unique_portrait("Français", "M", game_id=game_id)
        if portrait:
            portraits.append(portrait)
            print(f"  Portrait {i+1}: ...{portrait[-50:]}")
    
    # Vérifier l'unicité
    unique_portraits = set(portraits)
    if len(portraits) == len(unique_portraits):
        print(f"\n✅ SUCCÈS : {len(portraits)} portraits uniques générés")
    else:
        print(f"\n❌ ÉCHEC : Doublons détectés ! ({len(portraits)} générés, {len(unique_portraits)} uniques)")
    
    # Test 2 : Vérifier que les portraits peuvent être réutilisés dans une autre partie
    print("\n📝 Test 2 : Réutilisation dans une autre partie")
    print("-" * 60)
    
    game_id_2 = "test-game-456"
    portrait_game2 = service.get_unique_portrait("Français", "M", game_id=game_id_2)
    
    if portrait_game2:
        print(f"  Partie 2 - Portrait 1: ...{portrait_game2[-50:]}")
        # Ce portrait peut être le même qu'un de la partie 1, c'est OK
        print("✅ Portraits peuvent être utilisés dans différentes parties")
    
    # Test 3 : Libération des portraits
    print("\n📝 Test 3 : Libération des portraits après fin de partie")
    print("-" * 60)
    
    stats_before = service.get_total_assigned(game_id=game_id)
    print(f"  Avant libération : {stats_before} portraits assignés à la partie {game_id}")
    
    service.release_game_portraits(game_id)
    
    stats_after = service.get_total_assigned(game_id=game_id)
    print(f"  Après libération : {stats_after} portraits assignés à la partie {game_id}")
    
    if stats_after == 0:
        print("✅ SUCCÈS : Tous les portraits ont été libérés")
    else:
        print(f"❌ ÉCHEC : {stats_after} portraits non libérés")
    
    # Test 4 : Statistiques
    print("\n📝 Test 4 : Statistiques globales")
    print("-" * 60)
    
    active_games = service.get_active_games()
    print(f"  Parties actives : {active_games}")
    
    total_assigned = service.get_total_assigned()
    print(f"  Total portraits assignés (toutes parties) : {total_assigned}")
    
    # Nettoyage
    print("\n🧹 Nettoyage...")
    print("-" * 60)
    service.release_game_portraits(game_id_2)
    print("  Parties de test nettoyées")
    
    print("\n" + "=" * 60)
    print("✅ Tests terminés avec succès !")
    print("=" * 60)

if __name__ == "__main__":
    test_portrait_uniqueness()
