# Système d'Unicité des Portraits par Partie

## 📝 Description

Le système garantit qu'**aucun portrait ne peut être utilisé deux fois dans la même partie**. Chaque joueur a un visage unique au sein d'une même partie, mais les portraits peuvent être réutilisés dans des parties différentes.

## 🎯 Fonctionnement

### 1. Attribution des Portraits

Quand une partie est créée :
1. Un `game_id` unique est généré **avant** la création des joueurs
2. Pour chaque joueur, un portrait aléatoire est sélectionné parmi ceux **non encore utilisés dans cette partie**
3. Le portrait est marqué comme "utilisé" pour cette partie spécifique
4. Les données sont sauvegardées dans `/app/backend/data/portrait_assignments_by_game.json`

### 2. Structure des Données

```json
{
  "game_id_1": {
    "europe_white_F": [
      "/api/static/realistic_portraits/europe/white/F/europe_white_F_21_35_0001.jpg",
      "/api/static/realistic_portraits/europe/white/F/europe_white_F_34_50_0042.jpg"
    ],
    "asia_asian_M": [
      "/api/static/realistic_portraits/asia/asian/M/asia_asian_M_21_35_0015.jpg"
    ]
  },
  "game_id_2": {
    "europe_white_F": [
      "/api/static/realistic_portraits/europe/white/F/europe_white_F_21_35_0003.jpg"
    ]
  }
}
```

### 3. Libération des Portraits

Quand une partie se termine (`game.completed = True`) :
- Tous les portraits de cette partie sont automatiquement **libérés**
- Ils redeviennent disponibles pour de nouvelles parties
- L'entrée de la partie est supprimée du fichier JSON

## 🔧 Composants Modifiés

### Backend Services

#### `portrait_assignment_service.py`
- **Changement principal** : Tracking par `game_id` au lieu de global
- **Méthodes clés** :
  - `get_unique_portrait(nationality, gender, game_id)` : Récupère un portrait unique pour cette partie
  - `release_game_portraits(game_id)` : Libère tous les portraits d'une partie
  - `get_assignment_stats(game_id)` : Statistiques d'utilisation par partie

#### `game_service.py`
- `_generate_portrait()` : Accepte maintenant un paramètre `game_id`
- `generate_multiple_players()` : Transmet le `game_id` lors de la génération

### Backend Routes

#### `game_routes.py`
- **create_game()** :
  - Génère un `game_id` **avant** de créer les joueurs
  - Transmet ce `game_id` lors de la génération des portraits
  - Utilise cet ID pour créer le Game
  
- **Libération automatique** dans 5 endpoints :
  - Après simulation d'événement (si partie terminée)
  - Après simulation temps réel (si partie terminée)
  - Après skip d'événement (si partie terminée)
  - Après simulation automatique complète
  - Après simulation par phases

## 📊 Statistiques

### Portraits Disponibles (après suppressions)
- Africa : 1,200 portraits
- America : 1,185 portraits  
- Asia : 1,176 portraits
- Europe : 1,136 portraits
- Middle East : 1,186 portraits
- Oceania : 1,198 portraits
- **Total : 7,081 portraits uniques**

### Capacité Théorique
Avec une distribution équilibrée, le système peut supporter :
- **~200 joueurs par partie** (avec 6 régions, ~35 portraits par région/genre)
- Réutilisation immédiate après fin de partie

## 🎮 Exemple d'Utilisation

### Création d'une Partie
```python
# Dans game_routes.py - create_game()
game_id = str(uuid.uuid4())  # Généré en premier

# Génération des joueurs avec game_id
portrait = GameService._generate_portrait(
    nationality="Français", 
    gender="M",
    game_id=game_id  # ← Garantit l'unicité dans cette partie
)

# Création du jeu avec l'ID pré-généré
game = Game(
    id=game_id,
    players=players,
    events=events
)
```

### Fin de Partie
```python
# Automatiquement appelé quand game.completed = True
release_game_portraits(game.id)
# → Tous les portraits de cette partie sont libérés
```

## 🛠️ API de Gestion

### Méthodes Utiles

```python
from services.portrait_assignment_service import PortraitAssignmentService

service = PortraitAssignmentService()

# Obtenir un portrait unique pour une partie
portrait = service.get_unique_portrait(
    nationality="Français",
    gender="F", 
    game_id="abc-123"
)

# Libérer tous les portraits d'une partie
service.release_game_portraits("abc-123")

# Statistiques d'une partie spécifique
stats = service.get_assignment_stats(game_id="abc-123")

# Statistiques globales (toutes les parties actives)
global_stats = service.get_assignment_stats()

# Lister les parties actives
active_games = service.get_active_games()

# Réinitialiser une partie spécifique
service.reset_assignments(game_id="abc-123")

# Réinitialiser TOUTES les parties
service.reset_assignments()
```

## ✅ Garanties du Système

1. **Unicité par Partie** : Aucun portrait ne peut apparaître deux fois dans la même partie
2. **Isolation des Parties** : Les portraits d'une partie A sont indépendants de la partie B
3. **Réutilisation Efficace** : Les portraits sont libérés immédiatement après la fin de partie
4. **Fallback Gracieux** : Si tous les portraits d'une catégorie sont utilisés, le système retourne None (fallback sur calques PNG)
5. **Persistance** : Les assignations sont sauvegardées sur disque et survivent aux redémarrages

## 🐛 Dépannage

### Problème : Tous les portraits sont utilisés
```
⚠️ Tous les portraits de europe/white/F sont déjà assignés dans cette partie
```
**Cause** : Plus de 200 joueurs européens blancs féminins dans une seule partie
**Solution** : Augmenter la bibliothèque de portraits ou limiter le nombre de joueurs

### Problème : Portraits non libérés
```python
# Vérifier les parties actives
service = PortraitAssignmentService()
print(service.get_active_games())

# Libérer manuellement une partie abandonnée
service.release_game_portraits("old-game-id")
```

### Problème : Fichier JSON corrompu
**Localisation** : `/app/backend/data/portrait_assignments_by_game.json`
**Solution** : Supprimer le fichier, il sera recréé automatiquement

## 📈 Améliorations Futures Possibles

1. **Nettoyage Automatique** : Supprimer les parties de plus de X jours
2. **Statistiques Détaillées** : Dashboard d'utilisation des portraits
3. **Pré-allocation** : Réserver des portraits avant la création complète de la partie
4. **Cache en Mémoire** : Optimiser les performances pour de très nombreuses parties simultanées

## 🎉 Résultat

Les joueurs d'une même partie ont maintenant **tous des visages différents** ! 🎭
