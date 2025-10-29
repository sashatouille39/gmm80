#!/bin/bash

# Script de monitoring de la génération des calques manquants

echo "🎨 MONITORING GÉNÉRATION CALQUES IA - PORTRAITS"
echo "=================================================="
echo ""

# Vérifier si le processus est actif
PID_FILE="/tmp/portrait_gen_missing_pid.txt"
LOG_FILE="/tmp/portrait_generation_missing.log"

if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p $PID > /dev/null 2>&1; then
        echo "✅ Processus actif (PID: $PID)"
    else
        echo "⚠️  Processus terminé ou interrompu (PID: $PID)"
    fi
else
    echo "❌ Aucun fichier PID trouvé"
fi

echo ""
echo "📊 PROGRESSION DES CALQUES:"
echo "----------------------------"

# Compter les fichiers dans chaque dossier
PORTRAIT_DIR="/app/backend/static/portraits"

for layer in base eyes hair mouth nose; do
    if [ -d "$PORTRAIT_DIR/$layer" ]; then
        COUNT=$(ls -1 "$PORTRAIT_DIR/$layer" 2>/dev/null | wc -l)
        
        case $layer in
            base)   TARGET=10 ;;
            eyes)   TARGET=18 ;;
            hair)   TARGET=200 ;;
            mouth)  TARGET=10 ;;
            nose)   TARGET=10 ;;
        esac
        
        PERCENTAGE=$((COUNT * 100 / TARGET))
        BAR_LENGTH=$((PERCENTAGE / 5))
        BAR=$(printf '█%.0s' $(seq 1 $BAR_LENGTH))
        EMPTY=$(printf '░%.0s' $(seq 1 $((20 - BAR_LENGTH))))
        
        printf "%-8s [%s%s] %3d/%3d (%3d%%)\n" "$layer" "$BAR" "$EMPTY" "$COUNT" "$TARGET" "$PERCENTAGE"
    fi
done

echo ""

# Total
TOTAL_CURRENT=$(find "$PORTRAIT_DIR" -type f -name "*.png" 2>/dev/null | wc -l)
TOTAL_TARGET=248
TOTAL_PERCENTAGE=$((TOTAL_CURRENT * 100 / TOTAL_TARGET))
echo "📊 TOTAL: $TOTAL_CURRENT/$TOTAL_TARGET calques ($TOTAL_PERCENTAGE%)"

echo ""
echo "📄 DERNIÈRES LIGNES DU LOG:"
echo "----------------------------"
if [ -f "$LOG_FILE" ]; then
    tail -20 "$LOG_FILE"
else
    echo "❌ Fichier log non trouvé: $LOG_FILE"
fi

echo ""
echo "💡 COMMANDES UTILES:"
echo "  • Suivre le log en temps réel: tail -f $LOG_FILE"
echo "  • Arrêter la génération: kill \$(cat $PID_FILE)"
echo "  • Relancer ce monitoring: /app/backend/scripts/monitor_missing_generation.sh"
