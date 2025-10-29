# Système de Portraits par Calques

## 📝 Description

Le système de portraits par calques utilise l'IA (gpt-image-1 via OpenAI) pour générer des portraits modulaires composés de 5 calques PNG transparents :

- **Base** : Forme de tête avec teinte de peau
- **Yeux** : Yeux cohérents avec la région
- **Cheveux** : Coupes variées (100+ styles différents)
- **Bouche** : Bouche adaptée à l'ethnicité  
- **Nez** : Nez adapté à l'ethnicité

Ces calques sont **assemblés aléatoirement** pour créer des milliers de combinaisons uniques, tout en restant cohérents avec la nationalité et le sexe du personnage.

## 🎨 Architecture

### Backend
- `services/portrait_generator_service.py` : Service principal de génération
- `routes/portrait_routes.py` : API endpoints pour générer des portraits
- `models/game_models.py` : Modèle PlayerPortrait avec champs layer_*
- `static/portraits/` : Stockage des calques PNG

### Frontend
- `components/LayeredPortrait.jsx` : Composant React qui affiche les calques superposés
- Intégré dans : GameSetup, GameArena, FinalRanking, CustomPlayersList

## 🚀 Utilisation

### Option 1 : Génération d'échantillon (recommandé pour tester)

Générez un petit échantillon de calques pour voir le système en action :

```bash
cd /app/backend
python scripts/generate_sample_library.py
```

Cela génère ~90 calques (3 variations × 5 types × 6 combinaisons nationalité/genre).

### Option 2 : Génération complète de bibliothèque

Pour une bibliothèque complète avec centaines de variations :

```bash
cd /app/backend
python scripts/generate_portrait_library.py
```

⚠️ **Attention** : Cela génère ~10,000+ calques et peut prendre plusieurs heures et coûter en crédits API.

### Option 3 : Génération à la demande via API

Les portraits peuvent aussi être générés à la demande via l'API :

```bash
# Générer un portrait complet pour un français
curl -X POST http://localhost:8001/api/portraits/generate \
  -H "Content-Type: application/json" \
  -d '{"nationality": "Français", "gender": "male", "age": 25, "variations": 1}'
```

## 🎭 Fonctionnement

### 1. Génération des calques

Chaque calque est généré avec des prompts IA spécifiques qui garantissent :
- Cohérence avec la nationalité (12 régions définies)
- Palettes de couleurs appropriées (peau, cheveux, yeux)
- Transparence PNG pour la superposition
- Variations multiples pour diversité

### 2. Assemblage aléatoire

Quand un joueur est généré dans le jeu :

```python
# Le système sélectionne UN calque aléatoire de chaque type
portrait_layers = portrait_service.assemble_random_layers(region, gender)

# Résultat : 
{
  'base': '/static/portraits/base/western_european_M_age25_3_base.png',
  'eyes': '/static/portraits/eyes/western_european_M_age25_7_eyes.png',
  'hair': '/static/portraits/hair/western_european_M_age25_42_hair.png',
  'mouth': '/static/portraits/mouth/western_european_M_age25_15_mouth.png',
  'nose': '/static/portraits/nose/western_european_M_age25_9_nose.png'
}
```

### 3. Affichage frontend

Le composant `LayeredPortrait` superpose les images avec z-index approprié :

```jsx
<LayeredPortrait 
  player={player} 
  size="medium"  // tiny | small | medium | large | xlarge
  showNumber={true}
/>
```

Les calques sont empilés : Base → Nez → Bouche → Yeux → Cheveux (au-dessus)

## 📊 Régions et Nationalités

Le système supporte 12 régions avec palettes de couleurs spécifiques :

- **nordic** : Scandinaves (Suédois, Norvégien, etc.)
- **western_european** : Europe de l'Ouest (Français, Allemand, etc.)
- **mediterranean** : Europe du Sud (Italien, Espagnol, Grec)
- **eastern_european** : Europe de l'Est (Russe, Polonais, etc.)
- **east_asian** : Asie de l'Est (Chinois, Japonais, Coréen)
- **south_asian** : Asie du Sud (Indien)
- **southeast_asian** : Asie du Sud-Est (Thaïlandais, Indonésien)
- **middle_eastern** : Moyen-Orient (Turc, Iranien, Afghan)
- **north_african** : Afrique du Nord (Marocain, Égyptien)
- **african** : Afrique sub-saharienne (Nigérian)
- **latino** : Amérique Latine (Mexicain, Argentin)
- **mixed** : Mixte (Américain, Canadien, Australien, Brésilien)

## 🔧 Configuration

### Clé API

La clé EMERGENT_LLM_KEY doit être configurée dans `/app/backend/.env` :

```bash
EMERGENT_LLM_KEY=sk-emergent-VOTRE_CLE
```

### Paramètres de génération

Dans `scripts/generate_portrait_library.py` :

```python
CALQUES_CONFIG = {
    'base': 40,      # 40 bases différentes par région/sexe
    'eyes': 30,      # 30 types d'yeux
    'hair': 100,     # 100 coupes de cheveux (le plus varié)
    'mouth': 25,     # 25 bouches
    'nose': 25       # 25 nez
}
```

## 🎯 Avantages

✅ **Modulaire** : Des milliers de combinaisons à partir de centaines de calques
✅ **Économique** : Génération une fois, réutilisation infinie
✅ **Cohérent** : Respecte nationalité, région, couleurs de peau
✅ **Performant** : Pas de génération IA en temps réel dans le jeu
✅ **Évolutif** : Facile d'ajouter plus de variations

## 📝 Fallback

Si aucun calque n'est disponible, le système utilise automatiquement :
1. **Portraits simples Pillow** : Générés à la volée avec couleurs cohérentes
2. **Cercles colorés** : Affichage minimal avec numéro du joueur

## 🐛 Dépannage

### Les portraits n'apparaissent pas
- Vérifier que les calques sont générés : `ls /app/backend/static/portraits/base/`
- Vérifier les logs backend : `tail -f /var/log/supervisor/backend.err.log`
- Tester l'assemblage : `cd /app/backend && python scripts/test_portrait_system.py`

### Erreur "Module not found"
- Installer les dépendances : `cd /app/backend && pip install -r requirements.txt`

### Images ne se chargent pas
- Vérifier que `/api/static/portraits/` est accessible
- Regarder la console navigateur pour erreurs réseau

## 📚 Fichiers importants

```
/app/backend/
├── services/
│   └── portrait_generator_service.py  # Logique principale
├── routes/
│   └── portrait_routes.py            # API endpoints
├── scripts/
│   ├── generate_sample_library.py    # Échantillon rapide
│   ├── generate_portrait_library.py  # Bibliothèque complète
│   └── test_portrait_system.py       # Tests
└── static/
    └── portraits/                    # Stockage calques
        ├── base/
        ├── eyes/
        ├── hair/
        ├── mouth/
        └── nose/

/app/frontend/src/
└── components/
    └── LayeredPortrait.jsx           # Composant affichage
```

## 🎉 Résultat

Les joueurs du jeu affichent maintenant des portraits uniques générés par IA, avec des centaines de variations possibles qui respectent leur nationalité et leur sexe !
