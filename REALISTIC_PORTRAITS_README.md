# 📸 Système de Portraits Réalistes - 7200 Portraits

## 🎯 Objectif

Télécharger **1200 portraits semi-réalistes PAR continent** (total : 7200 portraits) depuis thispersonnotexist.org, organisés par continents et ethnies.

## 📊 Configuration

### Répartition par continent (1200 portraits chacun)

| Continent | Ethnies | Hommes | Femmes | Total |
|-----------|---------|--------|--------|-------|
| **Afrique** | Black | 600 | 600 | 1200 |
| **Asie** | Asian (350) + Indian (250) | 350+250 | 350+250 | 1200 |
| **Europe** | White | 600 | 600 | 1200 |
| **Amérique** | Latino Hispanic (350) + White (250) | 350+250 | 350+250 | 1200 |
| **Moyen-Orient** | Middle Eastern | 600 | 600 | 1200 |
| **Océanie** | White | 600 | 600 | 1200 |

### Paramètres

- **Style** : Semi-réaliste (comme thispersonnotexist.org)
- **Genre** : 50/50 hommes/femmes
- **Âges** : 21-35 ans et 35-50 ans (pas d'enfants)
- **Émotion** : Neutre
- **Format** : JPG, 1024x1024px
- **Taille** : ~200-250KB par image

## 🚀 Lancement du téléchargement

### Option 1 : Téléchargement complet (7200 portraits)

```bash
cd /app/backend

# Lancer en arrière-plan
nohup python download_realistic_portraits_optimized.py > /tmp/realistic_download.log 2>&1 &

# Sauvegarder le PID
echo $! > /tmp/realistic_download_pid.txt
```

### Option 2 : Test avec échantillon (32 portraits)

```bash
cd /app/backend
python test_batch_download.py
```

## 📡 Monitoring

### Suivre la progression en temps réel

```bash
# Monitoring avec interface
/app/backend/monitor_realistic_download.sh

# Ou voir les logs
tail -f /tmp/realistic_download.log

# Ou compter les fichiers téléchargés
find /app/backend/static/realistic_portraits -type f | wc -l
```

### Vérifier le processus

```bash
# Voir si le processus tourne
PID=$(cat /tmp/realistic_download_pid.txt)
ps -p $PID

# Arrêter le processus si nécessaire
kill $PID
```

## 📁 Structure des dossiers

```
/app/backend/static/realistic_portraits/
├── africa/
│   └── black/
│       ├── M/
│       │   ├── africa_black_M_21_35_0001.jpg
│       │   ├── africa_black_M_21_35_0002.jpg
│       │   └── ... (600 fichiers)
│       └── F/
│           └── ... (600 fichiers)
├── asia/
│   ├── asian/
│   │   ├── M/ (350 fichiers)
│   │   └── F/ (350 fichiers)
│   └── indian/
│       ├── M/ (250 fichiers)
│       └── F/ (250 fichiers)
├── europe/
│   └── white/
│       ├── M/ (600 fichiers)
│       └── F/ (600 fichiers)
├── america/
│   ├── latino_hispanic/
│   │   ├── M/ (350 fichiers)
│   │   └── F/ (350 fichiers)
│   └── white/
│       ├── M/ (250 fichiers)
│       └── F/ (250 fichiers)
├── middle_east/
│   └── middle_eastern/
│       ├── M/ (600 fichiers)
│       └── F/ (600 fichiers)
└── oceania/
    └── white/
        ├── M/ (600 fichiers)
        └── F/ (600 fichiers)
```

## ⏱️ Estimation du temps

- **Par lot** : 8 portraits en ~10-12 secondes
- **Total de lots** : 7200 ÷ 8 = 900 lots
- **Temps estimé** : 900 × 12s = 10,800s ≈ **3 heures**
- **Avec pauses/erreurs** : ~**4-5 heures**

## 🔧 Scripts disponibles

| Script | Description |
|--------|-------------|
| `download_realistic_portraits_optimized.py` | Script principal (7200 portraits) |
| `test_batch_download.py` | Script de test (32 portraits) |
| `monitor_realistic_download.sh` | Monitoring en temps réel |

## 📈 Progression sauvegardée

Le script sauvegarde automatiquement la progression dans :
```
/tmp/portrait_download_progress.json
```

En cas d'interruption, le script peut reprendre où il s'était arrêté.

## ⚠️ Notes importantes

1. **Connexion Internet** : Le téléchargement nécessite une connexion stable
2. **Espace disque** : ~1.5-2GB nécessaires pour 7200 portraits
3. **Rate Limiting** : Le script inclut des pauses automatiques entre les lots
4. **Reprise** : Le script peut être relancé en cas d'interruption

## 🎨 Utilisation dans l'application

Une fois téléchargés, les portraits peuvent être utilisés pour :
- Génération de joueurs avec des portraits réalistes
- Système de sélection par continent et ethnie
- Affichage cohérent avec la nationalité des joueurs

## 🧹 Suppression de l'ancien système

Une fois les nouveaux portraits téléchargés, l'ancien système de calques peut être supprimé :

```bash
# Sauvegarder l'ancien système (optionnel)
mv /app/backend/static/portraits /app/backend/static/portraits_old

# Ou supprimer directement
rm -rf /app/backend/static/portraits
```

## ✅ Vérification

Après le téléchargement, vérifier que tous les portraits sont bien là :

```bash
# Compter par continent
for continent in africa asia europe america middle_east oceania; do
    count=$(find /app/backend/static/realistic_portraits/$continent -type f | wc -l)
    echo "$continent: $count/1200"
done

# Total
total=$(find /app/backend/static/realistic_portraits -type f | wc -l)
echo "TOTAL: $total/7200"
```

## 📝 Logs et Debug

- **Log principal** : `/tmp/realistic_download.log`
- **Progression** : `/tmp/portrait_download_progress.json`
- **PID** : `/tmp/realistic_download_pid.txt`
- **Captures d'écran test** : `/app/backend/static/realistic_portraits_test/`

---

**Créé le** : 30 Octobre 2025  
**Source** : thispersonnotexist.org  
**Technologie** : StyleGAN3 (AI-generated faces)
