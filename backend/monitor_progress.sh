#!/bin/bash
echo "📊 MONITORING TÉLÉCHARGEMENT PORTRAITS RÉALISTES"
echo "================================================"
echo ""
echo "🔄 Vérification du processus..."
PID=$(cat /tmp/realistic_download_pid.txt 2>/dev/null)
if [ -n "$PID" ] && ps -p $PID > /dev/null 2>&1; then
    echo "✅ Processus actif (PID: $PID)"
    ps -p $PID -o pid,comm,%cpu,%mem,etime
else
    echo "⚠️  Processus terminé ou non trouvé"
fi

echo ""
echo "📁 Comptage des portraits par continent:"
echo "----------------------------------------"

for continent in africa asia europe america middle_east oceania; do
    count=$(find /app/backend/static/realistic_portraits/$continent -type f 2>/dev/null | wc -l)
    pct=$(echo "scale=1; ($count * 100) / 1200" | bc 2>/dev/null || echo "0")
    
    if [ $count -eq 1200 ]; then
        echo "✅ $continent: $count/1200 (100%)"
    elif [ $count -gt 1100 ]; then
        echo "🔄 $continent: $count/1200 ($pct%)"
    else
        echo "⏳ $continent: $count/1200 ($pct%)"
    fi
done

echo ""
total=$(find /app/backend/static/realistic_portraits -type f 2>/dev/null | wc -l)
total_pct=$(echo "scale=1; ($total * 100) / 7200" | bc 2>/dev/null || echo "0")
echo "📊 TOTAL: $total/7200 ($total_pct%)"
echo ""
echo "📄 Dernières lignes du log:"
echo "----------------------------------------"
tail -10 /tmp/realistic_download.log 2>/dev/null || echo "Aucun log disponible"
