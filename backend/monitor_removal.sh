#!/bin/bash

echo "═══════════════════════════════════════════════════════════"
echo "📊 MONITORING - Suppression des portraits d'enfants"
echo "═══════════════════════════════════════════════════════════"

# Vérifier si le process est en cours
if pgrep -f "remove_children_portraits.py" > /dev/null; then
    echo "✅ Status: En cours d'exécution"
    echo ""
    
    # Afficher les dernières lignes du log
    echo "📋 Progression actuelle:"
    echo "-----------------------------------------------------------"
    tail -15 /app/backend/children_removal.log | grep -E "(📂|Analyse|africa|asia|europe|america|middle_east|oceania|%|it/s)"
    echo ""
    
    # Compter les fichiers déplacés
    if [ -d "/app/backend/static/realistic_portraits_backup_children" ]; then
        MOVED=$(find /app/backend/static/realistic_portraits_backup_children -type f \( -name "*.jpg" -o -name "*.png" \) 2>/dev/null | wc -l)
        echo "❌ Portraits d'enfants déplacés: $MOVED"
    fi
    
    # Estimer le temps restant
    TOTAL=7199
    PROCESSED=$(grep -oP "africa/black/M:.*?(\d+)/600" /app/backend/children_removal.log 2>/dev/null | tail -1 | grep -oP "\d+/600" | cut -d/ -f1 || echo "0")
    
    if [ "$PROCESSED" -gt "0" ]; then
        PERCENT=$((PROCESSED * 100 / TOTAL))
        echo "📈 Progression estimée: ~$PERCENT%"
    fi
    
else
    echo "⚠️  Status: Terminé ou arrêté"
    echo ""
    
    # Vérifier si le rapport existe
    if [ -f "/app/backend/children_removal_report.json" ]; then
        echo "✅ Rapport généré"
        echo ""
        
        # Afficher le résumé du rapport
        echo "📊 RÉSUMÉ:"
        echo "-----------------------------------------------------------"
        tail -30 /app/backend/children_removal.log | grep -A 20 "RAPPORT DE SUPPRESSION"
    else
        echo "❌ Aucun rapport trouvé"
    fi
fi

echo "═══════════════════════════════════════════════════════════"
