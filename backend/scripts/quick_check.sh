#!/bin/bash
# Quick check - résumé rapide de la progression

if [ -f /tmp/portrait_hair_gen_pid.txt ]; then
    PID=$(cat /tmp/portrait_hair_gen_pid.txt)
    if ps -p $PID > /dev/null 2>&1; then
        STATUS="🟢 EN COURS"
    else
        STATUS="🔴 TERMINÉ"
    fi
else
    STATUS="⚪ ARRÊTÉ"
fi

hair_male=$(ls -1 /app/backend/static/portraits/hair_male/*.png 2>/dev/null | wc -l)
hair_female=$(ls -1 /app/backend/static/portraits/hair_female/*.png 2>/dev/null | wc -l)
total_hair=$((hair_male + hair_female))

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  GÉNÉRATION CHEVEUX - STATUT"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Status: $STATUS"
echo ""
echo "Cheveux homme:  $hair_male/100 ($(( hair_male * 100 / 100 ))%)"
echo "Cheveux femme:  $hair_female/100 ($(( (hair_female > 0 ? hair_female : 1) * 100 / 100 ))%)"
echo "Total généré:   $total_hair/200"
echo ""

if [ $total_hair -gt 0 ]; then
    # Estimer le temps restant
    if [ -f /tmp/hair_generation.log ]; then
        # Chercher le premier timestamp
        start_time=$(grep "Démarrage:" /tmp/hair_generation.log | head -1 | awk '{print $3}')
        if [ ! -z "$start_time" ]; then
            # Calculer le temps écoulé approximativement
            elapsed_min=$((total_hair * 20 / 60))  # ~20 sec par image
            remaining=$((200 - total_hair))
            eta_min=$((remaining * 20 / 60))
            
            echo "⏱️  Temps écoulé: ~${elapsed_min} min"
            echo "⏳ Temps restant: ~${eta_min} min"
        fi
    fi
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "💡 Commandes disponibles:"
echo "   • Détails:   /app/backend/scripts/monitor_hair_generation.sh"
echo "   • Live:      /app/backend/scripts/watch_generation.sh"
echo "   • Logs:      tail -f /tmp/hair_generation.log"
