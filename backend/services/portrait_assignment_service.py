"""
Service de gestion des assignations de portraits réalistes
Assure qu'aucun portrait n'est utilisé deux fois DANS LA MÊME PARTIE
"""
import json
from pathlib import Path
from typing import Dict, Set, Optional, Tuple
from datetime import datetime
from services.realistic_portrait_service import RealisticPortraitService


class PortraitAssignmentService:
    """Service pour gérer les assignations uniques de portraits PAR PARTIE"""
    
    ASSIGNMENT_FILE = Path("/app/backend/data/portrait_assignments_by_game.json")
    
    def __init__(self):
        """Initialise le service"""
        self.realistic_service = RealisticPortraitService()
        self.assignments = self._load_assignments()
        
    def _load_assignments(self) -> Dict[str, Dict[str, Set[str]]]:
        """
        Charge les assignations depuis le fichier JSON
        
        Returns:
            Dict avec la structure: {
                "game_id": {
                    "continent_ethnicity_gender": ["portrait_path1", "portrait_path2", ...]
                }
            }
        """
        if not self.ASSIGNMENT_FILE.exists():
            return {}
        
        try:
            with open(self.ASSIGNMENT_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Convertir les listes en sets pour des recherches plus rapides
                result = {}
                for game_id, game_data in data.items():
                    result[game_id] = {key: set(value) for key, value in game_data.items()}
                return result
        except Exception as e:
            print(f"⚠️ Erreur lors du chargement des assignations: {e}")
            return {}
    
    def _save_assignments(self):
        """Sauvegarde les assignations dans le fichier JSON"""
        try:
            # Créer le dossier data s'il n'existe pas
            self.ASSIGNMENT_FILE.parent.mkdir(parents=True, exist_ok=True)
            
            # Convertir les sets en listes pour la sérialisation JSON
            data = {}
            for game_id, game_data in self.assignments.items():
                data[game_id] = {key: list(value) for key, value in game_data.items()}
            
            with open(self.ASSIGNMENT_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️ Erreur lors de la sauvegarde des assignations: {e}")
    
    def _get_assignment_key(self, continent: str, ethnicity: str, gender: str) -> str:
        """Génère une clé unique pour une catégorie de portrait"""
        return f"{continent}_{ethnicity}_{gender}"
    
    def get_unique_portrait(
        self, 
        nationality: str, 
        gender: str,
        game_id: str = "default"
    ) -> Optional[str]:
        """
        Sélectionne un portrait unique qui n'a pas encore été assigné DANS CETTE PARTIE
        
        Args:
            nationality: La nationalité du joueur
            gender: Le genre ('M' ou 'F')
            game_id: L'identifiant de la partie (pour isoler les assignations)
            
        Returns:
            Le chemin relatif vers le portrait unique, ou None si tous sont utilisés
        """
        # Obtenir le continent et l'ethnie
        continent, ethnicity = self.realistic_service.get_continent_and_ethnicity(nationality)
        
        # Obtenir tous les portraits disponibles
        available_portraits = self.realistic_service.get_available_portraits(
            continent, ethnicity, gender
        )
        
        if not available_portraits:
            print(f"⚠️ Aucun portrait disponible pour {nationality} ({gender})")
            return None
        
        # Initialiser les assignations pour cette partie si nécessaire
        if game_id not in self.assignments:
            self.assignments[game_id] = {}
        
        # Obtenir la clé d'assignation
        assignment_key = self._get_assignment_key(continent, ethnicity, gender)
        
        # Obtenir les portraits déjà assignés DANS CETTE PARTIE
        assigned_portraits = self.assignments[game_id].get(assignment_key, set())
        
        # Filtrer pour ne garder que les portraits non assignés
        available_paths = [
            str(p).replace('/app/backend/static', '/api/static') 
            for p in available_portraits
        ]
        unassigned = [p for p in available_paths if p not in assigned_portraits]
        
        if not unassigned:
            print(f"⚠️ Tous les portraits de {continent}/{ethnicity}/{gender} sont déjà assignés dans cette partie ({len(assigned_portraits)} utilisés)")
            # Tous les portraits sont utilisés dans cette partie
            return None
        
        # Sélectionner aléatoirement parmi les non assignés
        import random
        selected = random.choice(unassigned)
        
        # Marquer comme assigné POUR CETTE PARTIE
        if assignment_key not in self.assignments[game_id]:
            self.assignments[game_id][assignment_key] = set()
        self.assignments[game_id][assignment_key].add(selected)
        
        # Sauvegarder
        self._save_assignments()
        
        print(f"✅ Portrait assigné [Game: {game_id}]: {selected} ({len(assigned_portraits)+1}/{len(available_paths)} utilisés dans cette partie)")
        
        return selected
    
    def release_portrait(self, portrait_path: str, game_id: str = "default"):
        """
        Libère un portrait (le rend disponible à nouveau) DANS UNE PARTIE SPÉCIFIQUE
        Utile si un joueur est supprimé
        
        Args:
            portrait_path: Le chemin du portrait à libérer
            game_id: L'identifiant de la partie
        """
        if game_id not in self.assignments:
            print(f"⚠️ Aucune assignation trouvée pour la partie : {game_id}")
            return
            
        for assignment_key, assigned_set in self.assignments[game_id].items():
            if portrait_path in assigned_set:
                assigned_set.remove(portrait_path)
                self._save_assignments()
                print(f"✅ Portrait libéré [Game: {game_id}]: {portrait_path}")
                return
        
        print(f"⚠️ Portrait non trouvé dans les assignations de la partie {game_id}: {portrait_path}")
    
    def release_game_portraits(self, game_id: str):
        """
        Libère TOUS les portraits d'une partie (quand la partie est terminée)
        
        Args:
            game_id: L'identifiant de la partie à libérer
        """
        if game_id in self.assignments:
            total_released = sum(len(assigned_set) for assigned_set in self.assignments[game_id].values())
            del self.assignments[game_id]
            self._save_assignments()
            print(f"✅ Tous les portraits de la partie {game_id} ont été libérés ({total_released} portraits)")
        else:
            print(f"⚠️ Aucune assignation trouvée pour la partie : {game_id}")
    
    def get_assignment_stats(self, game_id: str = None) -> Dict:
        """
        Retourne des statistiques sur les assignations
        
        Args:
            game_id: Si fourni, retourne les stats pour cette partie uniquement.
                    Sinon, retourne les stats globales de toutes les parties.
        
        Returns:
            Dict avec les stats d'utilisation par catégorie
        """
        stats = {}
        
        # Si game_id spécifique, analyser seulement cette partie
        games_to_analyze = {game_id: self.assignments.get(game_id, {})} if game_id else self.assignments
        
        for gid, game_assignments in games_to_analyze.items():
            for assignment_key, assigned_set in game_assignments.items():
                parts = assignment_key.split('_')
                if len(parts) >= 3:
                    continent = parts[0]
                    ethnicity = '_'.join(parts[1:-1])  # Gérer les ethnies avec underscore (ex: latino_hispanic)
                    gender = parts[-1]
                    
                    # Obtenir le total disponible
                    available = self.realistic_service.get_available_portraits(
                        continent, ethnicity, gender
                    )
                    total_available = len(available)
                    
                    if continent not in stats:
                        stats[continent] = {}
                    if ethnicity not in stats[continent]:
                        stats[continent][ethnicity] = {}
                    
                    # Si on analyse plusieurs parties, cumuler les stats
                    if gender not in stats[continent][ethnicity]:
                        stats[continent][ethnicity][gender] = {
                            "assigned": 0,
                            "available": total_available,
                            "games": []
                        }
                    
                    stats[continent][ethnicity][gender]["assigned"] += len(assigned_set)
                    if game_id:
                        stats[continent][ethnicity][gender]["games"].append(gid)
        
        # Calculer les valeurs finales
        for continent in stats:
            for ethnicity in stats[continent]:
                for gender in stats[continent][ethnicity]:
                    assigned = stats[continent][ethnicity][gender]["assigned"]
                    available = stats[continent][ethnicity][gender]["available"]
                    stats[continent][ethnicity][gender]["remaining"] = available - assigned
                    stats[continent][ethnicity][gender]["usage_percent"] = round((assigned / available * 100), 1) if available > 0 else 0
        
        return stats
    
    def reset_assignments(self, game_id: str = None):
        """
        Réinitialise les assignations
        
        Args:
            game_id: Si fourni, réinitialise seulement cette partie.
                    Sinon, réinitialise TOUTES les parties.
        """
        if game_id:
            if game_id in self.assignments:
                del self.assignments[game_id]
                self._save_assignments()
                print(f"✅ Les assignations de la partie {game_id} ont été réinitialisées")
            else:
                print(f"⚠️ Aucune assignation trouvée pour la partie : {game_id}")
        else:
            self.assignments = {}
            self._save_assignments()
            print("✅ Toutes les assignations ont été réinitialisées")
    
    def get_total_assigned(self, game_id: str = None) -> int:
        """
        Retourne le nombre total de portraits assignés
        
        Args:
            game_id: Si fourni, compte seulement pour cette partie.
                    Sinon, compte toutes les parties.
        """
        if game_id:
            if game_id in self.assignments:
                return sum(len(assigned_set) for assigned_set in self.assignments[game_id].values())
            return 0
        else:
            total = 0
            for game_assignments in self.assignments.values():
                total += sum(len(assigned_set) for assigned_set in game_assignments.values())
            return total
    
    def get_total_remaining(self, game_id: str = None) -> int:
        """
        Retourne le nombre total de portraits encore disponibles
        
        Args:
            game_id: Si fourni, compte pour cette partie.
                    Sinon, donne une estimation globale.
        """
        total_available = 7081  # Notre collection actuelle après suppressions
        total_assigned = self.get_total_assigned(game_id)
        return total_available - total_assigned
    
    def get_active_games(self) -> list:
        """Retourne la liste des game_id ayant des portraits assignés"""
        return list(self.assignments.keys())
