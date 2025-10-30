#!/bin/bash
# Script de vérification rapide du système de portraits réalistes

echo "========================================"
echo "🔍 VÉRIFICATION SYSTÈME PORTRAITS"
echo "========================================"
echo ""

# 1. Vérifier le nombre de portraits téléchargés
echo "📊 1. Comptage des portraits téléchargés"
echo "----------------------------------------"
total=$(find /app/backend/static/realistic_portraits -name "*.jpg" 2>/dev/null | wc -l)
echo "Total: $total/7200 portraits"
percentage=$((total * 100 / 7200))
echo "Progression: $percentage%"
echo ""

# 2. Vérifier par continent
echo "🌍 2. Répartition par continent"
echo "----------------------------------------"
for continent in africa asia europe america middle_east oceania; do
    if [ -d "/app/backend/static/realistic_portraits/$continent" ]; then
        count=$(find "/app/backend/static/realistic_portraits/$continent" -name "*.jpg" 2>/dev/null | wc -l)
        perc=$((count * 100 / 1200))
        status="🔄"
        if [ $count -eq 1200 ]; then
            status="✅"
        fi
        printf "%s %-15s: %4d/1200 (%3d%%)\n" "$status" "$continent" $count $perc
    fi
done
echo ""

# 3. Vérifier que le backend fonctionne
echo "🔧 3. Test de l'API backend"
echo "----------------------------------------"
response=$(curl -s http://localhost:8001/api/portraits/realistic/stats 2>/dev/null)
if [ $? -eq 0 ]; then
    echo "✅ API accessible"
    ready=$(echo "$response" | jq -r '.ready' 2>/dev/null)
    if [ "$ready" == "true" ]; then
        echo "✅ Système de portraits prêt"
        api_total=$(echo "$response" | jq -r '.stats.total' 2>/dev/null)
        echo "   Total API: $api_total portraits"
    else
        echo "⚠️  Système de portraits non prêt"
    fi
else
    echo "❌ API non accessible"
fi
echo ""

# 4. Test de génération de joueurs
echo "👥 4. Test de génération de joueurs"
echo "----------------------------------------"
player_data=$(curl -s -X POST http://localhost:8001/api/games/generate-players \
    -H "Content-Type: application/json" \
    -d '{"count": 5, "difficulty": "normal"}' 2>/dev/null)

if [ $? -eq 0 ]; then
    echo "✅ Génération de joueurs fonctionnelle"
    
    # Compter combien ont des portraits réalistes
    with_portraits=$(echo "$player_data" | jq '[.[] | select(.portrait.realistic_portrait != null)] | length' 2>/dev/null)
    total_players=$(echo "$player_data" | jq '. | length' 2>/dev/null)
    
    if [ "$with_portraits" ]; then
        echo "   Joueurs avec portraits réalistes: $with_portraits/$total_players"
        
        # Afficher quelques exemples
        echo ""
        echo "   Exemples:"
        echo "$player_data" | jq -r '.[] | select(.portrait.realistic_portrait != null) | "   - \(.name) (\(.nationality), \(.gender)) → \(.portrait.realistic_portrait | split("/")[3])"' 2>/dev/null | head -3
    fi
else
    echo "❌ Erreur lors de la génération de joueurs"
fi
echo ""

# 5. Vérifier si le téléchargement est en cours
echo "📥 5. Statut du téléchargement"
echo "----------------------------------------"
if pgrep -f "download_realistic_portraits_optimized.py" > /dev/null; then
    echo "✅ Téléchargement en cours"
    pid=$(pgrep -f "download_realistic_portraits_optimized.py")
    echo "   PID: $pid"
    
    if [ -f /tmp/portrait_download.log ]; then
        echo "   Dernière activité:"
        tail -3 /tmp/portrait_download.log | sed 's/^/   /'
    fi
else
    echo "⚠️  Aucun téléchargement en cours"
    
    if [ $total -lt 7200 ]; then
        remaining=$((7200 - total))
        echo "   Il reste $remaining portraits à télécharger"
        echo "   Pour relancer: cd /app/backend && python3 download_realistic_portraits_optimized.py"
    fi
fi
echo ""

# 6. Résumé final
echo "========================================"
echo "📋 RÉSUMÉ"
echo "========================================"
if [ $percentage -eq 100 ]; then
    echo "🎉 TÉLÉCHARGEMENT COMPLET!"
    echo "   Tous les 7200 portraits sont disponibles"
elif [ $percentage -ge 95 ]; then
    echo "✅ QUASI COMPLET ($percentage%)"
    echo "   Le système est opérationnel"
    remaining=$((7200 - total))
    echo "   Il reste $remaining portraits à télécharger"
elif [ $percentage -ge 80 ]; then
    echo "🔄 EN COURS ($percentage%)"
    echo "   Le système est opérationnel mais incomplet"
    remaining=$((7200 - total))
    echo "   Il reste $remaining portraits à télécharger"
else
    echo "⚠️  INCOMPLET ($percentage%)"
    remaining=$((7200 - total))
    echo "   Il reste $remaining portraits à télécharger"
fi
echo ""
