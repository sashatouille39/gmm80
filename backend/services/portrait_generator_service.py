"""
Service de génération de portraits par calques PNG cohérents avec la nationalité
Utilise l'IA (gpt-image-1) pour générer des calques semi-réalistes
"""
import os
import asyncio
import base64
import random
from typing import Dict, List, Tuple
from dotenv import load_dotenv
from emergentintegrations.llm.openai.image_generation import OpenAIImageGeneration

load_dotenv()

class PortraitGeneratorService:
    """Service pour générer des calques de portraits cohérents avec la nationalité"""
    
    # Définition des palettes de couleurs par région/continent
    SKIN_COLOR_PALETTES = {
        # Europe du Nord (nordique)
        'nordic': {
            'description': 'Nordic/Scandinavian',
            'skin_tones': ['very pale', 'pale', 'light'],
            'continents': ['Européen du Nord']
        },
        # Europe de l'Ouest
        'western_european': {
            'description': 'Western European',
            'skin_tones': ['pale', 'light', 'fair'],
            'continents': ['Européen de l\'Ouest']
        },
        # Europe du Sud (méditerranéen)
        'mediterranean': {
            'description': 'Mediterranean/Southern European',
            'skin_tones': ['olive', 'tan', 'light brown'],
            'continents': ['Européen du Sud', 'Méditerranéen']
        },
        # Europe de l'Est
        'eastern_european': {
            'description': 'Eastern European',
            'skin_tones': ['fair', 'light', 'pale'],
            'continents': ['Européen de l\'Est']
        },
        # Asie de l'Est
        'east_asian': {
            'description': 'East Asian',
            'skin_tones': ['light', 'fair', 'pale yellow'],
            'continents': ['Asiatique de l\'Est']
        },
        # Asie du Sud
        'south_asian': {
            'description': 'South Asian',
            'skin_tones': ['tan', 'brown', 'medium brown'],
            'continents': ['Asiatique du Sud']
        },
        # Asie du Sud-Est
        'southeast_asian': {
            'description': 'Southeast Asian',
            'skin_tones': ['tan', 'light brown', 'olive'],
            'continents': ['Asiatique du Sud-Est']
        },
        # Moyen-Orient
        'middle_eastern': {
            'description': 'Middle Eastern',
            'skin_tones': ['olive', 'tan', 'medium brown'],
            'continents': ['Moyen-Oriental']
        },
        # Afrique du Nord
        'north_african': {
            'description': 'North African',
            'skin_tones': ['tan', 'olive', 'medium brown'],
            'continents': ['Nord-Africain']
        },
        # Afrique sub-saharienne
        'african': {
            'description': 'Sub-Saharan African',
            'skin_tones': ['dark brown', 'very dark brown', 'deep brown'],
            'continents': ['Africain']
        },
        # Amérique Latine
        'latino': {
            'description': 'Latino/Hispanic',
            'skin_tones': ['tan', 'olive', 'light brown', 'medium brown'],
            'continents': ['Latino', 'Hispanique']
        },
        # Mixte (Amérique du Nord, Australie, etc.)
        'mixed': {
            'description': 'Mixed/Diverse',
            'skin_tones': ['fair', 'light', 'tan', 'olive', 'brown'],
            'continents': ['Américain', 'Canadien', 'Australien', 'Brésilien']
        }
    }
    
    # Mapping nationalités -> régions
    NATIONALITY_TO_REGION = {
        # Europe du Nord
        'Danois': 'nordic',
        'Finlandais': 'nordic',
        'Islandais': 'nordic',
        'Norvégien': 'nordic',
        'Suédois': 'nordic',
        
        # Europe de l'Ouest
        'Allemand': 'western_european',
        'Autrichien': 'western_european',
        'Belge': 'western_european',
        'Britannique': 'western_european',
        'Français': 'western_european',
        'Irlandais': 'western_european',
        'Néerlandais': 'western_european',
        'Suisse': 'western_european',
        
        # Europe du Sud
        'Espagnol': 'mediterranean',
        'Grec': 'mediterranean',
        'Italien': 'mediterranean',
        'Portugais': 'mediterranean',
        
        # Europe de l'Est
        'Bulgare': 'eastern_european',
        'Croate': 'eastern_european',
        'Estonien': 'eastern_european',
        'Hongrois': 'eastern_european',
        'Polonais': 'eastern_european',
        'Roumain': 'eastern_european',
        'Russe': 'eastern_european',
        'Tchèque': 'eastern_european',
        
        # Asie de l'Est
        'Chinois': 'east_asian',
        'Coréen': 'east_asian',
        'Japonais': 'east_asian',
        
        # Asie du Sud
        'Indien': 'south_asian',
        
        # Asie du Sud-Est
        'Indonésien': 'southeast_asian',
        'Thaïlandais': 'southeast_asian',
        
        # Moyen-Orient
        'Afghan': 'middle_eastern',
        'Iranien': 'middle_eastern',
        'Turc': 'middle_eastern',
        
        # Afrique du Nord
        'Égyptien': 'north_african',
        'Marocain': 'north_african',
        
        # Afrique sub-saharienne
        'Nigérian': 'african',
        
        # Amérique Latine
        'Argentin': 'latino',
        'Mexicain': 'latino',
        
        # Mixte
        'Américain': 'mixed',
        'Australien': 'mixed',
        'Brésilien': 'mixed',
        'Canadien': 'mixed',
    }
    
    # Caractéristiques par région
    REGION_FEATURES = {
        'nordic': {
            'hair_colors': ['blonde', 'light blonde', 'golden blonde', 'light brown'],
            'eye_colors': ['blue', 'light blue', 'grey-blue', 'green'],
            'hair_types': ['straight', 'wavy']
        },
        'western_european': {
            'hair_colors': ['brown', 'light brown', 'blonde', 'dark blonde', 'chestnut'],
            'eye_colors': ['blue', 'green', 'hazel', 'light brown'],
            'hair_types': ['straight', 'wavy']
        },
        'mediterranean': {
            'hair_colors': ['dark brown', 'black', 'brown'],
            'eye_colors': ['dark brown', 'hazel', 'brown', 'green'],
            'hair_types': ['wavy', 'curly']
        },
        'eastern_european': {
            'hair_colors': ['blonde', 'light brown', 'brown', 'dark brown'],
            'eye_colors': ['blue', 'green', 'grey', 'hazel'],
            'hair_types': ['straight', 'wavy']
        },
        'east_asian': {
            'hair_colors': ['black', 'dark brown'],
            'eye_colors': ['dark brown', 'black'],
            'hair_types': ['straight']
        },
        'south_asian': {
            'hair_colors': ['black', 'dark brown'],
            'eye_colors': ['dark brown', 'black'],
            'hair_types': ['straight', 'wavy', 'curly']
        },
        'southeast_asian': {
            'hair_colors': ['black', 'dark brown'],
            'eye_colors': ['dark brown', 'brown'],
            'hair_types': ['straight', 'wavy']
        },
        'middle_eastern': {
            'hair_colors': ['black', 'dark brown', 'brown'],
            'eye_colors': ['dark brown', 'brown', 'hazel'],
            'hair_types': ['wavy', 'curly']
        },
        'north_african': {
            'hair_colors': ['black', 'dark brown'],
            'eye_colors': ['dark brown', 'brown'],
            'hair_types': ['wavy', 'curly']
        },
        'african': {
            'hair_colors': ['black'],
            'eye_colors': ['dark brown', 'black'],
            'hair_types': ['curly', 'kinky', 'afro-textured']
        },
        'latino': {
            'hair_colors': ['black', 'dark brown', 'brown'],
            'eye_colors': ['dark brown', 'brown', 'hazel'],
            'hair_types': ['straight', 'wavy', 'curly']
        },
        'mixed': {
            'hair_colors': ['blonde', 'brown', 'black', 'red', 'light brown'],
            'eye_colors': ['blue', 'green', 'brown', 'hazel', 'grey'],
            'hair_types': ['straight', 'wavy', 'curly']
        }
    }
    
    def __init__(self):
        """Initialise le service avec la clé API"""
        api_key = os.getenv('EMERGENT_LLM_KEY', 'sk-emergent-default')
        self.image_gen = OpenAIImageGeneration(api_key=api_key)
        self.base_path = "/app/backend/static/portraits"
        
    def get_region_for_nationality(self, nationality: str) -> str:
        """Retourne la région correspondant à une nationalité"""
        return self.NATIONALITY_TO_REGION.get(nationality, 'mixed')
    
    def get_skin_tone_for_region(self, region: str) -> str:
        """Retourne une tonalité de peau aléatoire pour une région"""
        palette = self.SKIN_COLOR_PALETTES.get(region, self.SKIN_COLOR_PALETTES['mixed'])
        return random.choice(palette['skin_tones'])
    
    def get_hair_color_for_region(self, region: str) -> str:
        """Retourne une couleur de cheveux cohérente avec la région"""
        features = self.REGION_FEATURES.get(region, self.REGION_FEATURES['mixed'])
        return random.choice(features['hair_colors'])
    
    def get_eye_color_for_region(self, region: str) -> str:
        """Retourne une couleur d'yeux cohérente avec la région"""
        features = self.REGION_FEATURES.get(region, self.REGION_FEATURES['mixed'])
        return random.choice(features['eye_colors'])
    
    def get_hair_type_for_region(self, region: str) -> str:
        """Retourne un type de cheveux cohérent avec la région"""
        features = self.REGION_FEATURES.get(region, self.REGION_FEATURES['mixed'])
        return random.choice(features['hair_types'])
    
    async def generate_base_layer(self, region: str, gender: str, age_range: str, variation_id: int) -> bytes:
        """Génère un calque de base (tête) cohérent avec la région"""
        skin_tone = self.get_skin_tone_for_region(region)
        
        prompt = f"""Create a semi-realistic {gender} human head base layer for a character portrait.
Style: Semi-realistic, clean, professional illustration.
Skin tone: {skin_tone}.
Age range: {age_range}.
View: Front-facing, neutral expression.
Details: Just the head and neck shape, no facial features (no eyes, no mouth, no nose, no hair).
Background: Completely transparent (PNG with alpha channel).
Format: Clean silhouette of a head, {skin_tone} colored.
Resolution: High quality, suitable for layering.
Variation #{variation_id} to ensure uniqueness."""
        
        images = await self.image_gen.generate_images(
            prompt=prompt,
            model="gpt-image-1",
            number_of_images=1
        )
        
        return images[0] if images else None
    
    async def generate_eyes_layer(self, region: str, gender: str, age_range: str, variation_id: int) -> bytes:
        """Génère un calque d'yeux cohérent avec la région"""
        eye_color = self.get_eye_color_for_region(region)
        region_desc = self.SKIN_COLOR_PALETTES[region]['description']
        
        prompt = f"""Create semi-realistic eyes for a {region_desc} {gender} character.
Style: Semi-realistic, detailed, expressive.
Eye color: {eye_color}.
Age range: {age_range}.
Ethnicity: {region_desc} features.
Details: Just the eyes (both eyes, symmetric), with appropriate eye shape for {region_desc} ethnicity.
Background: Completely transparent (PNG with alpha channel).
Format: Eyes only, no other facial features, positioned correctly for front-facing head.
Resolution: High quality, suitable for layering.
Variation #{variation_id} to ensure uniqueness."""
        
        images = await self.image_gen.generate_images(
            prompt=prompt,
            model="gpt-image-1",
            number_of_images=1
        )
        
        return images[0] if images else None
    
    async def generate_hair_layer(self, region: str, gender: str, age_range: str, variation_id: int) -> bytes:
        """Génère un calque de cheveux cohérent avec la région"""
        hair_color = self.get_hair_color_for_region(region)
        hair_type = self.get_hair_type_for_region(region)
        
        # Style de coiffure selon le genre
        if gender == 'male':
            hairstyles = ['short', 'medium length', 'crew cut', 'undercut', 'slicked back']
        else:
            hairstyles = ['long', 'medium', 'bob', 'wavy', 'ponytail', 'layered']
        
        hairstyle = random.choice(hairstyles)
        
        prompt = f"""Create semi-realistic {hair_color} {hair_type} hair for a {gender} character.
Style: Semi-realistic, detailed, natural looking.
Hair color: {hair_color}.
Hair type: {hair_type}.
Hairstyle: {hairstyle}.
Age range: {age_range}.
Details: Just the hair, {hairstyle} style, covering appropriate areas of the head.
Background: Completely transparent (PNG with alpha channel).
Format: Hair only, no face, no other features, positioned for front-facing head.
Resolution: High quality, suitable for layering.
Variation #{variation_id} to ensure uniqueness."""
        
        images = await self.image_gen.generate_images(
            prompt=prompt,
            model="gpt-image-1",
            number_of_images=1
        )
        
        return images[0] if images else None
    
    async def generate_mouth_layer(self, region: str, gender: str, age_range: str, variation_id: int) -> bytes:
        """Génère un calque de bouche cohérent avec la région"""
        region_desc = self.SKIN_COLOR_PALETTES[region]['description']
        
        prompt = f"""Create a semi-realistic mouth for a {region_desc} {gender} character.
Style: Semi-realistic, neutral expression.
Ethnicity: {region_desc} features.
Age range: {age_range}.
Details: Just the mouth and lips, appropriate shape for {region_desc} ethnicity, neutral/slight smile.
Background: Completely transparent (PNG with alpha channel).
Format: Mouth only, no other facial features, positioned correctly for front-facing head.
Resolution: High quality, suitable for layering.
Variation #{variation_id} to ensure uniqueness."""
        
        images = await self.image_gen.generate_images(
            prompt=prompt,
            model="gpt-image-1",
            number_of_images=1
        )
        
        return images[0] if images else None
    
    async def generate_nose_layer(self, region: str, gender: str, age_range: str, variation_id: int) -> bytes:
        """Génère un calque de nez cohérent avec la région"""
        region_desc = self.SKIN_COLOR_PALETTES[region]['description']
        
        prompt = f"""Create a semi-realistic nose for a {region_desc} {gender} character.
Style: Semi-realistic, front view.
Ethnicity: {region_desc} features (appropriate nose shape for this ethnicity).
Age range: {age_range}.
Details: Just the nose, appropriate shape and size for {region_desc} ethnicity.
Background: Completely transparent (PNG with alpha channel).
Format: Nose only, no other facial features, positioned correctly for front-facing head.
Resolution: High quality, suitable for layering.
Variation #{variation_id} to ensure uniqueness."""
        
        images = await self.image_gen.generate_images(
            prompt=prompt,
            model="gpt-image-1",
            number_of_images=1
        )
        
        return images[0] if images else None
    
    async def generate_portrait_layers_set(
        self,
        nationality: str,
        gender: str,
        age: int = 25,
        set_id: int = 1,
        layer_types: List[str] = None
    ) -> Dict[str, str]:
        """
        Génère un set complet ou partiel de calques pour un portrait
        
        Args:
            nationality: Nationalité du personnage
            gender: Sexe ('male' ou 'female')
            age: Âge du personnage
            set_id: ID de variation pour générer différentes versions
            layer_types: Liste des types de calques à générer ['base', 'eyes', 'hair', 'mouth', 'nose']
                        Si None, génère tous les calques
        
        Retourne les chemins des fichiers générés
        """
        region = self.get_region_for_nationality(nationality)
        
        # Si aucun type spécifié, générer tous les calques
        if layer_types is None:
            layer_types = ['base', 'eyes', 'hair', 'mouth', 'nose']
        
        # Déterminer la tranche d'âge
        if age < 20:
            age_range = "young adult (18-25)"
        elif age < 35:
            age_range = "adult (25-35)"
        elif age < 50:
            age_range = "middle-aged (35-50)"
        else:
            age_range = "mature (50+)"
        
        # Créer les identifiants uniques
        gender_code = 'M' if gender == 'male' else 'F'
        base_filename = f"{region}_{gender_code}_age{age}_{set_id}"
        
        # Générer les calques demandés
        layers = {}
        
        try:
            # Base (tête)
            if 'base' in layer_types:
                base_bytes = await self.generate_base_layer(region, gender, age_range, set_id)
                if base_bytes:
                    os.makedirs(f"{self.base_path}/base", exist_ok=True)
                    base_path = f"{self.base_path}/base/{base_filename}_base.png"
                    with open(base_path, 'wb') as f:
                        f.write(base_bytes)
                    layers['base'] = f"/static/portraits/base/{base_filename}_base.png"
            
            # Yeux
            if 'eyes' in layer_types:
                eyes_bytes = await self.generate_eyes_layer(region, gender, age_range, set_id)
                if eyes_bytes:
                    os.makedirs(f"{self.base_path}/eyes", exist_ok=True)
                    eyes_path = f"{self.base_path}/eyes/{base_filename}_eyes.png"
                    with open(eyes_path, 'wb') as f:
                        f.write(eyes_bytes)
                    layers['eyes'] = f"/static/portraits/eyes/{base_filename}_eyes.png"
            
            # Cheveux
            if 'hair' in layer_types:
                hair_bytes = await self.generate_hair_layer(region, gender, age_range, set_id)
                if hair_bytes:
                    os.makedirs(f"{self.base_path}/hair", exist_ok=True)
                    hair_path = f"{self.base_path}/hair/{base_filename}_hair.png"
                    with open(hair_path, 'wb') as f:
                        f.write(hair_bytes)
                    layers['hair'] = f"/static/portraits/hair/{base_filename}_hair.png"
            
            # Bouche
            if 'mouth' in layer_types:
                mouth_bytes = await self.generate_mouth_layer(region, gender, age_range, set_id)
                if mouth_bytes:
                    os.makedirs(f"{self.base_path}/mouth", exist_ok=True)
                    mouth_path = f"{self.base_path}/mouth/{base_filename}_mouth.png"
                    with open(mouth_path, 'wb') as f:
                        f.write(mouth_bytes)
                    layers['mouth'] = f"/static/portraits/mouth/{base_filename}_mouth.png"
            
            # Nez
            if 'nose' in layer_types:
                nose_bytes = await self.generate_nose_layer(region, gender, age_range, set_id)
                if nose_bytes:
                    os.makedirs(f"{self.base_path}/nose", exist_ok=True)
                    nose_path = f"{self.base_path}/nose/{base_filename}_nose.png"
                    with open(nose_path, 'wb') as f:
                        f.write(nose_bytes)
                    layers['nose'] = f"/static/portraits/nose/{base_filename}_nose.png"
            
        except Exception as e:
            print(f"❌ Erreur lors de la génération: {str(e)}")
            raise
        
        return layers
    
    def get_available_portraits_for_region(self, region: str, gender: str) -> List[Dict[str, str]]:
        """Retourne la liste des portraits disponibles pour une région et un genre"""
        gender_code = 'M' if gender == 'male' else 'F'
        pattern = f"{region}_{gender_code}_"
        
        available = []
        
        # Parcourir les fichiers base pour trouver les sets disponibles
        base_dir = f"{self.base_path}/base"
        if os.path.exists(base_dir):
            for filename in os.listdir(base_dir):
                if filename.startswith(pattern) and filename.endswith('_base.png'):
                    # Extraire l'identifiant du set
                    base_name = filename.replace('_base.png', '')
                    
                    # Vérifier que tous les calques existent
                    portrait_set = {
                        'base': f"/static/portraits/base/{base_name}_base.png",
                        'eyes': f"/static/portraits/eyes/{base_name}_eyes.png",
                        'hair': f"/static/portraits/hair/{base_name}_hair.png",
                        'mouth': f"/static/portraits/mouth/{base_name}_mouth.png",
                        'nose': f"/static/portraits/nose/{base_name}_nose.png",
                    }
                    
                    # Vérifier que tous les fichiers existent
                    all_exist = all([
                        os.path.exists(f"{self.base_path}{path}")
                        for path in portrait_set.values()
                    ])
                    
                    if all_exist:
                        available.append(portrait_set)
        
        return available
    
    def assemble_random_layers(
        self,
        region: str,
        gender: str
    ) -> Dict[str, str]:
        """
        Assemble aléatoirement des calques individuels de la bibliothèque
        pour créer un portrait unique
        
        Retourne un dict avec les chemins des calques assemblés :
        {'base': '/path/to/base.png', 'eyes': '/path/to/eyes.png', ...}
        """
        assembled = {}
        layer_types = ['base', 'eyes', 'hair', 'mouth', 'nose']
        
        gender_code = 'M' if gender == 'male' else 'F'
        
        # Pour chaque type de calque, sélectionner un fichier aléatoire
        for layer_type in layer_types:
            layer_dir = f"{self.base_path}/{layer_type}"
            
            if not os.path.exists(layer_dir):
                continue
            
            # Trouver tous les fichiers de ce type pour cette région/sexe
            pattern_prefix = f"{region}_{gender_code}_"
            matching_files = [
                f for f in os.listdir(layer_dir)
                if f.startswith(pattern_prefix) and f.endswith(f'_{layer_type}.png')
            ]
            
            if matching_files:
                # Choisir un fichier aléatoire
                chosen_file = random.choice(matching_files)
                assembled[layer_type] = f"/static/portraits/{layer_type}/{chosen_file}"
        
        return assembled
    
    def select_random_portrait_layers(
        self,
        nationality: str,
        gender: str
    ) -> Dict[str, str]:
        """
        Assemble aléatoirement des calques individuels pour créer un portrait unique
        Utilise la bibliothèque de calques pré-générés par région/sexe
        """
        region = self.get_region_for_nationality(nationality)
        gender_param = 'male' if gender == 'M' else 'female'
        
        # Essayer d'assembler des calques de la bibliothèque
        assembled_layers = self.assemble_random_layers(region, gender_param)
        
        if assembled_layers and len(assembled_layers) > 0:
            return assembled_layers
        else:
            # Fallback : chercher des sets complets
            available = self.get_available_portraits_for_region(region, gender_param)
            
            if available:
                return random.choice(available)
            else:
                # Générer un portrait simple à la volée
                from services.simple_portrait_generator import simple_portrait_gen
                from services.game_service import GameService
                
                # Obtenir des couleurs cohérentes avec la région
                skin_color = self.get_skin_tone_for_region(region)
                hair_color_name = self.get_hair_color_for_region(region)
                eye_color_name = self.get_eye_color_for_region(region)
                
                # Convertir les noms de couleurs en hex (utiliser les palettes du GameService)
                skin_color_hex = GameService.SKIN_COLORS[random.randint(0, len(GameService.SKIN_COLORS) - 1)]
            hair_color_hex = GameService.HAIR_COLORS[random.randint(0, len(GameService.HAIR_COLORS) - 1)]
            
            # Couleurs d'yeux en hex
            eye_colors_hex = {
                'blue': '#4169E1',
                'light blue': '#87CEEB',
                'grey-blue': '#6495ED',
                'green': '#228B22',
                'brown': '#8B4513',
                'dark brown': '#654321',
                'hazel': '#8E7618',
                'light brown': '#A0522D',
                'black': '#000000',
                'grey': '#808080'
            }
            eye_color_hex = eye_colors_hex.get(eye_color_name, '#8B4513')
            
            # Générer le portrait simple
            set_id = random.randint(1, 9999)
            layers = simple_portrait_gen.generate_complete_portrait(
                nationality=nationality,
                region=region,
                gender=gender,
                skin_color=skin_color_hex,
                hair_color=hair_color_hex,
                eye_color=eye_color_hex,
                eye_shape='Amande',
                set_id=set_id
            )
            
            return layers


# Instance globale du service
portrait_service = PortraitGeneratorService()
