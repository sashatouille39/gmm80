#!/bin/bash

echo "📊 MONITORING GÉNÉRATION OPTIMISÉE"
echo "=========================================="
echo ""

# Vérifier si le processus tourne
PID=$(cat /tmp/portrait_gen_missing_pid.txt 2>/dev/null)
if [ -z "$PID" ]; then
    echo "❌ Pas de génération en cours"
    exit 1
fi

if ps -p $PID > /dev/null 2>&1; then
    echo "✅ Processus actif (PID: $PID)"
else
    echo "⚠️  Processus terminé"
fi

echo ""
echo "📈 PROGRESSION:"
echo "----------------------------------------"

# Compter les calques générés
BASE_COUNT=$(ls /app/backend/static/portraits/base/skin_tone_*.png 2>/dev/null | wc -l)
EYES_COUNT=$(ls /app/backend/static/portraits/eyes/eyes_*.png 2>/dev/null | wc -l)
HAIR_MALE=$(ls /app/backend/static/portraits/hair/hair_male_*.png 2>/dev/null | wc -l)
HAIR_FEMALE=$(ls /app/backend/static/portraits/hair/hair_female_*.png 2>/dev/null | wc -l)
MOUTH_COUNT=$(ls /app/backend/static/portraits/mouth/mouth_*.png 2>/dev/null | wc -l)
NOSE_COUNT=$(ls /app/backend/static/portraits/nose/nose_*.png 2>/dev/null | wc -l)

echo "  Bases (peau):      $BASE_COUNT/10   $([ $BASE_COUNT -ge 10 ] && echo "✅" || echo "⏳")"
echo "  Yeux:              $EYES_COUNT/18   $([ $EYES_COUNT -ge 18 ] && echo "✅" || echo "⏳")"
echo "  Cheveux homme:     $HAIR_MALE/100  $([ $HAIR_MALE -ge 100 ] && echo "✅" || echo "⏳")"
echo "  Cheveux femme:     $HAIR_FEMALE/100  $([ $HAIR_FEMALE -ge 100 ] && echo "✅" || echo "⏳")"
echo "  Bouches:           $MOUTH_COUNT/10   $([ $MOUTH_COUNT -ge 10 ] && echo "✅" || echo "⏳")"
echo "  Nez:               $NOSE_COUNT/10   $([ $NOSE_COUNT -ge 10 ] && echo "✅" || echo "⏳")"

TOTAL_GENERATED=$((BASE_COUNT + EYES_COUNT + HAIR_MALE + HAIR_FEMALE + MOUTH_COUNT + NOSE_COUNT))
PERCENT=$((TOTAL_GENERATED * 100 / 248))

echo ""
echo "  🎯 TOTAL: $TOTAL_GENERATED/248 ($PERCENT%)"

# Barre de progression
FILLED=$((PERCENT / 2))
EMPTY=$((50 - FILLED))
printf "  ["
printf "%${FILLED}s" | tr ' ' '█'
printf "%${EMPTY}s" | tr ' ' '░'
printf "] $PERCENT%%\n"

echo ""
echo "📝 DERNIÈRES LIGNES:"
echo "----------------------------------------"
tail -10 /tmp/portrait_generation_missing.log

echo ""
echo "💡 Commandes:"
echo "  - Log complet:   cat /tmp/portrait_generation_missing.log"
echo "  - Temps réel:    tail -f /tmp/portrait_generation_missing.log"
echo "  - Arrêter:       kill $PID"
echo "  - Vérifier:      python /app/backend/scripts/verify_portrait_system.py"
