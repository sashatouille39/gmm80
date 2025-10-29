#!/bin/bash
# Script de monitoring pour la génération des cheveux féminins

echo "=============================================="
echo "Monitoring Génération Cheveux Femme"
echo "=============================================="
echo ""

# Vérifier si le processus est toujours en cours
if pgrep -f "generate_hair_female.py" > /dev/null; then
    echo "✅ Processus en cours (PID: $(pgrep -f 'generate_hair_female.py'))"
else
    echo "⚠️  Processus terminé ou non démarré"
fi

echo ""

# Compter les fichiers générés
TOTAL_FILES=$(ls -1 /app/backend/static/portraits/hair_female/*.png 2>/dev/null | wc -l)
echo "📊 Progression: $TOTAL_FILES/100 images générées"

# Calculer le pourcentage
PERCENTAGE=$((TOTAL_FILES * 100 / 100))
echo "📈 Pourcentage: ${PERCENTAGE}%"

# Barre de progression
echo -n "["
for i in $(seq 1 50); do
    if [ $((i * 2)) -le $TOTAL_FILES ]; then
        echo -n "="
    else
        echo -n " "
    fi
done
echo "]"

echo ""

# Afficher les dernières lignes du log
echo "📋 Dernières activités:"
echo "----------------------------------------------"
tail -10 /tmp/hair_female_generation.log 2>/dev/null || echo "Aucun log disponible"
echo "----------------------------------------------"

echo ""
echo "Pour voir le log complet: tail -f /tmp/hair_female_generation.log"
