# 🎨 Génération de 7200 Portraits Réalistes par IA

## ✅ Système Déployé et En Cours

La génération automatique de **7200 portraits photo-réalistes** avec **gpt-image-1** est actuellement **EN COURS** en arrière-plan.

---

## 📊 Progression

### Surveiller en temps réel
```bash
bash /app/backend/monitor_ai_generation.sh
```

### Voir les logs complets
```bash
tail -f /tmp/ai_portraits_full.log
```

---

## 🎯 Configuration

### Objectif
- **7200 portraits** au total
- **6 continents** : Afrique, Asie, Europe, Amérique du Nord, Amérique du Sud, Océanie
- **1200 portraits par continent** : 600 hommes + 600 femmes
- **Qualité** : Semi-réaliste, haute qualité
- **Taille** : 1024x1024 pixels (~2MB par image)

### Modèle IA
- **gpt-image-1** (OpenAI, via Emergent LLM Key)
- **Quality** : "low" (pour optimiser le crédit)
- **Style** : Semi-réaliste, portraits photographiques professionnels

### Arrêt Automatique
- S'arrête automatiquement quand le crédit atteint **0.50**
- Ou après avoir généré les 7200 portraits
- Progression sauvegardée - peut être relancé sans perdre le travail

---

## 📁 Structure des Dossiers

```
/app/backend/static/portraits/
├── africa/
│   ├── male/          (600 portraits)
│   └── female/        (600 portraits)
├── asia/
│   ├── male/          (600 portraits)
│   └── female/        (600 portraits)
├── europe/
│   ├── male/          (600 portraits)
│   └── female/        (600 portraits)
├── north_america/
│   ├── male/          (600 portraits)
│   └── female/        (600 portraits)
├── south_america/
│   ├── male/          (600 portraits)
│   └── female/        (600 portraits)
└── oceania/
    ├── male/          (600 portraits)
    └── female/        (600 portraits)
```

Nommage : `portrait_0001.png`, `portrait_0002.png`, ..., `portrait_0600.png`

---

## 🔄 Gestion du Processus

### Arrêter la génération
```bash
pkill -f generate_ai_portraits
```

### Relancer après arrêt
```bash
cd /app/backend
python generate_ai_portraits.py
```
**Note** : Le script détecte automatiquement les portraits déjà générés et reprend là où il s'est arrêté.

### Voir le statut du processus
```bash
ps aux | grep generate_ai_portraits
```

---

## ⏱️ Temps Estimé

- **~17 secondes** par portrait (temps mesuré)
- **7200 portraits** × 17s = **~34 heures** au total
- **Ou jusqu'à épuisement du crédit** (arrêt à 0.50 restant)

---

## 🎨 Caractéristiques des Portraits

### Prompts Personnalisés par Continent

**Afrique** :
- Ethnicités : African, Sub-Saharan African, West African, East African
- Teints : Dark brown, deep brown, rich brown, ebony

**Asie** :
- Ethnicités : East Asian, Southeast Asian, South Asian, Chinese, Japanese, Korean
- Teints : Light, fair, tan, olive, brown

**Europe** :
- Ethnicités : European, Caucasian, Northern European, Southern European
- Teints : Pale, fair, light, olive, tan

**Amérique du Nord** :
- Ethnicités : North American, Caucasian, Latino, Hispanic, Mixed
- Teints : Fair, light, tan, olive, brown

**Amérique du Sud** :
- Ethnicités : Latino, Hispanic, South American, Brazilian, Mixed
- Teints : Tan, olive, light brown, bronze

**Océanie** :
- Ethnicités : Pacific Islander, Polynesian, Aboriginal Australian, Maori
- Teints : Tan, olive, brown, fair

### Style de Portrait
- **Semi-réaliste** : Détails photographiques réalistes
- **Composition** : Tête et épaules, centré, face caméra
- **Éclairage** : Studio professionnel, doux
- **Expression** : Neutre et naturelle
- **Fond** : Propre et neutre

---

## 💰 Gestion du Crédit

### Crédit Actuel
La génération continue jusqu'à ce que le crédit atteigne **0.50**.

### Coût Estimé
- **gpt-image-1** en qualité "low" : ~0.040$ par image (estimation OpenAI)
- **7200 images** × 0.040$ = **~288$** pour le projet complet

**Note** : Le script s'arrêtera automatiquement si le crédit est insuffisant.

---

## 📊 Statistiques en Temps Réel

Utilisez le script de monitoring :
```bash
bash /app/backend/monitor_ai_generation.sh
```

Affiche :
- ✅ Portraits générés par continent
- 📊 Pourcentage de complétion
- ⏱️ Temps écoulé et temps restant estimé
- 📝 Dernières lignes du log

---

## 🎯 Utilisation dans l'Application

Les portraits générés sont accessibles via :
```
/static/portraits/{continent}/{gender}/portrait_XXXX.png
```

**Exemples** :
- `/static/portraits/africa/male/portrait_0001.png`
- `/static/portraits/asia/female/portrait_0350.png`
- `/static/portraits/europe/male/portrait_0599.png`

---

## 🛠️ Fichiers du Système

**Scripts principaux** :
- `generate_ai_portraits.py` - Générateur principal
- `test_ai_generation.py` - Test avec 3 portraits
- `monitor_ai_generation.sh` - Monitoring en temps réel

**Logs** :
- `/tmp/ai_portraits_full.log` - Log complet de la génération

**Configuration** :
- `.env` - Contient `EMERGENT_LLM_KEY`

---

## ✅ Vérification

### Voir les images générées
```bash
ls /app/backend/static/portraits/africa/male/ | head -10
```

### Compter les images
```bash
find /app/backend/static/portraits -name "portrait_*.png" | wc -l
```

### Taille totale utilisée
```bash
du -sh /app/backend/static/portraits
```

---

## 🎉 Résultat Final Attendu

Quand la génération sera terminée :
- ✅ **7200 portraits réalistes** générés par IA
- ✅ Organisés par **continent** et **genre**
- ✅ **Haute qualité** (1024x1024, semi-réaliste)
- ✅ **Prêts à utiliser** dans votre application
- ✅ **Diversité ethnique authentique** pour chaque continent

---

## 📞 Support

**Problème : Génération arrêtée**
→ Vérifiez les logs : `tail -50 /tmp/ai_portraits_full.log`
→ Vérifiez le crédit restant
→ Relancez : `python generate_ai_portraits.py`

**Problème : Images corrompues**
→ Le script génère automatiquement des images PNG valides
→ Vérifiez la taille : images ~2MB chacune

**Problème : Mémoire insuffisante**
→ Machine déjà upgradée, devrait fonctionner correctement

---

**🚀 La génération est EN COURS !**

Utilisez `bash monitor_ai_generation.sh` pour suivre la progression.
