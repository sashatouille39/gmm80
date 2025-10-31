#!/usr/bin/env python3
"""
Script manuel simplifié pour télécharger des portraits depuis Perchance.
Instructions d'utilisation :
1. Allez sur https://perchance.org/ai-face-generator
2. Entrez le prompt et générez 9 images
3. Cliquez droit sur chaque image -> Copier l'adresse de l'image
4. Collez les URLs dans ce script et exécutez-le
"""

import requests
import os
from pathlib import Path

# Configuration
OUTPUT_DIR = "/app/backend/static/realistic_portraits/asia/asian/M"
Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

# Trouver le prochain numéro disponible
def get_next_number(age_range):
    existing_files = list(Path(OUTPUT_DIR).glob(f"asia_asian_M_{age_range}_*.jpg"))
    if existing_files:
        existing_numbers = [int(f.stem.split('_')[-1]) for f in existing_files]
        return max(existing_numbers) + 1
    return 1

# Fonction pour télécharger une image depuis une URL
def download_image(url, filename):
    try:
        print(f"📥 Téléchargement : {filename}...")
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            filepath = os.path.join(OUTPUT_DIR, filename)
            with open(filepath, 'wb') as f:
                f.write(response.content)
            print(f"  ✅ Sauvegardé : {filepath}")
            return True
        else:
            print(f"  ❌ Erreur HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"  ❌ Erreur : {e}")
        return False

def main():
    print("="*60)
    print("🎨 TÉLÉCHARGEUR DE PORTRAITS PERCHANCE (MODE MANUEL)")
    print("="*60)
    
    print("\n📋 Instructions :")
    print("1. Allez sur https://perchance.org/ai-face-generator")
    print("2. Entrez ce prompt :")
    print("   'face d'un homme asiatique de l'est qui a {20|30|40} ans")
    print("   en gros plan, tête droite de face, photo professionnelle")
    print("   sur fond blanc. on ne voit que la tête et rien en dessous")
    print("   du cou car la tete prend toute l'image'")
    print("3. Sélectionnez 9 images dans 'How many'")
    print("4. Générez les images")
    print("5. Pour chaque image, clic droit -> Copier l'adresse de l'image")
    print("6. Collez toutes les URLs ci-dessous (une par ligne)")
    print("7. Appuyez sur Entrée deux fois pour terminer")
    
    # Demander l'âge
    print("\n👤 Quel âge ont les personnes sur les photos ?")
    print("  1) 20-35 ans")
    print("  2) 34-50 ans")
    choice = input("Choix (1 ou 2) : ").strip()
    age_range = "21_35" if choice == "1" else "34_50"
    
    # Collecter les URLs
    print(f"\n📥 Collez les URLs des images (Entrée x2 pour terminer) :")
    urls = []
    while True:
        url = input().strip()
        if not url:
            break
        urls.append(url)
    
    if not urls:
        print("❌ Aucune URL fournie !")
        return
    
    print(f"\n📊 {len(urls)} URLs collectées")
    print(f"🎯 Range d'âge : {age_range}")
    print(f"📁 Dossier : {OUTPUT_DIR}")
    
    input("\n⏸️  Appuyez sur Entrée pour commencer le téléchargement...")
    
    # Télécharger toutes les images
    next_num = get_next_number(age_range)
    success_count = 0
    
    for idx, url in enumerate(urls, 1):
        filename = f"asia_asian_M_{age_range}_{next_num + idx - 1:04d}.jpg"
        if download_image(url, filename):
            success_count += 1
    
    print(f"\n✅ Terminé ! {success_count}/{len(urls)} images téléchargées")
    print(f"📁 Dossier : {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
