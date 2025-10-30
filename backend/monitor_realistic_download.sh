#!/bin/bash
# Script de monitoring pour suivre la progression du téléchargement

PORTRAITS_DIR="/app/backend/static/realistic_portraits"
PROGRESS_FILE="/tmp/portrait_download_progress.json"

echo "📊 MONITORING DU TÉLÉCHARGEMENT DE PORTRAITS"
echo "=============================================="
echo ""

# Fonction pour compter les fichiers
count_files() {
    local dir=$1
    if [ -d "$dir" ]; then
        find "$dir" -type f \( -name "*.jpg" -o -name "*.png" \) 2>/dev/null | wc -l
    else
        echo "0"
    fi
}

# Boucle de monitoring
while true; do
    clear
    echo "📊 MONITORING DU TÉLÉCHARGEMENT - $(date '+%H:%M:%S')"
    echo "=============================================="
    echo ""
    
    # Compter par continent
    total=0
    for continent in africa asia europe america middle_east oceania; do
        if [ -d "$PORTRAITS_DIR/$continent" ]; then
            count=$(count_files "$PORTRAITS_DIR/$continent")
            total=$((total + count))
            percentage=$((count * 100 / 1200))
            
            # Barre de progression
            bar_length=30
            filled=$((percentage * bar_length / 100))
            bar=$(printf "█%.0s" $(seq 1 $filled))
            empty=$(printf "░%.0s" $(seq 1 $((bar_length - filled))))
            
            echo "🌍 $(printf '%-15s' $continent) : $count/1200 [$bar$empty] $percentage%"
        else
            echo "🌍 $(printf '%-15s' $continent) : 0/1200 [░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░] 0%"
        fi
    done
    
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📈 TOTAL: $total/7200 ($(($total * 100 / 7200))%)"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    # Progression JSON
    if [ -f "$PROGRESS_FILE" ]; then
        echo ""
        echo "📋 Détails de progression :"
        python3 -c "
import json
import sys
try:
    with open('$PROGRESS_FILE', 'r') as f:
        data = json.load(f)
        for key, value in sorted(data.items()):
            print(f'  ✓ {key}: {value}')
except:
    pass
" 2>/dev/null
    fi
    
    echo ""
    echo "⏱️  Mise à jour toutes les 15 secondes (Ctrl+C pour quitter)"
    
    sleep 15
done
