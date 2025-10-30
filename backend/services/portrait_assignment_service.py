"""
Service de gestion des assignations de portraits réalistes
Assure qu'aucun portrait n'est utilisé deux fois
"""
import json
from pathlib import Path
from typing import Dict, Set, Optional, Tuple
from datetime import datetime
from services.realistic_portrait_service import RealisticPortraitService


class PortraitAssignmentService:
    """Service pour gérer les assignations uniques de portraits"""
    
    ASSIGNMENT_FILE = Path("/app/backend/data/portrait_assignments.json")
    
    def __init__(self):
        """Initialise le service"""
        self.realistic_service = RealisticPortraitService()
        self.assignments = self._load_assignments()
        
    def _load_assignments(self) -> Dict[str, Set[str]]:
        """
        Charge les assignations depuis le fichier JSON
        
        Returns:
            Dict avec la structure: {
                "continent_ethnicity_gender": ["portrait_path1", "portrait_path2", ...]
            }
        """
        if not self.ASSIGNMENT_FILE.exists():
            return {}
        
        try:
            with open(self.ASSIGNMENT_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Convertir les listes en sets pour des recherches plus rapides
                return {key: set(value) for key, value in data.items()}
        except Exception as e:
            print(f"⚠️ Erreur lors du chargement des assignations: {e}")
            return {}
    
    def _save_assignments(self):
        """Sauvegarde les assignations dans le fichier JSON"""
        try:
            # Créer le dossier data s'il n'existe pas
            self.ASSIGNMENT_FILE.parent.mkdir(parents=True, exist_ok=True)
            
            # Convertir les sets en listes pour la sérialisation JSON
            data = {key: list(value) for key, value in self.assignments.items()}
            
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
        gender: str
    ) -> Optional[str]:
        """
        Sélectionne un portrait unique qui n'a pas encore été assigné
        
        Args:
            nationality: La nationalité du joueur
            gender: Le genre ('M' ou 'F')
            
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
        
        # Obtenir la clé d'assignation
        assignment_key = self._get_assignment_key(continent, ethnicity, gender)
        
        # Obtenir les portraits déjà assignés
        assigned_portraits = self.assignments.get(assignment_key, set())
        
        # Filtrer pour ne garder que les portraits non assignés
        available_paths = [
            str(p).replace('/app/backend/static', '/static') 
            for p in available_portraits
        ]
        unassigned = [p for p in available_paths if p not in assigned_portraits]
        
        if not unassigned:
            print(f"⚠️ Tous les portraits de {continent}/{ethnicity}/{gender} sont déjà assignés ({len(assigned_portraits)} utilisés)")
            # Tous les portraits sont utilisés, on peut soit :
            # 1. Retourner None (pas de portrait)
            # 2. Réutiliser un portrait aléatoire (moins idéal)
            # 3. Lever une exception
            # Pour l'instant, on retourne None
            return None
        
        # Sélectionner aléatoirement parmi les non assignés
        import random
        selected = random.choice(unassigned)
        
        # Marquer comme assigné
        if assignment_key not in self.assignments:
            self.assignments[assignment_key] = set()
        self.assignments[assignment_key].add(selected)
        
        # Sauvegarder
        self._save_assignments()
        
        print(f"✅ Portrait assigné : {selected} ({len(assigned_portraits)+1}/{len(available_paths)} utilisés)")
        
        return selected
    
    def release_portrait(self, portrait_path: str):
        """
        Libère un portrait (le rend disponible à nouveau)
        Utile si un joueur est supprimé
        
        Args:
            portrait_path: Le chemin du portrait à libérer
        """
        for assignment_key, assigned_set in self.assignments.items():
            if portrait_path in assigned_set:
                assigned_set.remove(portrait_path)
                self._save_assignments()
                print(f"✅ Portrait libéré : {portrait_path}")
                return
        
        print(f"⚠️ Portrait non trouvé dans les assignations : {portrait_path}")
    
    def get_assignment_stats(self) -> Dict:
        """
        Retourne des statistiques sur les assignations
        
        Returns:
            Dict avec les stats d'utilisation par catégorie
        """
        stats = {}
        
        for assignment_key, assigned_set in self.assignments.items():
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
                
                stats[continent][ethnicity][gender] = {
                    "assigned": len(assigned_set),
                    "available": total_available,
                    "remaining": total_available - len(assigned_set),
                    "usage_percent": round((len(assigned_set) / total_available * 100), 1) if total_available > 0 else 0
                }
        
        return stats
    
    def reset_assignments(self):
        """
        Réinitialise toutes les assignations
        Utile pour recommencer une nouvelle partie
        """
        self.assignments = {}
        self._save_assignments()
        print("✅ Toutes les assignations ont été réinitialisées")
    
    def get_total_assigned(self) -> int:
        """Retourne le nombre total de portraits assignés"""
        return sum(len(assigned_set) for assigned_set in self.assignments.values())
    
    def get_total_remaining(self) -> int:
        """Retourne le nombre total de portraits encore disponibles"""
        total_available = 7200  # Notre collection complète
        total_assigned = self.get_total_assigned()
        return total_available - total_assigned
