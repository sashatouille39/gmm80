"""
Test rapide : générer un joueur français et vérifier ses calques
"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from services.game_service import GameService

# Forcer la génération d'un joueur français
player = GameService.generate_random_player(1)

# Forcer nationalité française pour test
player.nationality = "Français"
player.gender = "M"

# Regénérer le portrait avec cette nationalité
from services.portrait_generator_service import portrait_service
portrait_layers = portrait_service.select_random_portrait_layers(
    nationality="Français",
    gender="M"
)

print(f"\n🎭 Joueur Test : {player.name}")
print(f"   Nationalité : {player.nationality}")
print(f"   Genre : {player.gender}")
print(f"\n📸 Calques du portrait :")
for layer_type, path in portrait_layers.items():
    status = "✅" if path else "❌"
    print(f"   {status} {layer_type:10s}: {path or 'Non disponible'}")

# Vérifier les fichiers
import os
if any(portrait_layers.values()):
    print(f"\n✨ Le système fonctionne ! Les calques sont assemblés.")
    # Vérifier qu'ils existent
    all_exist = True
    for layer_type, path in portrait_layers.items():
        if path:
            full_path = f"/app/backend{path}"
            if not os.path.exists(full_path):
                print(f"   ⚠️  Fichier manquant : {path}")
                all_exist = False
    
    if all_exist:
        print(f"   ✅ Tous les fichiers existent sur le disque")
else:
    print(f"\n⚠️  Aucun calque disponible (fallback sur système simple)")
