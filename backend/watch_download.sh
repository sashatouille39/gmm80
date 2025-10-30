#!/bin/bash
echo "🔄 Monitoring automatique lancé (rafraîchissement toutes les 30s)"
echo "Appuyez sur Ctrl+C pour arrêter"
echo ""

while true; do
    clear
    /app/backend/monitor_progress.sh
    echo ""
    echo "⏰ Prochaine mise à jour dans 30 secondes..."
    sleep 30
done
