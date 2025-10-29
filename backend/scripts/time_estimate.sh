#!/bin/bash
# Script d'estimation du temps restant

PORTRAIT_DIR="/app/backend/static/portraits"
HAIR=$(ls -1 "$PORTRAIT_DIR/hair" 2>/dev/null | wc -l)
HAIR_REMAINING=$((200 - HAIR))

# Vitesse estimée: ~17 secondes par cheveu
SECONDS_PER_HAIR=17
TOTAL_SECONDS=$((HAIR_REMAINING * SECONDS_PER_HAIR))
MINUTES=$((TOTAL_SECONDS / 60))

echo "⏱️  ESTIMATION TEMPS RESTANT"
echo "=============================="
printf "Cheveux actuels:  %d/200\n" $HAIR
printf "Cheveux restants: %d\n" $HAIR_REMAINING
printf "Temps estimé:     ~%d minutes\n" $MINUTES
echo ""
echo "💡 La génération se poursuit automatiquement en arrière-plan"
