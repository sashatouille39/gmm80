#!/bin/bash
# Script de vérification finale de la collection de portraits réalistes

echo "🔍 VÉRIFICATION COMPLÈTE DE LA COLLECTION DE PORTRAITS"
echo "======================================================"
echo ""

# Variables
BASE_DIR="/app/backend/static/realistic_portraits"
TOTAL_EXPECTED=7200
CONTINENTS=("africa" "asia" "europe" "america" "middle_east" "oceania")
EXPECTED_PER_CONTINENT=1200

# Compteurs
total_portraits=0
continents_ok=0
continents_ko=0

# Vérifier chaque continent
echo "📊 VÉRIFICATION PAR CONTINENT"
echo "------------------------------"

for continent in "${CONTINENTS[@]}"; do
    count=$(find "$BASE_DIR/$continent" -type f 2>/dev/null | wc -l)
    total_portraits=$((total_portraits + count))
    
    if [ $count -eq $EXPECTED_PER_CONTINENT ]; then
        echo "✅ $continent: $count/$EXPECTED_PER_CONTINENT"
        continents_ok=$((continents_ok + 1))
    else
        echo "❌ $continent: $count/$EXPECTED_PER_CONTINENT"
        continents_ko=$((continents_ko + 1))
    fi
done

echo ""
echo "📈 RÉSUMÉ GLOBAL"
echo "------------------------------"
echo "Total de portraits : $total_portraits/$TOTAL_EXPECTED"

if [ $total_portraits -eq $TOTAL_EXPECTED ]; then
    echo "✅ Collection complète !"
else
    echo "⚠️  Il manque $((TOTAL_EXPECTED - total_portraits)) portrait(s)"
fi

echo "Continents OK : $continents_ok/6"
echo "Continents KO : $continents_ko/6"

echo ""
echo "🔎 VÉRIFICATION DÉTAILLÉE PAR ETHNIE/GENRE"
echo "-------------------------------------------"

# Fonction pour vérifier un dossier
check_folder() {
    local continent=$1
    local ethnicity=$2
    local gender=$3
    local expected=$4
    
    local folder_path="$BASE_DIR/$continent/$ethnicity/$gender"
    
    if [ -d "$folder_path" ]; then
        local count=$(ls "$folder_path" | wc -l)
        if [ $count -eq $expected ]; then
            echo "  ✅ $continent/$ethnicity/$gender: $count/$expected"
        else
            echo "  ⚠️  $continent/$ethnicity/$gender: $count/$expected"
            # Lister les fichiers manquants
            for i in $(seq 1 $expected); do
                age1_file=$(printf "$folder_path/${continent}_${ethnicity}_${gender}_21_35_%04d.jpg" $i)
                age2_file=$(printf "$folder_path/${continent}_${ethnicity}_${gender}_34_50_%04d.jpg" $i)
                if [ ! -f "$age1_file" ] && [ ! -f "$age2_file" ]; then
                    echo "      ❌ Fichier #$i manquant"
                fi
            done
        fi
    else
        echo "  ❌ $continent/$ethnicity/$gender: Dossier manquant !"
    fi
}

# Afrique
echo "🌍 AFRIQUE"
check_folder "africa" "black" "M" 600
check_folder "africa" "black" "F" 600

# Asie
echo "🌏 ASIE"
check_folder "asia" "asian" "M" 350
check_folder "asia" "asian" "F" 350
check_folder "asia" "indian" "M" 250
check_folder "asia" "indian" "F" 250

# Europe
echo "🌍 EUROPE"
check_folder "europe" "white" "M" 600
check_folder "europe" "white" "F" 600

# Amérique
echo "🌎 AMÉRIQUE"
check_folder "america" "latino_hispanic" "M" 350
check_folder "america" "latino_hispanic" "F" 350
check_folder "america" "white" "M" 250
check_folder "america" "white" "F" 250

# Moyen-Orient
echo "🌍 MOYEN-ORIENT"
check_folder "middle_east" "middle_eastern" "M" 600
check_folder "middle_east" "middle_eastern" "F" 600

# Océanie
echo "🌏 OCÉANIE"
check_folder "oceania" "white" "M" 600
check_folder "oceania" "white" "F" 600

echo ""
echo "💾 STATISTIQUES D'ESPACE DISQUE"
echo "--------------------------------"
total_size=$(du -sh "$BASE_DIR" 2>/dev/null | cut -f1)
echo "Taille totale : $total_size"

avg_size=$(find "$BASE_DIR" -type f -exec ls -l {} \; 2>/dev/null | awk '{sum+=$5; count++} END {printf "%.0f KB", sum/count/1024}')
echo "Taille moyenne par portrait : $avg_size"

echo ""
if [ $total_portraits -eq $TOTAL_EXPECTED ] && [ $continents_ko -eq 0 ]; then
    echo "🎉 VÉRIFICATION RÉUSSIE : Collection complète et conforme !"
    exit 0
else
    echo "⚠️  VÉRIFICATION ÉCHOUÉE : Des portraits manquent ou sont mal organisés"
    exit 1
fi
