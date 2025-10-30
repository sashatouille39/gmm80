#!/usr/bin/env python3
"""
Script pour détecter et supprimer les portraits qui pourraient représenter des enfants
"""
import os
from pathlib import Path
import shutil
from datetime import datetime

# Dossier des portraits
PORTRAITS_DIR = Path("/app/backend/static/realistic_portraits")
BACKUP_DIR = Path("/app/backend/static/portraits_backup_children")

def analyze_portraits():
    """Analyse les portraits et identifie ceux avec des tranches d'âge jeunes"""
    
    print("🔍 Analyse des portraits...")
    
    all_portraits = list(PORTRAITS_DIR.glob("**/*.jpg"))
    print(f"📊 Total de portraits trouvés: {len(all_portraits)}")
    
    # Analyser les noms de fichiers pour détecter les tranches d'âge
    age_groups = {}
    suspicious_portraits = []
    
    for portrait in all_portraits:
        filename = portrait.name
        parts = filename.split('_')
        
        # Format attendu: continent_ethnicity_gender_age1_age2_number.jpg
        # Ex: europe_white_M_21_35_0001.jpg
        
        try:
            if len(parts) >= 5:
                # Extraire les âges
                age1 = parts[3]
                age2 = parts[4]
                
                age_key = f"{age1}_{age2}"
                if age_key not in age_groups:
                    age_groups[age_key] = []
                age_groups[age_key].append(portrait)
                
                # Détecter les jeunes âges (< 21 ans)
                try:
                    if int(age1) < 21:
                        suspicious_portraits.append(portrait)
                except ValueError:
                    pass
        except Exception as e:
            print(f"⚠️ Erreur d'analyse pour {filename}: {e}")
    
    print("\n📈 Répartition par tranche d'âge:")
    for age_group, portraits in sorted(age_groups.items()):
        print(f"  • {age_group}: {len(portraits)} portraits")
    
    return suspicious_portraits, all_portraits

def check_specific_patterns():
    """Vérifier des motifs spécifiques dans les noms de fichiers"""
    print("\n🔎 Recherche de motifs spécifiques (child, kid, teen, young, etc.)...")
    
    patterns = ['child', 'kid', 'teen', 'young', 'minor', 'juvenile', 'adolescent']
    found = []
    
    for pattern in patterns:
        matches = list(PORTRAITS_DIR.glob(f"**/*{pattern}*.jpg"))
        if matches:
            print(f"  ⚠️ Trouvé {len(matches)} portraits avec '{pattern}'")
            found.extend(matches)
    
    if not found:
        print("  ✅ Aucun motif suspect trouvé dans les noms de fichiers")
    
    return found

def remove_portraits(portraits_to_remove):
    """Supprime les portraits identifiés et crée une sauvegarde"""
    
    if not portraits_to_remove:
        print("\n✅ Aucun portrait à supprimer")
        return
    
    print(f"\n⚠️ {len(portraits_to_remove)} portraits identifiés pour suppression")
    print("\n📦 Création d'une sauvegarde...")
    
    # Créer le dossier de backup
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_folder = BACKUP_DIR / timestamp
    backup_folder.mkdir(parents=True, exist_ok=True)
    
    removed_count = 0
    for portrait in portraits_to_remove:
        try:
            # Copier dans le backup
            relative_path = portrait.relative_to(PORTRAITS_DIR)
            backup_path = backup_folder / relative_path
            backup_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(portrait, backup_path)
            
            # Supprimer l'original
            portrait.unlink()
            removed_count += 1
            
        except Exception as e:
            print(f"  ❌ Erreur lors de la suppression de {portrait.name}: {e}")
    
    print(f"\n✅ {removed_count} portraits supprimés")
    print(f"📁 Sauvegarde créée dans: {backup_folder}")
    
    return removed_count

def main():
    print("=" * 60)
    print("🔍 DÉTECTION ET SUPPRESSION DES PORTRAITS D'ENFANTS")
    print("=" * 60)
    
    # Analyse des portraits
    suspicious_by_age, all_portraits = analyze_portraits()
    suspicious_by_pattern = check_specific_patterns()
    
    # Combiner les résultats
    all_suspicious = list(set(suspicious_by_age + suspicious_by_pattern))
    
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ")
    print("=" * 60)
    print(f"Total de portraits: {len(all_portraits)}")
    print(f"Portraits suspects (âge < 21): {len(suspicious_by_age)}")
    print(f"Portraits suspects (motifs): {len(suspicious_by_pattern)}")
    print(f"Total à supprimer: {len(all_suspicious)}")
    
    if all_suspicious:
        print("\n⚠️ Portraits identifiés pour suppression:")
        for portrait in all_suspicious[:10]:  # Afficher les 10 premiers
            print(f"  • {portrait.relative_to(PORTRAITS_DIR)}")
        if len(all_suspicious) > 10:
            print(f"  ... et {len(all_suspicious) - 10} autres")
        
        # Supprimer
        removed = remove_portraits(all_suspicious)
        
        # Statistiques finales
        remaining = len(all_portraits) - removed
        print(f"\n✅ Portraits restants: {remaining}")
    else:
        print("\n✅ Aucun portrait d'enfant détecté!")
        print("   Tous les portraits semblent être des adultes (21+ ans)")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
