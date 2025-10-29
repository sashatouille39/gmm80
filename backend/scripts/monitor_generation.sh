#!/bin/bash

echo "📊 MONITORING DE LA GÉNÉRATION DES CALQUES"
echo "=========================================="
echo ""

# Vérifier si le processus tourne
PID=$(cat /tmp/portrait_gen_pid.txt 2>/dev/null)
if [ -z "$PID" ]; then
    echo "❌ Pas de génération en cours"
    exit 1
fi

if ps -p $PID > /dev/null 2>&1; then
    echo "✅ Processus actif (PID: $PID)"
else
    echo "⚠️  Processus terminé ou arrêté"
fi

echo ""
echo "📈 PROGRESSION:"
echo "----------------------------------------"

# Compter les calques générés par type
BASE_COUNT=$(ls /app/backend/static/portraits/base/skin_tone_*.png 2>/dev/null | wc -l)
EYES_COUNT=$(ls /app/backend/static/portraits/eyes/eyes_*.png 2>/dev/null | wc -l)
HAIR_MALE=$(ls /app/backend/static/portraits/hair/hair_male_*.png 2>/dev/null | wc -l)
HAIR_FEMALE=$(ls /app/backend/static/portraits/hair/hair_female_*.png 2>/dev/null | wc -l)
HAIR_TOTAL=$((HAIR_MALE + HAIR_FEMALE))
MOUTH_COUNT=$(ls /app/backend/static/portraits/mouth/mouth_*.png 2>/dev/null | wc -l)
NOSE_COUNT=$(ls /app/backend/static/portraits/nose/nose_*.png 2>/dev/null | wc -l)

echo "  Bases (peau):  $BASE_COUNT/10"
echo "  Yeux:          $EYES_COUNT/18"
echo "  Cheveux:       $HAIR_TOTAL/200 (M:$HAIR_MALE F:$HAIR_FEMALE)"
echo "  Bouches:       $MOUTH_COUNT/10"
echo "  Nez:           $NOSE_COUNT/10"

TOTAL_GENERATED=$((BASE_COUNT + EYES_COUNT + HAIR_TOTAL + MOUTH_COUNT + NOSE_COUNT))
PERCENT=$((TOTAL_GENERATED * 100 / 248))

echo ""
echo "  🎯 TOTAL: $TOTAL_GENERATED/248 ($PERCENT%)"
echo ""

# Afficher les dernières lignes du log
echo "📝 DERNIÈRES LIGNES DU LOG:"
echo "----------------------------------------"
tail -15 /tmp/portrait_generation.log

echo ""
echo "💡 Commandes utiles:"
echo "  - Voir le log complet:  cat /tmp/portrait_generation.log"
echo "  - Suivre en temps réel: tail -f /tmp/portrait_generation.log"
echo "  - Arrêter la génération: kill $PID"
