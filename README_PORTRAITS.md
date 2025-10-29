# Système de Génération de Portraits par Calques

## 📋 Aperçu

Le système génère des portraits de joueurs composés de **5 calques PNG superposés**, cohérents avec la **nationalité** et le **sexe** du personnage:

1. **Base** - Forme de la tête et couleur de peau
2. **Nez** - Nez cohérent avec l'ethnie
3. **Bouche** - Bouche avec expression
4. **Yeux** - Yeux avec couleur cohérente
5. **Cheveux** - Coiffure variée (12+ variations par nationalité/sexe)

## 🌍 Régions Géographiques Supportées

Le système utilise des palettes de couleurs et caractéristiques spécifiques par continent:

- **Europe du Nord** (Nordique) - Peau claire, cheveux blonds, yeux bleus
- **Europe de l'Ouest** - Varié, peaux claires à moyennes
- **Europe du Sud** (Méditerranéen) - Peau olive, cheveux bruns/noirs
- **Europe de l'Est** - Cheveux blonds/châtains, yeux clairs
- **Asie de l'Est** - Cheveux noirs raides, traits asiatiques
- **Asie du Sud** - Peau plus foncée, cheveux noirs
- **Asie du Sud-Est** - Peau tan/olive
- **Moyen-Orient** - Peau olive, cheveux noirs/bruns
- **Afrique du Nord** - Peau tan/olive
- **Afrique Sub-Saharienne** - Peau foncée, cheveux crépus
- **Amérique Latine** - Varié, peau olive/brune
- **Amérique du Nord / Mixte** - Très varié

## 📁 Structure des Fichiers

```
/app/backend/static/portraits/
├── base/      # Calques de base (tête avec peau)
├── eyes/      # Calques d'yeux
├── hair/      # Calques de cheveux (12+ variations)
├── mouth/     # Calques de bouche
└── nose/      # Calques de nez
```

Nomenclature des fichiers:
```
{region}_{gender}_{age}_{variation_id}_{layer_type}.png

Exemple:
  nordic_M_age25_1_base.png      # Base pour homme nordique, 25 ans, variation 1
  nordic_M_age25_1_hair.png      # Cheveux pour même personnage
  east_asian_F_age25_5_eyes.png  # Yeux pour femme asiatique, variation 5
```

## 🚀 Scripts de Génération

### 1. Génération Rapide (Pillow - Instantané)

```bash
cd /app/backend
python generate_simple_portraits.py
```

Génère des portraits simples avec des formes géométriques. **Idéal pour les tests immédiats.**

### 2. Génération de Démonstration (IA - 5-10 minutes)

```bash
cd /app/backend
python generate_demo_portraits.py
```

Génère 6 portraits via gpt-image-1:
- 2 portraits suédois (homme + femme)
- 2 portraits japonais (homme + femme)  
- 2 portraits nigérians (homme + femme)

**Temps estimé:** ~5-10 minutes

### 3. Génération Complète (IA - 3-5 heures)

```bash
cd /app/backend
python generate_portrait_layers.py
```

Génère une bibliothèque complète de calques pour:
- 20+ nationalités représentatives
- Hommes et femmes
- Variations multiples (3 bases, 3 yeux, **12 cheveux**, 3 bouches, 3 nez)

**Temps estimé:** 3-5 heures (peut être lancé en arrière-plan)

## 🔧 Intégration dans le Code

### Backend (Python)

Le service `portrait_generator_service.py` gère la génération et la sélection:

```python
from services.portrait_generator_service import portrait_service

# Générer un portrait complet
layers = await portrait_service.generate_portrait_layers_set(
    nationality='Japonais',
    gender='male',
    age=25,
    set_id=1
)

# Sélectionner un portrait existant
layers = portrait_service.select_random_portrait_layers(
    nationality='Japonais',
    gender='M'
)
```

Les joueurs générés par `GameService` obtiennent automatiquement des calques via `_generate_portrait()`.

### Frontend (React)

Le composant `LayeredPortrait` affiche les portraits:

```jsx
import LayeredPortrait from './LayeredPortrait';

// Utilisation
<LayeredPortrait 
  player={player}           // Objet joueur avec portrait.layer_*
  size="medium"            // 'tiny', 'small', 'medium', 'large', 'xlarge'
  showNumber={true}        // Afficher le numéro du joueur
  className="custom-class" // Classes CSS additionnelles
/>
```

**Fallback automatique:** Si les calques n'existent pas, affiche un avatar simple.

## 🎨 Personnalisation

### Ajouter une Nouvelle Nationalité

1. **Backend** - Ajouter dans `portrait_generator_service.py`:

```python
NATIONALITY_TO_REGION = {
    # ...
    'Thaïlandais': 'southeast_asian',  # Nouvelle nationalité
}
```

2. **Générer les calques:**

```bash
python generate_portrait_layers.py
# Sélectionner la nationalité dans le menu
```

### Ajuster les Variations de Cheveux

Dans `generate_portrait_layers.py`, modifier:

```python
hair_variations = 15  # Augmenter pour plus de coupes de cheveux
```

## 🧪 Tests

### Test Backend

```bash
cd /app/backend
python test_player_layers.py
```

Génère 5 joueurs de nationalités différentes et vérifie que tous les calques sont présents.

### Test Frontend

1. Lancer l'application: `http://localhost:3000`
2. Aller dans "Jouer" → "Générer des joueurs"
3. Les portraits devraient s'afficher avec les calques superposés

## 📊 Performance

- **Génération simple (Pillow):** <1 seconde par portrait
- **Génération IA (gpt-image-1):** ~15-20 secondes par calque (~1-2 minutes par portrait complet)
- **Chargement frontend:** Instantané (images PNG optimisées)

## 🔑 Prérequis

- **EMERGENT_LLM_KEY** configurée dans `/app/backend/.env`
- **Dépendances Python:**
  - `emergentintegrations >= 0.1.0`
  - `litellm >= 1.79.0`
  - `Pillow >= 10.0.0`

## 📝 Notes

- Les calques sont **réutilisables et mixables** entre eux
- Le système favorise la **cohérence ethnique** (couleur de peau, traits, cheveux)
- Les portraits sont **automatiquement attribués** lors de la génération de joueurs
- **12+ variations de cheveux** par nationalité/sexe pour plus de diversité
- Système de **fallback** si aucun calque n'est disponible

## 🚀 Prochaines Étapes

1. Lancer `generate_simple_portraits.py` pour tester immédiatement
2. Lancer `generate_demo_portraits.py` pour quelques portraits IA
3. Optionnel: Lancer `generate_portrait_layers.py` en arrière-plan pour la bibliothèque complète
4. Tester l'affichage dans le jeu

## ✅ Statut Actuel

- ✅ Service de génération de calques créé
- ✅ Composant React LayeredPortrait créé
- ✅ Intégration dans GameArena.jsx
- ✅ Intégration dans GameSetup.jsx
- ✅ Routes statiques configurées (/static/portraits/)
- ✅ Portraits simples générés (6 portraits de test)
- ✅ Système de fallback fonctionnel
- ⏳ Génération IA complète (à lancer selon besoin)

---

**Développé pour le jeu Squid Game - Système de portraits cohérents avec la nationalité**
