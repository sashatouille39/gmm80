#!/bin/bash
# Script pour surveiller la progression de la génération de portraits

echo "======================================================================"
echo "📊 MONITORING - GÉNÉRATION DE PORTRAITS"
echo "======================================================================"
echo ""

# Fonction pour compter les fichiers
count_files() {
    local dir=$1
    if [ -d "$dir" ]; then
        echo $(find "$dir" -type f -name "*.jpg" 2>/dev/null | wc -l)
    else
        echo "0"
    fi
}

# Vérifier si le processus est en cours
if pgrep -f "generate_portraits_pipeline" > /dev/null; then
    echo "✅ Le pipeline est EN COURS D'EXÉCUTION"
    echo ""
else
    echo "⚠️ Le pipeline ne semble pas être en cours"
    echo ""
fi

# Compter les images téléchargées
temp_dir="/app/backend/static/portraits/temp"
temp_count=$(count_files "$temp_dir")
echo "📥 ÉTAPE 1 - Téléchargement:"
echo "   Images téléchargées: $temp_count / 12000"
if [ "$temp_count" -ge 12000 ]; then
    echo "   ✅ Téléchargement terminé"
elif [ "$temp_count" -gt 0 ]; then
    echo "   🔄 En cours... ($(echo "scale=1; $temp_count * 100 / 12000" | bc)%)"
else
    echo "   ⏳ Pas encore démarré"
fi
echo ""

# Vérifier la classification
classification_file="/app/backend/static/portraits/classification_results.json"
if [ -f "$classification_file" ]; then
    classified=$(grep -o '"file"' "$classification_file" | wc -l)
    echo "🔍 ÉTAPE 2 - Classification:"
    echo "   Images classifiées: $classified / $temp_count"
    if [ "$classified" -eq "$temp_count" ] && [ "$temp_count" -gt 0 ]; then
        echo "   ✅ Classification terminée"
    elif [ "$classified" -gt 0 ]; then
        echo "   🔄 En cours... ($(echo "scale=1; $classified * 100 / $temp_count" | bc)%)"
    fi
else
    echo "🔍 ÉTAPE 2 - Classification:"
    echo "   ⏳ Pas encore démarrée"
fi
echo ""

# Compter les images finales par continent
final_dir="/app/backend/static/portraits"
echo "📂 ÉTAPE 3 - Images finales:"

total_final=0
for continent in africa asia europe north_america south_america oceania; do
    male_count=$(count_files "$final_dir/$continent/male")
    female_count=$(count_files "$final_dir/$continent/female")
    continent_total=$((male_count + female_count))
    total_final=$((total_final + continent_total))
    
    if [ "$continent_total" -gt 0 ]; then
        echo "   $continent: $continent_total / 1200 (${male_count}M, ${female_count}F)"
    fi
done

if [ "$total_final" -gt 0 ]; then
    echo ""
    echo "   📊 TOTAL: $total_final / 7200 images"
    if [ "$total_final" -ge 7200 ]; then
        echo "   🎉 TERMINÉ !"
    else
        echo "   🔄 En cours... ($(echo "scale=1; $total_final * 100 / 7200" | bc)%)"
    fi
else
    echo "   ⏳ Pas encore démarrée"
fi

echo ""
echo "======================================================================"
echo ""
echo "Commandes utiles:"
echo "   • Voir les logs: tail -f /app/backend/logs/portraits_pipeline.log"
echo "   • Relancer ce monitoring: bash monitor_portraits.sh"
echo "   • Arrêter le pipeline: pkill -f generate_portraits_pipeline"
echo ""
