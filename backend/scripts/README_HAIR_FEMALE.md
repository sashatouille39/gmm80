# 🎨 GÉNÉRATION DES CHEVEUX FEMME

## 📋 Quand lancer?
Après que les **100 cheveux homme** soient complètement générés.

## ▶️ Comment lancer?

### Option 1: En arrière-plan (recommandé)
```bash
cd /app/backend
nohup python scripts/generate_hair_female.py > /tmp/hair_female_generation.log 2>&1 &
```

### Option 2: En avant-plan (voir progression en direct)
```bash
cd /app/backend
python scripts/generate_hair_female.py
```

## 📊 Suivre la progression

**Vérification rapide:**
```bash
ls -1 /app/backend/static/portraits/hair_female/*.png | wc -l
```

**Monitoring détaillé:**
```bash
/app/backend/scripts/monitor_hair_generation.sh
```

**Logs en temps réel:**
```bash
tail -f /tmp/hair_female_generation.log
```

## ⏱️ Durée estimée
- **100 images** × ~20-25 secondes = **~35-45 minutes**

## ✅ Vérification finale
Une fois terminé:
```bash
cd /app/backend
python scripts/verify_portrait_system.py
```

Cela vous dira:
- ✅ Combien de calques sont disponibles
- ✅ Nombre de combinaisons possibles
- ✅ Si le système d'assemblage fonctionne

## 🎯 Résultat final
Avec les 100 cheveux femme, vous aurez:
- **248 calques PNG** au total
- **~2 millions de combinaisons** de portraits uniques
- Système complet et opérationnel

---

**Note:** Le script détecte automatiquement les fichiers existants et continue là où il s'était arrêté si interrompu.
