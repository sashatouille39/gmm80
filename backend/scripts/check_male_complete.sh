#!/bin/bash
# Vérification si la génération homme est terminée

hair_male_count=$(ls -1 /app/backend/static/portraits/hair_male/*.png 2>/dev/null | wc -l)

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  STATUT GÉNÉRATION HOMME"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Cheveux homme: $hair_male_count/100"
echo ""

if [ $hair_male_count -ge 100 ]; then
    echo "✅ GÉNÉRATION HOMME COMPLÈTE!"
    echo ""
    echo "🎯 Prochaine étape: Générer les cheveux femme"
    echo ""
    echo "Pour lancer la génération femme:"
    echo "  cd /app/backend"
    echo "  nohup python scripts/generate_hair_female.py > /tmp/hair_female_generation.log 2>&1 &"
    echo ""
    echo "📖 Documentation: /app/backend/scripts/README_HAIR_FEMALE.md"
elif [ -f /tmp/portrait_hair_gen_pid.txt ]; then
    PID=$(cat /tmp/portrait_hair_gen_pid.txt)
    if ps -p $PID > /dev/null 2>&1; then
        remaining=$((100 - hair_male_count))
        eta_min=$((remaining * 22 / 60))
        echo "🟢 GÉNÉRATION EN COURS"
        echo ""
        echo "Restant: $remaining cheveux (~${eta_min} minutes)"
        echo "Progression: $(( hair_male_count * 100 / 100 ))%"
        echo ""
        echo "📊 Suivi: /app/backend/scripts/quick_check.sh"
        echo "📜 Logs:  tail -f /tmp/hair_generation.log"
    else
        echo "⚠️  PROCESSUS ARRÊTÉ"
        echo ""
        echo "Relancer avec:"
        echo "  cd /app/backend"
        echo "  nohup python scripts/generate_hair_only.py > /tmp/hair_generation.log 2>&1 &"
    fi
else
    echo "⚪ PAS DE GÉNÉRATION ACTIVE"
    echo ""
    echo "Pour démarrer:"
    echo "  cd /app/backend"
    echo "  nohup python scripts/generate_hair_only.py > /tmp/hair_generation.log 2>&1 &"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
