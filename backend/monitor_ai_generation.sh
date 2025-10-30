#!/bin/bash
# Script de monitoring pour la génération de portraits IA

echo "======================================================================"
echo "📊 MONITORING - GÉNÉRATION DE PORTRAITS PAR IA"
echo "======================================================================"
echo ""

# Vérifier si le processus est en cours
if pgrep -f "generate_ai_portraits.py" > /dev/null; then
    echo "✅ La génération est EN COURS"
    echo ""
else
    echo "⚠️ La génération ne semble pas être en cours"
    echo "   Lancez: python generate_ai_portraits.py"
    echo ""
fi

# Fonction pour compter les fichiers
count_files() {
    local dir=$1
    if [ -d "$dir" ]; then
        echo $(find "$dir" -type f -name "portrait_*.png" 2>/dev/null | wc -l)
    else
        echo "0"
    fi
}

# Compter les portraits générés par continent
portraits_dir="/app/backend/static/portraits"
echo "📂 PORTRAITS GÉNÉRÉS PAR CONTINENT:"
echo ""

total_generated=0
for continent in africa asia europe north_america south_america oceania; do
    male_count=$(count_files "$portraits_dir/$continent/male")
    female_count=$(count_files "$portraits_dir/$continent/female")
    continent_total=$((male_count + female_count))
    total_generated=$((total_generated + continent_total))
    
    # Calculer le pourcentage
    percent=$(echo "scale=1; $continent_total * 100 / 1200" | bc)
    
    # Icône de statut
    if [ "$continent_total" -ge 1200 ]; then
        status="✅"
    elif [ "$continent_total" -gt 0 ]; then
        status="🔄"
    else
        status="⏳"
    fi
    
    # Afficher avec formatage
    printf "   %s %-20s : %4d / 1200 (%5.1f%%) [%4dM + %4dF]\n" \
        "$status" "$continent" "$continent_total" "$percent" "$male_count" "$female_count"
done

echo ""
echo "────────────────────────────────────────────────────────────────────────"
printf "   📊 TOTAL : %5d / 7200 portraits " "$total_generated"

if [ "$total_generated" -ge 7200 ]; then
    echo "(100.0%)"
    echo ""
    echo "   🎉 OBJECTIF ATTEINT !"
else
    total_percent=$(echo "scale=1; $total_generated * 100 / 7200" | bc)
    echo "($total_percent%)"
fi

echo "────────────────────────────────────────────────────────────────────────"
echo ""

# Estimation du temps restant
if [ "$total_generated" -gt 0 ]; then
    # Lire la date de démarrage du premier fichier
    first_file=$(find "$portraits_dir" -name "portrait_0001.png" 2>/dev/null | head -1)
    if [ -n "$first_file" ]; then
        start_time=$(stat -c %Y "$first_file" 2>/dev/null || stat -f %m "$first_file" 2>/dev/null)
        current_time=$(date +%s)
        elapsed=$((current_time - start_time))
        
        if [ "$elapsed" -gt 0 ] && [ "$total_generated" -gt 0 ]; then
            avg_time_per_image=$((elapsed / total_generated))
            remaining_images=$((7200 - total_generated))
            estimated_remaining_sec=$((remaining_images * avg_time_per_image))
            
            elapsed_min=$((elapsed / 60))
            remaining_min=$((estimated_remaining_sec / 60))
            remaining_hours=$((remaining_min / 60))
            
            echo "⏱️ STATISTIQUES:"
            echo "   • Temps écoulé: ${elapsed_min} minutes"
            echo "   • Vitesse moyenne: ${avg_time_per_image}s par portrait"
            echo "   • Temps restant estimé: ${remaining_hours}h ${remaining_min}min"
            echo ""
        fi
    fi
fi

# Dernières lignes du log
log_file="/tmp/ai_portraits_full.log"
if [ -f "$log_file" ]; then
    echo "📝 DERNIÈRES LIGNES DU LOG:"
    echo ""
    tail -5 "$log_file" | sed 's/^/   /'
    echo ""
fi

echo "======================================================================"
echo ""
echo "Commandes utiles:"
echo "   • Voir les logs complets: tail -f /tmp/ai_portraits_full.log"
echo "   • Relancer ce monitoring: bash monitor_ai_generation.sh"
echo "   • Arrêter la génération: pkill -f generate_ai_portraits"
echo "   • Voir une image: ls -lh $portraits_dir/africa/male/portrait_0001.png"
echo ""
