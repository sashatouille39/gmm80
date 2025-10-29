# Générateur Automatique de 7200 Portraits Réalistes

## 📋 Vue d'ensemble

Ce système télécharge et organise automatiquement **7200 portraits photo-réalistes** répartis par continents et genres :

- **6 continents** : Afrique, Asie, Europe, Amérique du Nord, Amérique du Sud, Océanie
- **2 genres par continent** : Homme, Femme
- **600 images par genre** = **1200 images par continent**

## 🎯 Objectif

Remplacer le système de calques par des portraits complets en une seule image, classés automatiquement par origine géographique et genre.

## 🔧 Technologies utilisées

- **thispersondoesnotexist.com** : Source gratuite d'images AI
- **DeepFace** : Classification automatique (ethnicité, genre, âge)
- **Python + TensorFlow** : Traitement et analyse

## 📦 Installation

Toutes les dépendances sont déjà installées :
```bash
# Déjà fait automatiquement
pip install deepface opencv-python-headless tf-keras tensorflow tqdm
```

## 🚀 Utilisation

### Option 1 : Pipeline Complet (Recommandé)

Exécute automatiquement les 3 étapes :

```bash
cd /app/backend
python generate_portraits_pipeline.py
```

**Temps estimé** : 2-3 heures  
**Interaction** : Minimale (confirmation au début)

### Option 2 : Exécution Étape par Étape

#### Étape 1 : Téléchargement (~30-60 min)
```bash
python download_random_faces.py
```
- Télécharge ~12,000 images aléatoires
- Images stockées dans `/app/backend/static/portraits/temp/`
- Peut être interrompu et repris (Ctrl+C)

#### Étape 2 : Classification (~1-2h)
```bash
python classify_faces.py
```
- Analyse chaque image avec DeepFace
- Détecte : ethnicité, genre, âge
- Résultats dans `classification_results.json`
- Traitement par lots pour optimiser la mémoire

#### Étape 3 : Réorganisation (~5 min)
```bash
python reorganize_faces.py
```
- Copie les images dans les dossiers finaux
- Structure : `/portraits/{continent}/{genre}/`
- Distribution automatique pour continents mixtes

## 📁 Structure Finale

```
/app/backend/static/portraits/
├── africa/
│   ├── male/ (600 images)
│   └── female/ (600 images)
├── asia/
│   ├── male/ (600 images)
│   └── female/ (600 images)
├── europe/
│   ├── male/ (600 images)
│   └── female/ (600 images)
├── north_america/
│   ├── male/ (600 images - mix White/Latino)
│   └── female/ (600 images - mix White/Latino)
├── south_america/
│   ├── male/ (600 images)
│   └── female/ (600 images)
└── oceania/
    ├── male/ (600 images - mix White/Asian)
    └── female/ (600 images - mix White/Asian)
```

## 🧪 Tests Rapides

### Test de téléchargement (10 images)
```bash
python test_quick_download.py
```

### Test de classification (5 images)
```bash
python test_quick_classify.py
```

## 🔍 Mapping Ethnicité → Continent

| Ethnicité DeepFace | Continent |
|-------------------|-----------|
| Black | Africa |
| Asian | Asia |
| Indian | Asia |
| White | Europe |
| Latino Hispanic | South America |
| Middle Eastern | Europe (réparti) |

**Continents mixtes** :
- **North America** : 50% White + 50% Latino Hispanic
- **Oceania** : 50% White + 50% Asian

## ⚙️ Paramètres Configurables

### download_random_faces.py
- `total_images` : Nombre d'images à télécharger (défaut: 12000)
- `batch_size` : Pause toutes les N images (défaut: 100)

### classify_faces.py
- `batch_size` : Nombre d'images avant nettoyage mémoire (défaut: 50)
- `detector_backend` : 'opencv', 'mtcnn', 'retinaface' (défaut: 'opencv')

### reorganize_faces.py
- `TARGET_PER_GENDER` : Nombre d'images par genre (défaut: 600)

## 🛠️ Dépannage

### Problème : Mémoire insuffisante
```bash
# Réduire le batch_size dans classify_faces.py
# Ou redémarrer le script (il reprend où il s'est arrêté)
```

### Problème : Images manquantes après réorganisation
```bash
# Télécharger plus d'images et relancer
python download_random_faces.py  # Télécharge plus d'images
python classify_faces.py         # Classifie les nouvelles
python reorganize_faces.py       # Réorganise
```

### Problème : Téléchargement lent
```bash
# Normal. Le serveur limite parfois les requêtes.
# Le script gère automatiquement les pauses et retries.
```

## 📊 Suivi de Progression

Tous les scripts sauvegardent leur progression :
- **Téléchargement** : Fichiers dans `/temp/` (reprend automatiquement)
- **Classification** : `classification_results.json` (sauvegarde tous les 50 images)
- **Réorganisation** : Fichiers dans dossiers finaux

Vous pouvez **interrompre à tout moment** (Ctrl+C) et **relancer** le script.

## 📝 Logs et Statistiques

Chaque étape affiche :
- ✅ Nombre d'images traitées
- ⚠️ Nombre d'échecs
- 📊 Distribution par catégorie
- ⏱️ Temps écoulé

## 🎉 Résultat Final

Après exécution complète :
- ✅ 7200 portraits photo-réalistes
- ✅ Classés automatiquement par continent et genre
- ✅ Prêts à utiliser dans votre application
- ✅ Format : JPG, haute qualité (500-600 KB par image)

## 💡 Conseils

1. **Première exécution** : DeepFace télécharge des modèles (~500MB) - soyez patient
2. **Connexion internet** : Nécessaire uniquement pour l'étape 1 (téléchargement)
3. **Espace disque** : Prévoir ~10GB (12000 images + modèles)
4. **Patience** : Le processus complet prend 2-3 heures

## 🔗 Intégration dans l'application

Les portraits sont accessibles via :
```
http://your-domain/static/portraits/{continent}/{gender}/portrait_XXXX.jpg
```

Exemple :
```
/static/portraits/africa/male/portrait_0001.jpg
/static/portraits/asia/female/portrait_0250.jpg
```

## 📄 Fichiers Générés

- `temp/` : Images téléchargées brutes (~12000)
- `classification_results.json` : Résultats d'analyse (~2MB)
- `{continent}/{gender}/` : Images finales organisées (7200)

## ⚡ Performance

- **Téléchargement** : ~1.5s par image
- **Classification** : ~2-3s par image (première fois), ~1s ensuite
- **Réorganisation** : Instantané (copie de fichiers)

---

**Prêt à démarrer ?**
```bash
cd /app/backend
python generate_portraits_pipeline.py
```
