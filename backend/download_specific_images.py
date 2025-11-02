#!/usr/bin/env python3
"""
Script pour télécharger les images spécifiées depuis thispersonnotexist.org
"""

import requests
from pathlib import Path
import time

TARGET_DIR = Path("/app/backend/static/realistic_portraits/asia/asian/F")

URLS = [
    "https://thispersonnotexist.org/downloadimage/Ac3RhdGljL3dvbWFuL3NlZWQ1Mjk4Mi5qcGVn",
    "https://thispersonnotexist.org/downloadimage/Ac3RhdGljL3dvbWFuL3NlZWQ1NDMzMC5qcGVn",
    "https://thispersonnotexist.org/downloadimage/Ac3RhdGljL3dvbWFuL3NlZWQyMDg2Mi5qcGVn",
    "https://thispersonnotexist.org/downloadimage/Ac3RhdGljL3dvbWFuL3NlZWQ3MDI4LmpwZWc=",
    "https://thispersonnotexist.org/downloadimage/Ac3RhdGljL3dvbWFuL3NlZWQ0ODQ4MC5qcGVn",
    "https://thispersonnotexist.org/downloadimage/Ac3RhdGljL3dvbWFuL3NlZWQzMTE2OC5qcGVn",
    "https://thispersonnotexist.org/downloadimage/Ac3RhdGljL3dvbWFuL3NlZWQ0NTQzMy5qcGVn",
    "https://thispersonnotexist.org/downloadimage/Ac3RhdGljL3dvbWFuL3NlZWQ0NTQ4OC5qcGVn",
    "https://thispersonnotexist.org/downloadimage/Ac3RhdGljL3dvbWFuL3NlZWQ0NTE2OC5qcGVn",
    "https://thispersonnotexist.org/downloadimage/Ac3RhdGljL3dvbWFuL3NlZWQxNjExMi5qcGVn",
    "https://thispersonnotexist.org/downloadimage/Ac3RhdGljL3dvbWFuL3NlZWQzNzM3My5qcGVn",
    "https://thispersonnotexist.org/downloadimage/Ac3RhdGljL3dvbWFuL3NlZWQxNDY0Ni5qcGVn",
    "https://thispersonnotexist.org/downloadimage/Ac3RhdGljL3dvbWFuL3NlZWQ0OTQ2OS5qcGVn",
    "https://thispersonnotexist.org/downloadimage/Ac3RhdGljL3dvbWFuL3NlZWQ1NjY0LmpwZWc=",
    "https://thispersonnotexist.org/downloadimage/Ac3RhdGljL3dvbWFuL3NlZWQxMTM3Ni5qcGVn",
]

def download_images():
    """Télécharge toutes les images"""
    print("📥 TÉLÉCHARGEMENT DES IMAGES")
    print("="*60)
    print(f"📁 Dossier cible: {TARGET_DIR}")
    print(f"🖼️  Nombre d'images: {len(URLS)}")
    print("="*60 + "\n")
    
    # Créer le dossier si nécessaire
    TARGET_DIR.mkdir(parents=True, exist_ok=True)
    
    # Obtenir le prochain numéro de fichier
    existing_files = list(TARGET_DIR.glob("asia_asian_F_*.jpg"))
    next_num = len(existing_files) + 1
    
    downloaded = 0
    errors = 0
    
    for i, url in enumerate(URLS, 1):
        try:
            print(f"[{i}/{len(URLS)}] Téléchargement...")
            
            # Télécharger l'image
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            # Générer le nom de fichier
            filename = f"asia_asian_F_21_35_{next_num:04d}.jpg"
            filepath = TARGET_DIR / filename
            
            # Sauvegarder
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            size_kb = len(response.content) // 1024
            print(f"   ✅ {filename} ({size_kb} KB)")
            
            downloaded += 1
            next_num += 1
            
            # Petite pause pour ne pas surcharger le serveur
            time.sleep(0.5)
            
        except Exception as e:
            print(f"   ❌ Erreur: {str(e)[:80]}")
            errors += 1
    
    # Résumé
    print("\n" + "="*60)
    print("📊 RÉSUMÉ")
    print("="*60)
    print(f"✅ Images téléchargées: {downloaded}/{len(URLS)}")
    print(f"❌ Erreurs: {errors}")
    
    # Vérifier le total dans le dossier
    total_files = len(list(TARGET_DIR.glob("*.jpg")))
    print(f"📂 Total d'images dans le dossier: {total_files}")
    print("="*60)
    
    return downloaded


if __name__ == "__main__":
    downloaded = download_images()
    exit(0 if downloaded > 0 else 1)
