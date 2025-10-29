#!/usr/bin/env python3
"""
Renommer les cheveux existants en séquence 1-N
"""
import os
import shutil
from pathlib import Path

hair_male_dir = Path("/app/backend/static/portraits/hair_male")
hair_female_dir = Path("/app/backend/static/portraits/hair_female")

def renumber_files(directory, prefix="hair_male"):
    """Renomme tous les fichiers PNG en séquence"""
    # Lister tous les PNG
    files = sorted(directory.glob("*.png"))
    
    if not files:
        print(f"❌ Aucun fichier dans {directory}")
        return 0
    
    print(f"\n📂 Traitement de {directory.name}/")
    print(f"   Fichiers trouvés: {len(files)}")
    
    # Créer dossier temporaire
    temp_dir = directory / "_temp"
    temp_dir.mkdir(exist_ok=True)
    
    # Copier dans temp avec nouveaux noms
    for idx, old_file in enumerate(files, 1):
        new_name = f"{prefix}_{idx}.png"
        shutil.copy2(old_file, temp_dir / new_name)
        print(f"   {old_file.name} → {new_name}")
    
    # Supprimer les anciens
    for old_file in files:
        old_file.unlink()
    
    # Déplacer les nouveaux
    for new_file in temp_dir.glob("*.png"):
        shutil.move(str(new_file), directory / new_file.name)
    
    # Supprimer temp
    temp_dir.rmdir()
    
    print(f"   ✅ {len(files)} fichiers renommés en séquence")
    return len(files)

if __name__ == "__main__":
    print("="*60)
    print("RENOMMAGE DES CALQUES CHEVEUX")
    print("="*60)
    
    # Renommer homme
    count_m = renumber_files(hair_male_dir, "hair_male")
    
    # Renommer femme (si existants)
    count_f = renumber_files(hair_female_dir, "hair_female")
    
    print("\n" + "="*60)
    print(f"✅ TERMINÉ")
    print(f"   Homme: {count_m} fichiers → hair_male_1.png à hair_male_{count_m}.png")
    if count_f > 0:
        print(f"   Femme: {count_f} fichiers → hair_female_1.png à hair_female_{count_f}.png")
    print("="*60 + "\n")
