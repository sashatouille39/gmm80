# 🎨 Guide du Système de Portraits Réalistes

## 📋 Vue d'ensemble

Le système de portraits réalistes remplace l'ancien système de calques PNG par des portraits complets semi-réalistes générés par StyleGAN3, téléchargés depuis **thispersonnotexist.org**.

### Caractéristiques principales

- **7200 portraits** au total (1200 par continent × 6 continents)
- **Répartition équilibrée** : 50% hommes / 50% femmes
- **Tranches d'âge** : 21-35 ans et 34-50 ans (pas d'enfants)
- **Émotion** : neutre uniquement
- **Organisation** : Par continent → ethnie → genre

---

## 🌍 Répartition par continent

| Continent | Ethnies | Portraits | Statut |
|-----------|---------|-----------|---------|
| **Afrique** | Black | 1200 | ✅ 100% |
| **Asie** | Asian (700) + Indian (500) | 1200 | ✅ 99.9% |
| **Europe** | White | 1200 | ✅ 100% |
| **Amérique** | Latino Hispanic (700) + White (500) | 1200 | ✅ 100% |
| **Moyen-Orient** | Middle Eastern | 1200 | 🔄 98.9% |
| **Océanie** | White | 1200 | 🔄 84.8% |

**Total actuel** : ~7000/7200 portraits (97.3%)

---

## 🏗️ Architecture du système

### Backend

#### 1. Service principal : `RealisticPortraitService`

**Fichier** : `/app/backend/services/realistic_portrait_service.py`

**Fonctionnalités** :
- Mapping de **250+ nationalités** vers continents et ethnies
- Sélection aléatoire de portraits selon nationalité et genre
- Cache intelligent pour optimiser les performances
- Statistiques en temps réel sur les portraits disponibles

**Exemple de mapping** :
```python
'Français' → ('europe', 'white')
'Nigérian' → ('africa', 'black')
'Chinois' → ('asia', 'asian')
'Brésilien' → ('america', 'latino_hispanic')
'Saoudien' → ('middle_east', 'middle_eastern')
'Australien' → ('oceania', 'white')
```

#### 2. Intégration dans `GameService`

**Fichier** : `/app/backend/services/game_service.py`

**Système de priorité dans `_generate_portrait()`** :

```python
# PRIORITÉ 1 : Portrait réaliste
if realistic_service.is_ready():
    realistic_portrait_path = realistic_service.select_random_portrait(nationality, gender)
    if realistic_portrait_path:
        return PlayerPortrait(
            realistic_portrait=realistic_portrait_path,
            # Calques à None
            layer_base=None,
            layer_eyes=None,
            # ...
        )

# PRIORITÉ 2 : Fallback sur calques PNG
portrait_layers = portrait_service.select_random_portrait_layers(nationality, gender)
return PlayerPortrait(
    layer_base=portrait_layers.get('base'),
    layer_eyes=portrait_layers.get('eyes'),
    # ...
)
```

#### 3. Routes API

**Statistiques** : `GET /api/portraits/realistic/stats`
```json
{
  "success": true,
  "ready": true,
  "stats": {
    "africa": {
      "black": { "M": 600, "F": 600 }
    },
    "asia": {
      "asian": { "M": 349, "F": 350 },
      "indian": { "M": 250, "F": 189 }
    },
    // ...
    "total": 7003
  }
}
```

**Portrait aléatoire** : `GET /api/portraits/realistic/random?nationality=Français&gender=M`

---

### Frontend

#### Composant `LayeredPortrait`

**Fichier** : `/app/frontend/src/components/LayeredPortrait.jsx`

**Système de priorité d'affichage** :

1. **PRIORITÉ 1** : Portrait réaliste complet
   ```jsx
   if (hasRealisticPortrait) {
     return <img src={`${backendUrl}${player.portrait.realistic_portrait}`} />
   }
   ```

2. **PRIORITÉ 2** : Calques PNG superposés (ancien système)
   ```jsx
   if (hasLayers) {
     return <div>
       <img src={layer_base} />
       <img src={layer_eyes} />
       {/* ... */}
     </div>
   }
   ```

3. **FALLBACK** : Cercle avec numéro du joueur
   ```jsx
   return <div className="rounded-full bg-blue-600">
     {player.number}
   </div>
   ```

---

## 📥 Téléchargement des portraits

### Script automatisé

**Fichier** : `/app/backend/download_realistic_portraits_optimized.py`

**Caractéristiques** :
- ✅ Télécharge **8 portraits à la fois** (optimisation)
- ✅ Saute les fichiers déjà existants
- ✅ Reprise automatique en cas d'interruption
- ✅ Sauvegarde de la progression dans `/tmp/portrait_download_progress.json`
- ✅ Délai aléatoire entre les lots (3-5 secondes)

**Lancer le téléchargement** :
```bash
cd /app/backend
python3 download_realistic_portraits_optimized.py
```

**Lancer en arrière-plan** :
```bash
cd /app/backend
nohup python3 download_realistic_portraits_optimized.py > /tmp/portrait_download.log 2>&1 &
```

**Monitorer la progression** :
```bash
tail -f /tmp/portrait_download.log
```

**Script de monitoring** :
```bash
bash /app/backend/monitor_realistic_download.sh
```

---

## 📂 Structure des fichiers

```
/app/backend/static/realistic_portraits/
├── africa/
│   └── black/
│       ├── M/
│       │   ├── africa_black_M_21_35_0001.jpg
│       │   ├── africa_black_M_21_35_0002.jpg
│       │   └── ...
│       └── F/
│           ├── africa_black_F_21_35_0001.jpg
│           └── ...
├── asia/
│   ├── asian/
│   │   ├── M/ (350 portraits)
│   │   └── F/ (350 portraits)
│   └── indian/
│       ├── M/ (250 portraits)
│       └── F/ (250 portraits)
├── europe/
│   └── white/
│       ├── M/ (600 portraits)
│       └── F/ (600 portraits)
├── america/
│   ├── latino_hispanic/
│   │   ├── M/ (350 portraits)
│   │   └── F/ (350 portraits)
│   └── white/
│       ├── M/ (250 portraits)
│       └── F/ (250 portraits)
├── middle_east/
│   └── middle_eastern/
│       ├── M/ (600 portraits)
│       └── F/ (600 portraits)
└── oceania/
    └── white/
        ├── M/ (600 portraits)
        └── F/ (600 portraits)
```

### Nomenclature des fichiers

Format : `{continent}_{ethnie}_{genre}_{tranche_age}_{numéro}.jpg`

Exemples :
- `africa_black_M_21_35_0001.jpg`
- `asia_asian_F_34_50_0123.jpg`
- `europe_white_M_21_35_0456.jpg`

---

## 🧪 Tests et validation

### Test de génération de joueurs

```bash
curl -X POST http://localhost:8001/api/games/generate-players \
  -H "Content-Type: application/json" \
  -d '{"count": 5, "difficulty": "normal"}' | jq '.[] | {name, nationality, gender, realistic: .portrait.realistic_portrait}'
```

**Résultat attendu** :
```json
{
  "name": "Youssef El Idrissi",
  "nationality": "Marocain",
  "gender": "M",
  "realistic": "/static/realistic_portraits/africa/black/M/africa_black_M_34_50_0139.jpg"
}
```

### Test des statistiques

```bash
curl -s http://localhost:8001/api/portraits/realistic/stats | jq '.stats.total'
```

### Test du mapping nationalités

```bash
# Test plusieurs nationalités
for nat in "Français" "Nigérian" "Chinois" "Brésilien" "Australien"; do
  curl -s "http://localhost:8001/api/portraits/realistic/random?nationality=$nat&gender=M" | jq -r '.portrait'
done
```

---

## 🔧 Dépendances

### Python
- `playwright` : Automatisation du navigateur pour téléchargement
- `pyee` : Gestion des événements asynchrones

### Installation
```bash
pip install playwright pyee
python -m playwright install chromium
```

---

## 📈 Performances

### Temps de téléchargement
- **8 portraits par lot** (~8 secondes par lot)
- **Pause entre lots** : 3-5 secondes
- **Temps total estimé** : 3-4 heures pour 7200 portraits

### Taille des fichiers
- **Taille moyenne** : ~50-100 KB par portrait
- **Taille totale** : ~400-700 MB pour 7200 portraits

### Cache backend
- Cache intelligent avec TTL de 5 minutes
- Évite les scans répétés du système de fichiers
- Rafraîchissement automatique si nécessaire

---

## 🐛 Dépannage

### Le script s'arrête pendant le téléchargement

**Problème** : Timeout ou erreur réseau

**Solution** :
```bash
# Relancer le script (reprise automatique)
cd /app/backend
nohup python3 download_realistic_portraits_optimized.py > /tmp/portrait_download.log 2>&1 &
```

### Les portraits ne s'affichent pas

**Vérifier** :
1. Le backend utilise-t-il le bon service ?
   ```bash
   grep -n "RealisticPortraitService" /app/backend/services/game_service.py
   ```

2. Les portraits sont-ils téléchargés ?
   ```bash
   find /app/backend/static/realistic_portraits -name "*.jpg" | wc -l
   ```

3. L'API retourne-t-elle des portraits ?
   ```bash
   curl -s http://localhost:8001/api/portraits/realistic/stats | jq '.stats.total'
   ```

### Erreur "Module not found: playwright"

**Solution** :
```bash
pip install playwright pyee
python -m playwright install chromium
```

---

## 🎯 Roadmap future

- [ ] Compléter les 197 portraits manquants (Océanie principalement)
- [ ] Ajouter plus d'ethnies si nécessaire
- [ ] Optimiser la taille des images (compression)
- [ ] Ajouter un système de backup/restore
- [ ] Créer un dashboard de monitoring en temps réel

---

## 📝 Notes importantes

1. **Compatibilité rétroactive** : L'ancien système de calques reste fonctionnel comme fallback
2. **Migration automatique** : Dès qu'un portrait réaliste est disponible, il est utilisé automatiquement
3. **Pas de modification de données** : Aucune migration de base de données nécessaire
4. **Performance** : Le système utilise un cache pour optimiser les requêtes répétées

---

## 👥 Contact et support

Pour toute question ou problème, référez-vous à la documentation technique dans :
- `services/realistic_portrait_service.py`
- `services/game_service.py`
- `components/LayeredPortrait.jsx`
