#!/bin/bash
# Script d'affichage continu de la progression

clear
echo "═══════════════════════════════════════════════════════════"
echo "   GÉNÉRATION DE PORTRAITS - SUIVI EN TEMPS RÉEL"
echo "═══════════════════════════════════════════════════════════"
echo ""

while true; do
    # Effacer l'écran mais garder le titre
    tput cup 4 0
    tput ed
    
    # Afficher le monitoring
    /app/backend/scripts/monitor_hair_generation.sh
    
    # Afficher les 5 dernières lignes du log
    echo ""
    echo "📜 DERNIÈRES ACTIVITÉS:"
    echo "───────────────────────────────────────────────────────────"
    tail -5 /tmp/hair_generation.log 2>/dev/null | sed 's/^/   /'
    echo ""
    echo "🔄 Rafraîchissement automatique dans 15s... (Ctrl+C pour quitter)"
    
    sleep 15
done
