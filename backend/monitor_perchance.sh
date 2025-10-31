#!/bin/bash
# Script de monitoring du téléchargement Perchance

echo "📊 MONITORING DU TÉLÉCHARGEMENT PERCHANCE"
echo "=========================================="
echo ""

# Vérifier si le processus tourne
if ps aux | grep -v grep | grep "download_perchance_portraits_v2.py" > /dev/null; then
    PID=$(ps aux | grep -v grep | grep "download_perchance_portraits_v2.py" | awk '{print $2}')
    echo "✅ Script en cours d'exécution (PID: $PID)"
else
    echo "❌ Script non actif"
fi

echo ""
echo "📂 Fichiers téléchargés:"
echo "----------------------------------------"
TARGET_DIR="/app/backend/static/realistic_portraits/asia/asian/M"
PERCHANCE_FILES=$(ls -1 "$TARGET_DIR"/perchance_*.jpg 2>/dev/null | wc -l)
echo "   Fichiers Perchance: $PERCHANCE_FILES"

if [ $PERCHANCE_FILES -gt 0 ]; then
    echo ""
    echo "📊 Répartition par âge:"
    for age in 20 30 40; do
        COUNT=$(ls -1 "$TARGET_DIR"/perchance_asia_asian_M_${age}_*.jpg 2>/dev/null | wc -l)
        echo "   Âge $age ans: $COUNT images"
    done
    
    echo ""
    echo "📁 Derniers fichiers créés:"
    ls -lht "$TARGET_DIR"/perchance_*.jpg 2>/dev/null | head -5 | awk '{print "   "$9" ("$5")"}'
fi

echo ""
echo "📄 Dernières lignes du log:"
echo "----------------------------------------"
tail -20 /app/backend/perchance_download.log 2>/dev/null || echo "   (Aucun log disponible)"

echo ""
echo "=========================================="
echo "💡 Commandes utiles:"
echo "   - Voir log complet: tail -f /app/backend/perchance_download.log"
echo "   - Arrêter le script: kill $PID"
echo "   - Relancer monitoring: bash $0"
