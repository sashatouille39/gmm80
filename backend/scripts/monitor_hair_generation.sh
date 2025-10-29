#!/bin/bash
# Script de monitoring de la génération des cheveux

echo "=== MONITORING GÉNÉRATION CHEVEUX ==="
echo ""

# Vérifier si le processus tourne
if [ -f /tmp/portrait_hair_gen_pid.txt ]; then
    PID=$(cat /tmp/portrait_hair_gen_pid.txt)
    if ps -p $PID > /dev/null 2>&1; then
        echo "✅ Processus actif (PID: $PID)"
        echo ""
    else
        echo "❌ Processus terminé (PID: $PID)"
        echo ""
    fi
else
    echo "ℹ️  Aucun processus en cours"
    echo ""
fi

# Compter les fichiers
echo "📊 PROGRESSION ACTUELLE:"
echo "------------------------"

for category in base eyes hair_male hair_female mouth nose; do
    count=$(ls -1 /app/backend/static/portraits/$category/*.png 2>/dev/null | wc -l)
    
    case $category in
        base)
            target=10
            ;;
        hair_male|hair_female)
            target=100
            ;;
        *)
            target=10
            ;;
    esac
    
    percent=$((count * 100 / target))
    printf "%-15s: %3d/%3d (%3d%%) " "$category" "$count" "$target" "$percent"
    
    # Barre de progression
    bars=$((percent / 5))
    printf "["
    for i in $(seq 1 20); do
        if [ $i -le $bars ]; then
            printf "█"
        else
            printf "░"
        fi
    done
    printf "]\n"
done

echo ""
echo "📈 TOTAL: $(ls -1 /app/backend/static/portraits/*/*.png 2>/dev/null | wc -l) fichiers générés"
echo ""

# Estimation du nombre de combinaisons possibles
base=$(ls -1 /app/backend/static/portraits/base/*.png 2>/dev/null | wc -l)
eyes=$(ls -1 /app/backend/static/portraits/eyes/*.png 2>/dev/null | wc -l)
hair_male=$(ls -1 /app/backend/static/portraits/hair_male/*.png 2>/dev/null | wc -l)
hair_female=$(ls -1 /app/backend/static/portraits/hair_female/*.png 2>/dev/null | wc -l)
mouth=$(ls -1 /app/backend/static/portraits/mouth/*.png 2>/dev/null | wc -l)
nose=$(ls -1 /app/backend/static/portraits/nose/*.png 2>/dev/null | wc -l)

if [ $hair_male -gt 0 ]; then
    combos_male=$((base * eyes * hair_male * mouth * nose))
    echo "🎭 Combinaisons homme possibles: $(printf "%'d" $combos_male)"
fi

if [ $hair_female -gt 0 ]; then
    combos_female=$((base * eyes * hair_female * mouth * nose))
    echo "🎭 Combinaisons femme possibles: $(printf "%'d" $combos_female)"
fi

echo ""
echo "💡 Rafraîchir: watch -n 10 /app/backend/scripts/monitor_hair_generation.sh"
