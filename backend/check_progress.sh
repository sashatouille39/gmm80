#!/bin/bash

echo "═══════════════════════════════════════════════════════════"
echo "📊 PROGRESSION - Suppression des portraits d'enfants"
echo "═══════════════════════════════════════════════════════════"
echo ""

# Vérifier si le process est en cours
if pgrep -f "remove_children_portraits_optimized.py" > /dev/null; then
    echo "✅ Status: EN COURS D'EXÉCUTION"
    echo ""
    
    # Afficher la progression actuelle
    echo "📋 Progression actuelle:"
    tail -5 /app/backend/children_removal.log | grep -E "africa|asia|europe|america|middle_east|oceania|%" || echo "  Traitement en cours..."
    echo ""
    
    # Compter les fichiers déplacés
    if [ -d "/app/backend/static/realistic_portraits_backup_children" ]; then
        MOVED=$(find /app/backend/static/realistic_portraits_backup_children -type f \( -name "*.jpg" -o -name "*.png" \) 2>/dev/null | wc -l)
        echo "❌ Portraits d'enfants déplacés jusqu'à maintenant: $MOVED"
    fi
    
    # Total de portraits
    TOTAL=$(find /app/backend/static/realistic_portraits -type f \( -name "*.jpg" -o -name "*.png" \) 2>/dev/null | wc -l)
    echo "📁 Portraits restants à analyser: $TOTAL"
    echo ""
    
    # Estimation du temps
    PROCESSED=$((7198 - TOTAL))
    if [ "$PROCESSED" -gt "0" ]; then
        PERCENT=$((PROCESSED * 100 / 7198))
        echo "📈 Progression: $PROCESSED/7198 ($PERCENT%)"
        
        # Estimer le temps restant (environ 1.5 it/s)
        REMAINING_TIME=$((TOTAL * 2 / 3 / 60))
        echo "⏱️  Temps estimé restant: ~$REMAINING_TIME minutes"
    fi
    
else
    echo "⏹️  Status: TERMINÉ"
    echo ""
    
    # Afficher le rapport final
    if [ -f "/app/backend/children_removal_report.json" ]; then
        echo "✅ Rapport généré: /app/backend/children_removal_report.json"
        echo ""
        
        # Extraire les statistiques du rapport
        SCANNED=$(grep -oP '"total_scanned":\s*\K\d+' /app/backend/children_removal_report.json 2>/dev/null || echo "0")
        REMOVED=$(grep -oP '"total_removed":\s*\K\d+' /app/backend/children_removal_report.json 2>/dev/null || echo "0")
        ERRORS=$(grep -oP '"errors":\s*\K\d+' /app/backend/children_removal_report.json 2>/dev/null || echo "0")
        
        echo "📊 RÉSULTATS FINAUX:"
        echo "  • Portraits scannés: $SCANNED"
        echo "  • Portraits d'enfants supprimés: $REMOVED"
        echo "  • Erreurs: $ERRORS"
        echo ""
        
        # Compter les fichiers dans le backup
        if [ -d "/app/backend/static/realistic_portraits_backup_children" ]; then
            BACKUP_COUNT=$(find /app/backend/static/realistic_portraits_backup_children -type f \( -name "*.jpg" -o -name "*.png" \) 2>/dev/null | wc -l)
            echo "💾 Fichiers dans le backup: $BACKUP_COUNT"
        fi
    else
        echo "⚠️  Aucun rapport trouvé - vérifiez les logs:"
        echo ""
        tail -20 /app/backend/children_removal.log
    fi
fi

echo ""
echo "═══════════════════════════════════════════════════════════"
