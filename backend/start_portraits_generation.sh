#!/bin/bash
# Script pour lancer le pipeline de génération de portraits en arrière-plan

echo "======================================================================"
echo "🎨 GÉNÉRATEUR DE 7200 PORTRAITS RÉALISTES"
echo "======================================================================"
echo ""
echo "Ce script va lancer le pipeline complet en arrière-plan."
echo "Le processus prendra environ 2-3 heures."
echo ""
echo "📋 Étapes:"
echo "   1. Téléchargement de 12,000 images (~30-60 min)"
echo "   2. Classification par IA (~1-2h)"
echo "   3. Réorganisation (~5 min)"
echo ""
echo "📁 Résultat: 7200 portraits dans /app/backend/static/portraits/"
echo ""
echo "======================================================================"
echo ""

# Demander confirmation
read -p "Voulez-vous démarrer le processus ? (y/n): " confirm

if [ "$confirm" != "y" ]; then
    echo "Annulé."
    exit 0
fi

# Créer le dossier de logs
mkdir -p /app/backend/logs

# Lancer en arrière-plan
cd /app/backend

echo ""
echo "🚀 Démarrage du pipeline..."
echo "📝 Logs dans: /app/backend/logs/portraits_pipeline.log"
echo ""
echo "Pour suivre la progression:"
echo "   tail -f /app/backend/logs/portraits_pipeline.log"
echo ""

# Lancer le pipeline en mode non-interactif
nohup python3 -u generate_portraits_pipeline_auto.py > logs/portraits_pipeline.log 2>&1 &

PID=$!
echo "✅ Pipeline lancé (PID: $PID)"
echo ""
echo "Commandes utiles:"
echo "   • Voir les logs: tail -f /app/backend/logs/portraits_pipeline.log"
echo "   • Arrêter: kill $PID"
echo "   • Statut: ps aux | grep $PID"
echo ""
echo "Le processus continue même si vous fermez ce terminal."
echo "======================================================================"
