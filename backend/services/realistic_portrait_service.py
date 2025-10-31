"""
Service de gestion des portraits réalistes téléchargés depuis thispersonnotexist.org
Remplace le système de calques par des portraits complets semi-réalistes
Organisés par continent et ethnie
"""
import os
import random
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime

class RealisticPortraitService:
    """Service pour sélectionner des portraits réalistes selon la nationalité et le genre"""
    
    PORTRAITS_BASE_DIR = Path("/app/backend/static/realistic_portraits")
    
    # Mapping des nationalités vers les continents et ethnies
    NATIONALITY_TO_CONTINENT_ETHNICITY = {
        # AFRIQUE - Black (Afrique subsaharienne)
        'Angolais': ('africa', 'black'),
        'Angolaise': ('africa', 'black'),
        'Béninois': ('africa', 'black'),
        'Béninoise': ('africa', 'black'),
        'Botswanais': ('africa', 'black'),
        'Botswanaise': ('africa', 'black'),
        'Burkinabé': ('africa', 'black'),
        'Burundais': ('africa', 'black'),
        'Burundaise': ('africa', 'black'),
        'Camerounais': ('africa', 'black'),
        'Camerounaise': ('africa', 'black'),
        'Cap-Verdien': ('africa', 'black'),
        'Cap-Verdienne': ('africa', 'black'),
        'Centrafricain': ('africa', 'black'),
        'Centrafricaine': ('africa', 'black'),
        'Comorien': ('africa', 'black'),
        'Comorienne': ('africa', 'black'),
        'Congolais': ('africa', 'black'),
        'Congolaise': ('africa', 'black'),
        'Ivoirien': ('africa', 'black'),
        'Ivoirienne': ('africa', 'black'),
        'Djiboutien': ('africa', 'black'),
        'Djiboutienne': ('africa', 'black'),
        'Équato-Guinéen': ('africa', 'black'),
        'Équato-Guinéenne': ('africa', 'black'),
        'Érythréen': ('africa', 'black'),
        'Érythréenne': ('africa', 'black'),
        'Éthiopien': ('africa', 'black'),
        'Éthiopienne': ('africa', 'black'),
        'Gabonais': ('africa', 'black'),
        'Gabonaise': ('africa', 'black'),
        'Gambien': ('africa', 'black'),
        'Gambienne': ('africa', 'black'),
        'Ghanéen': ('africa', 'black'),
        'Ghanéenne': ('africa', 'black'),
        'Guinéen': ('africa', 'black'),
        'Guinéenne': ('africa', 'black'),
        'Bissau-Guinéen': ('africa', 'black'),
        'Bissau-Guinéenne': ('africa', 'black'),
        'Kényan': ('africa', 'black'),
        'Kényane': ('africa', 'black'),
        'Lesothan': ('africa', 'black'),
        'Lesothane': ('africa', 'black'),
        'Libérien': ('africa', 'black'),
        'Libérienne': ('africa', 'black'),
        'Malgache': ('africa', 'black'),
        'Malawite': ('africa', 'black'),
        'Malien': ('africa', 'black'),
        'Malienne': ('africa', 'black'),
        'Mauritanien': ('africa', 'black'),
        'Mauritanienne': ('africa', 'black'),
        'Mauricien': ('africa', 'black'),
        'Mauricienne': ('africa', 'black'),
        'Mozambicain': ('africa', 'black'),
        'Mozambicaine': ('africa', 'black'),
        'Namibien': ('africa', 'black'),
        'Namibienne': ('africa', 'black'),
        'Nigérien': ('africa', 'black'),
        'Nigérienne': ('africa', 'black'),
        'Nigérian': ('africa', 'black'),
        'Nigériane': ('africa', 'black'),
        'Ougandais': ('africa', 'black'),
        'Ougandaise': ('africa', 'black'),
        'Rwandais': ('africa', 'black'),
        'Rwandaise': ('africa', 'black'),
        'Sao-Toméen': ('africa', 'black'),
        'Sao-Toméenne': ('africa', 'black'),
        'Sénégalais': ('africa', 'black'),
        'Sénégalaise': ('africa', 'black'),
        'Seychellois': ('africa', 'black'),
        'Seychelloise': ('africa', 'black'),
        'Sierra-Léonais': ('africa', 'black'),
        'Sierra-Léonaise': ('africa', 'black'),
        'Somalien': ('africa', 'black'),
        'Somalienne': ('africa', 'black'),
        'Sud-Africain': ('africa', 'black'),
        'Sud-Africaine': ('africa', 'black'),
        'Sud-Soudanais': ('africa', 'black'),
        'Sud-Soudanaise': ('africa', 'black'),
        'Soudanais': ('africa', 'black'),
        'Soudanaise': ('africa', 'black'),
        'Swazi': ('africa', 'black'),
        'Swazie': ('africa', 'black'),
        'Tanzanien': ('africa', 'black'),
        'Tanzanienne': ('africa', 'black'),
        'Tchadien': ('africa', 'black'),
        'Tchadienne': ('africa', 'black'),
        'Togolais': ('africa', 'black'),
        'Togolaise': ('africa', 'black'),
        'Zambien': ('africa', 'black'),
        'Zambienne': ('africa', 'black'),
        'Zimbabwéen': ('africa', 'black'),
        'Zimbabwéenne': ('africa', 'black'),
        
        # ASIE - Asian (Asie de l'Est et du Sud-Est)
        'Chinois': ('asia', 'asian'),
        'Chinoise': ('asia', 'asian'),
        'Japonais': ('asia', 'asian'),
        'Japonaise': ('asia', 'asian'),
        'Coréen': ('asia', 'asian'),
        'Coréenne': ('asia', 'asian'),
        'Mongol': ('asia', 'asian'),
        'Mongole': ('asia', 'asian'),
        'Taïwanais': ('asia', 'asian'),
        'Taïwanaise': ('asia', 'asian'),
        'Hongkongais': ('asia', 'asian'),
        'Hongkongaise': ('asia', 'asian'),
        'Vietnamien': ('asia', 'asian'),
        'Vietnamienne': ('asia', 'asian'),
        'Thaïlandais': ('asia', 'asian'),
        'Thaïlandaise': ('asia', 'asian'),
        'Cambodgien': ('asia', 'asian'),
        'Cambodgienne': ('asia', 'asian'),
        'Laotien': ('asia', 'asian'),
        'Laotienne': ('asia', 'asian'),
        'Birman': ('asia', 'asian'),
        'Birmane': ('asia', 'asian'),
        'Malaisien': ('asia', 'asian'),
        'Malaisienne': ('asia', 'asian'),
        'Singapourien': ('asia', 'asian'),
        'Singapourienne': ('asia', 'asian'),
        'Philippin': ('asia', 'asian'),
        'Philippine': ('asia', 'asian'),
        'Indonésien': ('asia', 'asian'),
        'Indonésienne': ('asia', 'asian'),
        'Brunéien': ('asia', 'asian'),
        'Brunéienne': ('asia', 'asian'),
        'Timorais': ('asia', 'asian'),
        'Timoraise': ('asia', 'asian'),
        
        # ASIE - Indian (Asie du Sud)
        'Indien': ('asia', 'indian'),
        'Indienne': ('asia', 'indian'),
        'Pakistanais': ('asia', 'indian'),
        'Pakistanaise': ('asia', 'indian'),
        'Bangladais': ('asia', 'indian'),
        'Bangladaise': ('asia', 'indian'),
        'Sri-Lankais': ('asia', 'indian'),
        'Sri-Lankaise': ('asia', 'indian'),
        'Népalais': ('asia', 'indian'),
        'Népalaise': ('asia', 'indian'),
        'Bhoutanais': ('asia', 'indian'),
        'Bhoutanaise': ('asia', 'indian'),
        'Maldivien': ('asia', 'indian'),
        'Maldivienne': ('asia', 'indian'),
        'Afghan': ('asia', 'indian'),
        'Afghane': ('asia', 'indian'),
        
        # EUROPE - White
        'Français': ('europe', 'white'),
        'Française': ('europe', 'white'),
        'Allemand': ('europe', 'white'),
        'Allemande': ('europe', 'white'),
        'Italien': ('europe', 'white'),
        'Italienne': ('europe', 'white'),
        'Espagnol': ('europe', 'white'),
        'Espagnole': ('europe', 'white'),
        'Britannique': ('europe', 'white'),
        'Irlandais': ('europe', 'white'),
        'Irlandaise': ('europe', 'white'),
        'Portugais': ('europe', 'white'),
        'Portugaise': ('europe', 'white'),
        'Néerlandais': ('europe', 'white'),
        'Néerlandaise': ('europe', 'white'),
        'Belge': ('europe', 'white'),
        'Suisse': ('europe', 'white'),
        'Autrichien': ('europe', 'white'),
        'Autrichienne': ('europe', 'white'),
        'Polonais': ('europe', 'white'),
        'Polonaise': ('europe', 'white'),
        'Tchèque': ('europe', 'white'),
        'Slovaque': ('europe', 'white'),
        'Hongrois': ('europe', 'white'),
        'Hongroise': ('europe', 'white'),
        'Roumain': ('europe', 'white'),
        'Roumaine': ('europe', 'white'),
        'Bulgare': ('europe', 'white'),
        'Grec': ('europe', 'white'),
        'Grecque': ('europe', 'white'),
        'Danois': ('europe', 'white'),
        'Danoise': ('europe', 'white'),
        'Suédois': ('europe', 'white'),
        'Suédoise': ('europe', 'white'),
        'Norvégien': ('europe', 'white'),
        'Norvégienne': ('europe', 'white'),
        'Finlandais': ('europe', 'white'),
        'Finlandaise': ('europe', 'white'),
        'Islandais': ('europe', 'white'),
        'Islandaise': ('europe', 'white'),
        'Estonien': ('europe', 'white'),
        'Letton': ('europe', 'white'),
        'Lituanien': ('europe', 'white'),
        'Russe': ('europe', 'white'),
        'Ukrainien': ('europe', 'white'),
        'Ukrainienne': ('europe', 'white'),
        'Biélorusse': ('europe', 'white'),
        'Moldave': ('europe', 'white'),
        'Serbe': ('europe', 'white'),
        'Croate': ('europe', 'white'),
        'Bosniaque': ('europe', 'white'),
        'Monténégrin': ('europe', 'white'),
        'Macédonien': ('europe', 'white'),
        'Albanais': ('europe', 'white'),
        'Albanaise': ('europe', 'white'),
        'Kosovar': ('europe', 'white'),
        'Slovène': ('europe', 'white'),
        
        # AMÉRIQUE - Latino Hispanic
        'Mexicain': ('america', 'latino_hispanic'),
        'Mexicaine': ('america', 'latino_hispanic'),
        'Guatémaltèque': ('america', 'latino_hispanic'),
        'Hondurien': ('america', 'latino_hispanic'),
        'Salvadorien': ('america', 'latino_hispanic'),
        'Nicaraguayen': ('america', 'latino_hispanic'),
        'Costaricain': ('america', 'latino_hispanic'),
        'Panaméen': ('america', 'latino_hispanic'),
        'Cubain': ('america', 'latino_hispanic'),
        'Dominicain': ('america', 'latino_hispanic'),
        'Haïtien': ('america', 'latino_hispanic'),
        'Jamaïcain': ('america', 'latino_hispanic'),
        'Portoricain': ('america', 'latino_hispanic'),
        'Colombien': ('america', 'latino_hispanic'),
        'Vénézuélien': ('america', 'latino_hispanic'),
        'Équatorien': ('america', 'latino_hispanic'),
        'Péruvien': ('america', 'latino_hispanic'),
        'Bolivien': ('america', 'latino_hispanic'),
        'Chilien': ('america', 'latino_hispanic'),
        'Argentin': ('america', 'latino_hispanic'),
        'Argentine': ('america', 'latino_hispanic'),
        'Uruguayen': ('america', 'latino_hispanic'),
        'Paraguayen': ('america', 'latino_hispanic'),
        'Brésilien': ('america', 'latino_hispanic'),
        'Brésilienne': ('america', 'latino_hispanic'),
        
        # AMÉRIQUE - White (USA, Canada)
        'Américain': ('america', 'white'),
        'Américaine': ('america', 'white'),
        'Canadien': ('america', 'white'),
        'Canadienne': ('america', 'white'),
        
        # MOYEN-ORIENT - Middle Eastern
        'Saoudien': ('middle_east', 'middle_eastern'),
        'Émirati': ('middle_east', 'middle_eastern'),
        'Qatari': ('middle_east', 'middle_eastern'),
        'Koweïtien': ('middle_east', 'middle_eastern'),
        'Bahreïni': ('middle_east', 'middle_eastern'),
        'Omanais': ('middle_east', 'middle_eastern'),
        'Yéménite': ('middle_east', 'middle_eastern'),
        'Jordanien': ('middle_east', 'middle_eastern'),
        'Libanais': ('middle_east', 'middle_eastern'),
        'Libanaise': ('middle_east', 'middle_eastern'),
        'Syrien': ('middle_east', 'middle_eastern'),
        'Irakien': ('middle_east', 'middle_eastern'),
        'Iranien': ('middle_east', 'middle_eastern'),
        'Iranienne': ('middle_east', 'middle_eastern'),
        'Turc': ('middle_east', 'middle_eastern'),
        'Turque': ('middle_east', 'middle_eastern'),
        'Israélien': ('middle_east', 'middle_eastern'),
        'Israélienne': ('middle_east', 'middle_eastern'),
        'Palestinien': ('middle_east', 'middle_eastern'),
        'Arménien': ('middle_east', 'middle_eastern'),
        'Arménienne': ('middle_east', 'middle_eastern'),
        'Géorgien': ('middle_east', 'middle_eastern'),
        'Géorgienne': ('middle_east', 'middle_eastern'),
        'Azéri': ('middle_east', 'middle_eastern'),
        
        # OCÉANIE - White
        'Australien': ('oceania', 'white'),
        'Australienne': ('oceania', 'white'),
        'Néo-Zélandais': ('oceania', 'white'),
        'Néo-Zélandaise': ('oceania', 'white'),
        'Fidjien': ('oceania', 'white'),
        'Papou-Néo-Guinéen': ('oceania', 'white'),
        'Samoan': ('oceania', 'white'),
        'Tongien': ('oceania', 'white'),
        'Vanuatais': ('oceania', 'white'),
        'Salomonais': ('oceania', 'white'),
        'Micronésien': ('oceania', 'white'),
        'Palaosien': ('oceania', 'white'),
        'Marshallais': ('oceania', 'white'),
        'Nauruan': ('oceania', 'white'),
        'Kiribatien': ('oceania', 'white'),
        'Tuvaluan': ('oceania', 'white'),
    }
    
    def __init__(self):
        """Initialise le service"""
        self.portraits_dir = self.PORTRAITS_BASE_DIR
        self._portrait_cache = {}  # Cache pour éviter de rescanner les dossiers
        self._last_cache_update = None
        
    def get_continent_and_ethnicity(self, nationality: str) -> Tuple[str, str]:
        """
        Retourne le continent et l'ethnie correspondant à une nationalité
        
        Args:
            nationality: La nationalité du joueur (ex: 'Français', 'Chinoise', 'Nigérian')
            
        Returns:
            Tuple (continent, ethnicity) (ex: ('europe', 'white'))
        """
        # Recherche directe
        if nationality in self.NATIONALITY_TO_CONTINENT_ETHNICITY:
            return self.NATIONALITY_TO_CONTINENT_ETHNICITY[nationality]
        
        # Recherche insensible à la casse
        nationality_lower = nationality.lower()
        for nat, (continent, ethnicity) in self.NATIONALITY_TO_CONTINENT_ETHNICITY.items():
            if nat.lower() == nationality_lower:
                return (continent, ethnicity)
        
        # Fallback : Europe/White par défaut
        return ('europe', 'white')
    
    def get_available_portraits(
        self, 
        continent: str, 
        ethnicity: str, 
        gender: str,
        force_refresh: bool = False
    ) -> List[Path]:
        """
        Récupère la liste des portraits disponibles pour un continent/ethnie/genre
        
        Args:
            continent: Le continent (ex: 'africa', 'asia', 'europe')
            ethnicity: L'ethnie (ex: 'black', 'asian', 'white')
            gender: Le genre ('M' ou 'F')
            force_refresh: Force le rafraîchissement du cache
            
        Returns:
            Liste des chemins vers les portraits disponibles
        """
        cache_key = f"{continent}_{ethnicity}_{gender}"
        
        # Utiliser le cache si disponible et récent (< 5 minutes)
        if not force_refresh and cache_key in self._portrait_cache:
            if self._last_cache_update:
                elapsed = (datetime.now() - self._last_cache_update).total_seconds()
                if elapsed < 300:  # 5 minutes
                    return self._portrait_cache[cache_key]
        
        # Scanner le dossier
        portrait_dir = self.portraits_dir / continent / ethnicity / gender
        
        if not portrait_dir.exists():
            print(f"⚠️ Dossier non trouvé : {portrait_dir}")
            return []
        
        # Trouver tous les fichiers JPG
        portraits = list(portrait_dir.glob("*.jpg"))
        
        # Mettre en cache
        self._portrait_cache[cache_key] = portraits
        self._last_cache_update = datetime.now()
        
        return portraits
    
    def select_random_portrait(
        self, 
        nationality: str, 
        gender: str
    ) -> Optional[str]:
        """
        Sélectionne un portrait aléatoire selon la nationalité et le genre
        
        Args:
            nationality: La nationalité du joueur
            gender: Le genre ('M' ou 'F')
            
        Returns:
            Le chemin relatif vers le portrait (ex: '/static/realistic_portraits/africa/black/M/africa_black_M_21_35_0001.jpg')
            ou None si aucun portrait n'est disponible
        """
        # Obtenir le continent et l'ethnie
        continent, ethnicity = self.get_continent_and_ethnicity(nationality)
        
        # Obtenir les portraits disponibles
        portraits = self.get_available_portraits(continent, ethnicity, gender)
        
        if not portraits:
            print(f"⚠️ Aucun portrait disponible pour {nationality} ({gender})")
            return None
        
        # Sélectionner aléatoirement
        selected = random.choice(portraits)
        
        # Convertir en chemin relatif pour l'API
        relative_path = str(selected).replace('/app/backend/static', '/api/static')
        
        return relative_path
    
    def get_portrait_stats(self) -> Dict:
        """
        Retourne des statistiques sur les portraits disponibles
        
        Returns:
            Dict avec les stats par continent/ethnie/genre
        """
        stats = {}
        
        if not self.portraits_dir.exists():
            return {"error": "Dossier des portraits non trouvé", "total": 0}
        
        total = 0
        for continent_dir in self.portraits_dir.iterdir():
            if not continent_dir.is_dir():
                continue
            
            continent = continent_dir.name
            stats[continent] = {}
            
            for ethnicity_dir in continent_dir.iterdir():
                if not ethnicity_dir.is_dir():
                    continue
                
                ethnicity = ethnicity_dir.name
                stats[continent][ethnicity] = {}
                
                for gender_dir in ethnicity_dir.iterdir():
                    if not gender_dir.is_dir():
                        continue
                    
                    gender = gender_dir.name
                    count = len(list(gender_dir.glob("*.jpg")))
                    stats[continent][ethnicity][gender] = count
                    total += count
        
        stats["total"] = total
        return stats
    
    def is_ready(self) -> bool:
        """
        Vérifie si le système de portraits réalistes est prêt
        
        Returns:
            True si des portraits sont disponibles, False sinon
        """
        return self.portraits_dir.exists() and len(list(self.portraits_dir.glob("**/*.jpg"))) > 0
