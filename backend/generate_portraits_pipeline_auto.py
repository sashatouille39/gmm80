"""
Pipeline automatique (sans interaction) pour exécution en arrière-plan
"""
import sys
import time
from pathlib import Path

# Importer les modules
from download_random_faces import RandomFaceDownloader
from classify_faces import FaceClassifier
from reorganize_faces import FaceReorganizer


def main():
    """Pipeline automatique complet"""
    start_time = time.time()
    
    print("=" * 80)
    print("🚀 PIPELINE AUTOMATIQUE - GÉNÉRATION DE 7200 PORTRAITS")
    print("=" * 80)
    print(f"\n⏰ Démarré le: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n📋 Étapes:")
    print("   1. Téléchargement de 12,000 images")
    print("   2. Classification par IA")
    print("   3. Réorganisation automatique")
    print("\n" + "=" * 80 + "\n")
    
    try:
        # ===== ÉTAPE 1 : TÉLÉCHARGEMENT =====
        print("\n" + "🎬 " * 20)
        print("ÉTAPE 1/3 : TÉLÉCHARGEMENT")
        print("🎬 " * 20 + "\n")
        
        downloader = RandomFaceDownloader()
        downloader.download_batch(total_images=12000, batch_size=100)
        
        print("\n✅ Étape 1 terminée\n")
        time.sleep(5)
        
        # ===== ÉTAPE 2 : CLASSIFICATION =====
        print("\n" + "🎬 " * 20)
        print("ÉTAPE 2/3 : CLASSIFICATION")
        print("🎬 " * 20 + "\n")
        
        classifier = FaceClassifier()
        classifier.classify_all_images(batch_size=50)
        
        print("\n✅ Étape 2 terminée\n")
        time.sleep(5)
        
        # ===== ÉTAPE 3 : RÉORGANISATION =====
        print("\n" + "🎬 " * 20)
        print("ÉTAPE 3/3 : RÉORGANISATION")
        print("🎬 " * 20 + "\n")
        
        reorganizer = FaceReorganizer()
        reorganizer.reorganize_all()
        
        print("\n✅ Étape 3 terminée\n")
        
        # ===== RÉSUMÉ FINAL =====
        elapsed = time.time() - start_time
        
        print("\n" + "=" * 80)
        print("🎉 PIPELINE TERMINÉ AVEC SUCCÈS")
        print("=" * 80)
        print(f"\n⏱️ Temps total: {elapsed/60:.1f} minutes ({elapsed/3600:.1f} heures)")
        print(f"⏰ Terminé le: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("\n📁 Les 7200 portraits sont prêts !")
        print("   Emplacement: /app/backend/static/portraits/")
        print("\n💡 Structure:")
        print("   • 6 continents")
        print("   • 2 genres par continent")
        print("   • 600 images par genre = 1200 par continent")
        print("\n" + "=" * 80 + "\n")
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Pipeline interrompu par l'utilisateur")
        print("   Progression sauvegardée. Relancez pour continuer.")
        return 1
        
    except Exception as e:
        print(f"\n\n❌ Erreur: {e}")
        print("   Vérifiez les logs pour plus de détails")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
