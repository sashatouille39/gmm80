# 🎭 GÉNÉRATION DE PORTRAITS - DOCUMENTATION

## 📊 ÉTAT ACTUEL (au lancement)

### Calques déjà générés ✅
- **Base (teints de peau)**: 11/10 ✅ (110% - avec 1 test bonus)
- **Yeux**: 18/10 ✅ (180%)
- **Bouches**: 10/10 ✅ (100%)
- **Nez**: 10/10 ✅ (100%)

### Calques en cours de génération 🚀
- **Cheveux homme**: 0/100 → En cours
- **Cheveux femme**: 0/100 → Après cheveux homme

## ⚙️ PROCESSUS EN COURS

### Script actif
- **Fichier**: `/app/backend/scripts/generate_hair_only.py`
- **PID**: Voir `/tmp/portrait_hair_gen_pid.txt`
- **Log**: `/tmp/hair_generation.log`

### Caractéristiques
- Génération asynchrone avec `asyncio`
- Modèle IA: `gpt-image-1` (OpenAI)
- Prompts optimisés pour calques PNG transparents
- Pause automatique tous les 10 images (rate limiting)
- Nomenclature: `hair_male_X.png` et `hair_female_X.png`

### Temps estimé
- **Par image**: ~15-20 secondes
- **Total**: ~60-70 minutes pour 200 images
- **Progression**: Vérifier avec `quick_check.sh`

## 📁 STRUCTURE DES FICHIERS

```
/app/backend/static/portraits/
├── base/              # 11 fichiers (teints de peau)
├── eyes/              # 18 fichiers (variations yeux)
├── hair_male/         # 0→100 fichiers (EN COURS)
├── hair_female/       # 0→100 fichiers (À VENIR)
├── mouth/             # 10 fichiers (variations bouches)
└── nose/              # 10 fichiers (variations nez)
```

## 🛠️ COMMANDES UTILES

### Vérifier la progression
```bash
# Résumé rapide
/app/backend/scripts/quick_check.sh

# Détails complets
/app/backend/scripts/monitor_hair_generation.sh

# Suivi en temps réel (auto-refresh 15s)
/app/backend/scripts/watch_generation.sh
```

### Gérer le processus
```bash
# Vérifier si actif
PID=$(cat /tmp/portrait_hair_gen_pid.txt)
ps -p $PID

# Voir les logs en temps réel
tail -f /tmp/hair_generation.log

# Arrêter la génération (si nécessaire)
pkill -f generate_hair_only.py
```

## 🎯 OBJECTIF FINAL

Une fois terminé, vous aurez:
- **248 calques PNG** au total
- **~600,000 combinaisons de portraits uniques** possibles
- Portraits cohérents par nationalité et genre des joueurs
- Système d'assemblage automatique via `portrait_generator_service.py`

## 📈 COMBINAISONS POSSIBLES

### Homme
```
11 bases × 18 yeux × 100 cheveux × 10 bouches × 10 nez = 1,980,000 combinaisons
```

### Femme  
```
11 bases × 18 yeux × 100 cheveux × 10 bouches × 10 nez = 1,980,000 combinaisons
```

### Total théorique
**3,960,000 portraits uniques** possibles!

(Le système filtre par genre pour ~600k combinaisons pratiques)

## 🔧 DÉPANNAGE

### Le processus s'est arrêté?
```bash
# Vérifier combien ont été générés
ls -1 /app/backend/static/portraits/hair_male/*.png | wc -l
ls -1 /app/backend/static/portraits/hair_female/*.png | wc -l

# Relancer la génération
cd /app/backend
nohup python scripts/generate_hair_only.py > /tmp/hair_generation.log 2>&1 &
```

### Erreurs dans le log?
```bash
# Voir les erreurs
grep "❌" /tmp/hair_generation.log | tail -20

# Voir les succès
grep "✅" /tmp/hair_generation.log | tail -20
```

## ✅ VÉRIFICATION FINALE

Une fois la génération terminée:
```bash
cd /app/backend
python scripts/verify_portrait_system.py
```

Ce script:
- Compte tous les calques disponibles
- Calcule les combinaisons possibles
- Teste l'assemblage d'un portrait aléatoire
- Affiche un rapport complet

## 🎨 INTÉGRATION FRONTEND

Le composant React `LayeredPortrait.jsx` assemble automatiquement les calques:
- Récupère les calques depuis l'API `/api/portraits/random`
- Superpose les PNG avec transparence (z-index)
- Affiche le portrait final du joueur

Aucune modification nécessaire - tout est déjà configuré!

## 📝 NOTES IMPORTANTES

1. **Ne PAS interrompre** avant la fin pour avoir toutes les variations
2. **Ne PAS régénérer** les bases/yeux/bouches/nez (déjà faits)
3. **Surveiller l'espace disque** (~400-500 MB pour tous les calques)
4. **API Key**: Utilise `EMERGENT_LLM_KEY` depuis `.env`

---

**Généré le**: 2025-10-29  
**Script**: `/app/backend/scripts/generate_hair_only.py`  
**Documentation**: `/app/GENERATION_PROGRESS.md`
