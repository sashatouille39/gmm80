# PROMPT DE CONTINUATION - GÉNÉRATION CALQUES IA PORTRAITS

## CONTEXTE
Système de portraits par calques **DÉJÀ COMPLÈTEMENT IMPLÉMENTÉ** (service backend + frontend LayeredPortrait.jsx). 
Génération de 248 calques IA en cours via script personnalisé.

## ÉTAT ACTUEL (NE PAS REGÉNÉRER)
✅ **DÉJÀ GÉNÉRÉS** (31/248 - 12%):
- ✅ 10/10 Bases (teintes peau) - fichiers: skin_tone_*.png
- ✅ 21/100 Cheveux homme - fichiers: hair_male_*.png
- ⚠️  0/18 Yeux (mais système fonctionne, tests réussis)
- ⚠️  0/100 Cheveux femme
- ⚠️  0/10 Bouches
- ⚠️  0/10 Nez

## CE QU'IL RESTE À FAIRE
🎯 **GÉNÉRER LES CALQUES MANQUANTS** (217/248 restants):
- 18 Yeux (3 formes × 6 couleurs)
- 79 Cheveux homme (100 - 21 déjà faits)
- 100 Cheveux femme
- 10 Bouches
- 10 Nez

## SCRIPTS DISPONIBLES
📁 Tous dans `/app/backend/scripts/`:
1. **generate_custom_library.py** - Script principal (CORRIGÉ, fonctionne)
2. **monitor_generation.sh** - Suivi de progression
3. **verify_portrait_system.py** - Test final

## PROCESSUS EN COURS
- PID: Lire `/tmp/portrait_gen_pid.txt`
- Log: `/tmp/portrait_generation.log`
- Estimation: ~1h pour tout générer (15 sec/image)

## ACTIONS À FAIRE

### Option 1 - Laisser le processus actuel finir
```bash
# Vérifier si toujours actif
PID=$(cat /tmp/portrait_gen_pid.txt)
ps -p $PID

# Suivre la progression
/app/backend/scripts/monitor_generation.sh
tail -f /tmp/portrait_generation.log

# Attendre la fin, puis vérifier
python /app/backend/scripts/verify_portrait_system.py
```

### Option 2 - Régénérer seulement les manquants (RECOMMANDÉ)
```bash
# Arrêter le processus actuel si besoin
PID=$(cat /tmp/portrait_gen_pid.txt)
kill $PID 2>/dev/null

# Créer script de génération partielle
# Modifier generate_custom_library.py pour:
# - SKIP les bases (déjà 10/10)
# - CONTINUER cheveux homme à partir de 22/100
# - Générer cheveux femme, yeux, bouches, nez normalement
```

### Option 3 - Optimiser la génération (si trop lent)
- Réduire le nombre de cheveux (ex: 50 homme + 50 femme au lieu de 100+100)
- Ou générer en batch avec rate limiting

## ⚠️ CE QU'IL NE FAUT PAS FAIRE
❌ Ne PAS régénérer les bases déjà créées (skin_tone_*.png)
❌ Ne PAS supprimer les fichiers hair_male_*.png existants
❌ Ne PAS modifier portrait_generator_service.py (DÉJÀ FONCTIONNEL)
❌ Ne PAS modifier LayeredPortrait.jsx (DÉJÀ INTÉGRÉ)
❌ Ne PAS changer la nomenclature des fichiers

## VÉRIFICATION FINALE
Une fois la génération terminée (ou partiellement):
```bash
cd /app/backend
python scripts/verify_portrait_system.py
```
Cela indiquera combien de combinaisons sont possibles et testera l'assemblage.

## INFOS TECHNIQUES
- Clé API: EMERGENT_LLM_KEY dans /app/backend/.env (DÉJÀ CONFIGURÉE)
- Méthode IA: `service.image_gen.generate_images()` (pluriel!)
- Dossier calques: `/app/backend/static/portraits/{base,eyes,hair,mouth,nose}/`
- Système d'assemblage: `portrait_generator_service.py::select_random_portrait_layers()`

## RÉSULTAT ATTENDU
Avec les 248 calques: **~600,000 combinaisons de portraits uniques** cohérents avec nationalité/sexe des joueurs.
