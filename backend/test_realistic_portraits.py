#!/usr/bin/env python3
"""
Script de test pour vérifier le fonctionnement des portraits réalistes
"""
import sys
import os
sys.path.insert(0, '/app/backend')

from services.realistic_portrait_service import RealisticPortraitService
from services.game_service_fixed import GameService

def test_realistic_portraits():
    """Test le service de portraits réalistes"""
    print("🧪 TEST DU SYSTÈME DE PORTRAITS RÉALISTES")
    print("=" * 70)
    
    service = RealisticPortraitService()
    
    # Test 1: Vérifier si le système est prêt
    print("\n1️⃣ Test: Système prêt ?")
    is_ready = service.is_ready()
    print(f"   ✅ Système prêt: {is_ready}")
    
    # Test 2: Statistiques
    print("\n2️⃣ Test: Statistiques des portraits")
    stats = service.get_portrait_stats()
    print(f"   📊 Total de portraits: {stats.get('total', 0)}")
    
    for continent, ethnicities in stats.items():
        if continent == 'total':
            continue
        print(f"\n   🌍 {continent.upper()}:")
        if isinstance(ethnicities, dict):
            for ethnicity, genders in ethnicities.items():
                if isinstance(genders, dict):
                    for gender, count in genders.items():
                        print(f"      - {ethnicity} ({gender}): {count} portraits")
    
    # Test 3: Sélection de portraits pour nationalités africaines
    print("\n3️⃣ Test: Sélection de portraits africains")
    african_nationalities = [
        ('Nigérian', 'M'),
        ('Nigériane', 'F'),
        ('Sénégalais', 'M'),
        ('Kényane', 'F'),
        ('Sud-Africain', 'M')
    ]
    
    for nationality, gender in african_nationalities:
        continent, ethnicity = service.get_continent_and_ethnicity(nationality)
        portrait = service.select_random_portrait(nationality, gender)
        
        if portrait:
            print(f"   ✅ {nationality} ({gender}): {portrait}")
            print(f"      → Continent: {continent}, Ethnie: {ethnicity}")
        else:
            print(f"   ⚠️  {nationality} ({gender}): Aucun portrait disponible")
    
    # Test 4: Test avec GameService
    print("\n4️⃣ Test: Génération de joueurs africains")
    game_service = GameService()
    
    # Générer quelques joueurs africains
    african_players = []
    for i in range(3):
        nationality = ['Nigérian', 'Sénégalais', 'Kényan'][i]
        gender = 'M'
        
        player_data = {
            'nationality': nationality,
            'gender': gender
        }
        
        # Simuler la génération d'un portrait
        portrait = game_service._generate_portrait(nationality, gender)
        
        print(f"\n   Joueur {i+1}: {nationality} ({gender})")
        print(f"   - Portrait réaliste: {portrait.realistic_portrait or 'Non disponible'}")
        print(f"   - Fallback calques: {portrait.layer_base or 'Non disponible'}")
        
        if portrait.realistic_portrait:
            print(f"   ✅ Utilise un portrait réaliste")
        else:
            print(f"   ⚠️  Utilise le système de calques (fallback)")
    
    print("\n" + "=" * 70)
    print("✅ Tests terminés !")
    
if __name__ == "__main__":
    test_realistic_portraits()
