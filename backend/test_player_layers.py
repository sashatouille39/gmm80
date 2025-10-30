"""
Script de test pour vérifier que les joueurs générés ont bien des calques de portraits
"""
import sys
sys.path.insert(0, '/app/backend')

from services.game_service import GameService
import json

print("=" * 80)
print("🧪 TEST DE GÉNÉRATION DE JOUEURS AVEC CALQUES")
print("=" * 80)

# Générer 5 joueurs de différentes nationalités
print("\n📸 Génération de 5 joueurs de test...\n")

test_nationalities = ['Suédois', 'Japonais', 'Nigérian', 'Français', 'Brésilien']

for i, nationality in enumerate(test_nationalities, 1):
    print(f"\n{i}. Joueur {nationality}:")
    print("-" * 60)
    
    # Créer un joueur avec nationality fixe pour tester
    player = GameService.generate_random_player(i)
    # Forcer la nationalité pour tester
    player.nationality = nationality
    gender = 'M' if i % 2 == 1 else 'F'
    player.gender = gender
    
    # Régénérer le portrait avec la nationalité correcte
    player.portrait = GameService._generate_portrait(nationality, gender)
    
    print(f"   Nom: {player.name}")
    print(f"   Nationalité: {player.nationality}")
    print(f"   Genre: {'Homme' if player.gender == 'M' else 'Femme'}")
    print(f"   \n   Portrait:")
    print(f"      - Face: {player.portrait.face_shape}")
    print(f"      - Skin: {player.portrait.skin_color}")
    print(f"      - Hairstyle: {player.portrait.hairstyle}")
    print(f"      - Hair color: {player.portrait.hair_color}")
    print(f"      - Eye color: {player.portrait.eye_color}")
    print(f"      - Eye shape: {player.portrait.eye_shape}")
    print(f"   \n   Calques PNG:")
    print(f"      - Base: {player.portrait.layer_base or '❌ NON GÉNÉRÉ'}")
    print(f"      - Eyes: {player.portrait.layer_eyes or '❌ NON GÉNÉRÉ'}")
    print(f"      - Hair: {player.portrait.layer_hair or '❌ NON GÉNÉRÉ'}")
    print(f"      - Mouth: {player.portrait.layer_mouth or '❌ NON GÉNÉRÉ'}")
    print(f"      - Nose: {player.portrait.layer_nose or '❌ NON GÉNÉRÉ'}")
    
    has_all_layers = all([
        player.portrait.layer_base,
        player.portrait.layer_eyes,
        player.portrait.layer_hair,
        player.portrait.layer_mouth,
        player.portrait.layer_nose
    ])
    
    if has_all_layers:
        print(f"   ✅ TOUS LES CALQUES PRÉSENTS")
    else:
        print(f"   ⚠️  CALQUES MANQUANTS")

print("\n" + "=" * 80)
print("✅ TEST TERMINÉ!")
print("=" * 80)
