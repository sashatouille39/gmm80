#!/bin/bash
# Script de statut rapide de la génération

PORTRAIT_DIR="/app/backend/static/portraits"

# Compter les fichiers
BASE=$(ls -1 "$PORTRAIT_DIR/base" 2>/dev/null | wc -l)
EYES=$(ls -1 "$PORTRAIT_DIR/eyes" 2>/dev/null | wc -l)
HAIR=$(ls -1 "$PORTRAIT_DIR/hair" 2>/dev/null | wc -l)
MOUTH=$(ls -1 "$PORTRAIT_DIR/mouth" 2>/dev/null | wc -l)
NOSE=$(ls -1 "$PORTRAIT_DIR/nose" 2>/dev/null | wc -l)
TOTAL=$((BASE + EYES + HAIR + MOUTH + NOSE))

echo "📊 PROGRESSION RAPIDE"
echo "===================="
printf "Bases:   %3d/10   %s\n" $BASE "$([ $BASE -ge 10 ] && echo '✅' || echo '⏳')"
printf "Yeux:    %3d/18   %s\n" $EYES "$([ $EYES -ge 18 ] && echo '✅' || echo '⏳')"
printf "Cheveux: %3d/200  %s\n" $HAIR "$([ $HAIR -ge 200 ] && echo '✅' || echo '⏳')"
printf "Bouches: %3d/10   %s\n" $MOUTH "$([ $MOUTH -ge 10 ] && echo '✅' || echo '⏳')"
printf "Nez:     %3d/10   %s\n" $NOSE "$([ $NOSE -ge 10 ] && echo '✅' || echo '⏳')"
echo "--------------------"
printf "TOTAL:   %3d/248 (%d%%)\n" $TOTAL $((TOTAL * 100 / 248))

# Dernière ligne du log
if [ -f "/tmp/portrait_generation_missing.log" ]; then
    echo ""
    echo "📝 Dernière activité:"
    tail -3 /tmp/portrait_generation_missing.log | grep -E "HOMME|FEMME" | tail -1
fi
