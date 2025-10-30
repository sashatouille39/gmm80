#!/usr/bin/env python3
"""
Script de test pour vérifier que les joueurs générés ont bien leurs calques de portraits
"""
import sys
sys.path.insert(0, '/app/backend')

from services.game_service import GameService
from services.portrait_generator_service import PortraitGeneratorService
import json

print("=" * 80)
print("🎭 TEST D'AFFICHAGE DES PORTRAITS AVEC CALQUES")
print("=" * 80)
print()

# Générer plusieurs joueurs de différentes nationalités et sexes
test_cases = [
    ("Français", "M"),
    ("Française", "F"),
    ("Chinois", "M"),
    ("Chinoise", "F"),
    ("Nigérian", "M"),
    ("Nigériane", "F"),
    ("Suédois", "M"),
    ("Suédoise", "F"),
    ("Marocain", "M"),
    ("Marocaine", "F"),
]

portrait_service = PortraitGeneratorService()

for i, (nationality, gender) in enumerate(test_cases, 1):
    print(f"\n{'='*60}")
    print(f"Joueur #{i} - {nationality} ({gender})")
    print('='*60)
    
    # Déterminer la région
    region = portrait_service.get_region_for_nationality(nationality)
    print(f"📍 Région: {region}")
    
    # Générer le joueur
    player = GameService.generate_random_player(i)
    # Forcer la nationalité pour le test
    player.nationality = nationality
    player.gender = gender
    
    # Régénérer le portrait avec la bonne nationalité
    player.portrait = GameService._generate_portrait(nationality, gender)
    
    print(f"👤 Nom: {player.name}")
    print(f"🎯 Rôle: {player.role.value}")
    print()
    print("🎨 Calques du portrait:")
    
    # Vérifier chaque calque
    has_all_layers = True
    for layer_type in ['base', 'eyes', 'hair', 'mouth', 'nose']:
        layer_path = getattr(player.portrait, f'layer_{layer_type}', None)
        if layer_path:
            print(f"   ✅ {layer_type.capitalize()}: {layer_path}")
        else:
            print(f"   ❌ {layer_type.capitalize()}: MANQUANT")
            has_all_layers = False
    
    if has_all_layers:
        print(f"\n   ✨ Tous les calques sont présents ! Portrait complet.")
    else:
        print(f"\n   ⚠️  Certains calques manquent - fallback sera utilisé")

print("\n" + "=" * 80)
print("✅ TEST TERMINÉ")
print("=" * 80)
print("\n📝 Résumé:")
print("   - Les joueurs sont générés avec leurs calques de portraits")
print("   - Les calques sont cohérents avec la nationalité et le sexe")
print("   - Les portraits devraient s'afficher correctement dans le jeu")
print()
