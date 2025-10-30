#!/usr/bin/env python3
"""
Script pour analyser automatiquement les portraits et détecter les enfants
Utilise l'API OpenAI Vision pour analyser l'âge apparent
"""
import os
import base64
from pathlib import Path
import json
from datetime import datetime
import time

# Import de l'intégration Emergent
try:
    from emergentintegrations import UniversalKeyManager
    key_manager = UniversalKeyManager()
    EMERGENT_KEY = key_manager.get_api_key()
except:
    EMERGENT_KEY = os.getenv('EMERGENT_LLM_KEY')

import anthropic

# Configuration
PORTRAITS_DIR = Path("/app/backend/static/realistic_portraits")
RESULTS_FILE = Path("/app/portraits_age_analysis.json")
CHILDREN_LIST_FILE = Path("/app/portraits_children_list.txt")

def encode_image(image_path):
    """Encode l'image en base64"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def analyze_portrait_age(image_path):
    """Analyse un portrait pour déterminer l'âge apparent"""
    
    try:
        # Lire l'image
        with open(image_path, "rb") as f:
            image_data = base64.standard_b64encode(f.read()).decode("utf-8")
        
        # Utiliser Claude via Anthropic
        client = anthropic.Anthropic(api_key=EMERGENT_KEY)
        
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=200,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/jpeg",
                                "data": image_data,
                            },
                        },
                        {
                            "type": "text",
                            "text": """Analyze this portrait and determine the apparent age of the person.
Respond with ONLY ONE of these categories:
- CHILD (0-12 years old)
- TEEN (13-17 years old)  
- YOUNG_ADULT (18-25 years old)
- ADULT (26-45 years old)
- MATURE (46+ years old)

Respond with just the category name, nothing else."""
                        }
                    ],
                }
            ],
        )
        
        # Extraire la réponse
        age_category = message.content[0].text.strip()
        
        return age_category
        
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse de {image_path.name}: {e}")
        return "ERROR"

def analyze_all_portraits(sample_size=None, start_from=0):
    """Analyse tous les portraits (ou un échantillon)"""
    
    print("=" * 70)
    print("🔍 ANALYSE AUTOMATIQUE DES PORTRAITS")
    print("=" * 70)
    
    # Récupérer tous les portraits
    all_portraits = sorted(list(PORTRAITS_DIR.glob("**/*.jpg")))
    total = len(all_portraits)
    
    print(f"📊 Total de portraits à analyser: {total}")
    
    if sample_size:
        all_portraits = all_portraits[start_from:start_from + sample_size]
        print(f"📝 Analyse d'un échantillon: {len(all_portraits)} portraits")
        print(f"   (de {start_from} à {start_from + len(all_portraits)})")
    
    # Charger les résultats existants si disponibles
    results = {}
    if RESULTS_FILE.exists():
        with open(RESULTS_FILE, 'r') as f:
            results = json.load(f)
        print(f"📂 {len(results)} analyses précédentes chargées")
    
    # Analyser chaque portrait
    children = []
    teens = []
    young_adults = []
    adults = []
    mature = []
    errors = []
    
    for i, portrait in enumerate(all_portraits):
        relative_path = str(portrait.relative_to(PORTRAITS_DIR))
        
        # Vérifier si déjà analysé
        if relative_path in results:
            category = results[relative_path]
            print(f"[{i+1}/{len(all_portraits)}] ⏭️  Déjà analysé: {portrait.name} → {category}")
        else:
            print(f"[{i+1}/{len(all_portraits)}] 🔍 Analyse: {portrait.name}...", end=" ")
            category = analyze_portrait_age(portrait)
            print(f"→ {category}")
            
            results[relative_path] = category
            
            # Sauvegarder après chaque analyse
            with open(RESULTS_FILE, 'w') as f:
                json.dump(results, f, indent=2)
            
            # Pause pour éviter les rate limits
            time.sleep(0.5)
        
        # Catégoriser
        if category == "CHILD":
            children.append(relative_path)
        elif category == "TEEN":
            teens.append(relative_path)
        elif category == "YOUNG_ADULT":
            young_adults.append(relative_path)
        elif category == "ADULT":
            adults.append(relative_path)
        elif category == "MATURE":
            mature.append(relative_path)
        else:
            errors.append(relative_path)
    
    # Sauvegarder la liste des enfants et ados
    problematic = children + teens
    if problematic:
        with open(CHILDREN_LIST_FILE, 'w') as f:
            for p in problematic:
                f.write(f"{p}\n")
    
    # Afficher les résultats
    print("\n" + "=" * 70)
    print("📊 RÉSULTATS DE L'ANALYSE")
    print("=" * 70)
    print(f"👶 ENFANTS (0-12 ans):     {len(children):4d} portraits")
    print(f"🧒 ADOS (13-17 ans):       {len(teens):4d} portraits")
    print(f"👦 JEUNES ADULTES (18-25): {len(young_adults):4d} portraits")
    print(f"👨 ADULTES (26-45 ans):    {len(adults):4d} portraits")
    print(f"👴 MATURES (46+ ans):      {len(mature):4d} portraits")
    if errors:
        print(f"❌ ERREURS:                {len(errors):4d} portraits")
    
    print(f"\n⚠️  PORTRAITS À SUPPRIMER: {len(problematic)} (enfants + ados)")
    
    if problematic:
        print(f"\n📝 Liste sauvegardée dans: {CHILDREN_LIST_FILE}")
        print("\nExemples de portraits problématiques:")
        for p in problematic[:10]:
            print(f"  • {p}")
        if len(problematic) > 10:
            print(f"  ... et {len(problematic) - 10} autres")
    
    return results, problematic

if __name__ == "__main__":
    import sys
    
    # Vérifier si on fait un échantillon ou tout
    if len(sys.argv) > 1:
        if sys.argv[1] == "sample":
            # Analyser un échantillon de 50 portraits
            sample_size = int(sys.argv[2]) if len(sys.argv) > 2 else 50
            start = int(sys.argv[3]) if len(sys.argv) > 3 else 0
            results, problematic = analyze_all_portraits(sample_size=sample_size, start_from=start)
        elif sys.argv[1] == "all":
            # Analyser tous les portraits
            results, problematic = analyze_all_portraits()
    else:
        # Par défaut, analyser un échantillon
        print("💡 Usage:")
        print("  python3 analyze_portraits_age.py sample 50 0  # Analyser 50 portraits à partir du portrait 0")
        print("  python3 analyze_portraits_age.py all          # Analyser TOUS les portraits (prend du temps!)")
        print("\nPar défaut, analyse de 50 portraits...")
        results, problematic = analyze_all_portraits(sample_size=50)
    
    print("\n✅ Analyse terminée!")
