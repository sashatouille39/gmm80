"""
Pipeline complet : Téléchargement, Classification et Réorganisation
Orchestre les 3 étapes pour générer les 7200 portraits automatiquement
"""
import sys
import time
from pathlib import Path

# Importer les modules
try:
    from download_random_faces import RandomFaceDownloader
    from classify_faces import FaceClassifier
    from reorganize_faces import FaceReorganizer
except ImportError:
    print("❌ Erreur: Modules non trouvés")
    print("   Assurez-vous que tous les scripts sont dans le même dossier")
    sys.exit(1)


class PortraitPipeline:
    """Pipeline complet pour générer les 7200 portraits"""
    
    def __init__(self):
        self.start_time = time.time()
    
    def run_step_1_download(self, num_images: int = 12000):
        """Étape 1 : Téléchargement"""
        print("\n" + "🎬 " * 20)
        print("ÉTAPE 1/3 : TÉLÉCHARGEMENT DES IMAGES")
        print("🎬 " * 20 + "\n")
        
        downloader = RandomFaceDownloader()
        downloader.download_batch(total_images=num_images, batch_size=100)
        
        print("\n✅ Étape 1 terminée\n")
        input("Appuyez sur Entrée pour continuer vers l'étape 2...")
    
    def run_step_2_classify(self):
        """Étape 2 : Classification"""
        print("\n" + "🎬 " * 20)
        print("ÉTAPE 2/3 : CLASSIFICATION DES VISAGES")
        print("🎬 " * 20 + "\n")
        
        classifier = FaceClassifier()
        classifier.classify_all_images()
        
        print("\n✅ Étape 2 terminée\n")
        input("Appuyez sur Entrée pour continuer vers l'étape 3...")
    
    def run_step_3_reorganize(self):
        """Étape 3 : Réorganisation"""
        print("\n" + "🎬 " * 20)
        print("ÉTAPE 3/3 : RÉORGANISATION DES IMAGES")
        print("🎬 " * 20 + "\n")
        
        reorganizer = FaceReorganizer()
        reorganizer.reorganize_all()
        
        print("\n✅ Étape 3 terminée")
    
    def run_full_pipeline(self, num_images: int = 12000):
        """Exécute le pipeline complet"""
        print("=" * 80)
        print("🚀 PIPELINE COMPLET : GÉNÉRATION DE 7200 PORTRAITS")
        print("=" * 80)
        print("\n📋 Le processus comprend 3 étapes :")
        print("   1. Téléchargement de ~12,000 images aléatoires (~30-60 min)")
        print("   2. Classification par IA (ethnicité, genre, âge) (~1-2h)")
        print("   3. Réorganisation automatique dans les dossiers (~5 min)")
        print("\n⏰ Temps total estimé : 2-3 heures")
        print("=" * 80 + "\n")
        
        response = input("Voulez-vous lancer le pipeline complet ? (y/n): ")
        if response.lower() != 'y':
            print("Annulé.")
            return
        
        try:
            # Étape 1
            self.run_step_1_download(num_images)
            
            # Étape 2
            self.run_step_2_classify()
            
            # Étape 3
            self.run_step_3_reorganize()
            
            # Temps total
            elapsed = time.time() - self.start_time
            
            print("\n" + "=" * 80)
            print("🎉 PIPELINE TERMINÉ AVEC SUCCÈS")
            print("=" * 80)
            print(f"\n⏱️ Temps total: {elapsed/60:.1f} minutes ({elapsed/3600:.1f} heures)")
            print("\n📁 Les 7200 portraits sont prêts à être utilisés !")
            print("   Emplacement: /app/backend/static/portraits/")
            print("\n💡 Structure:")
            print("   • 6 continents (africa, asia, europe, north_america, south_america, oceania)")
            print("   • 2 genres par continent (male, female)")
            print("   • 600 images par genre = 1200 par continent")
            print("=" * 80)
            
        except KeyboardInterrupt:
            print("\n\n⚠️ Pipeline interrompu par l'utilisateur")
            print("   Vous pouvez relancer le pipeline, il reprendra où il s'est arrêté")
        except Exception as e:
            print(f"\n\n❌ Erreur: {e}")
            print("   Vérifiez les logs pour plus de détails")


def main():
    """Point d'entrée principal"""
    print("\n" + "🌟 " * 40)
    print("GÉNÉRATEUR AUTOMATIQUE DE PORTRAITS RÉALISTES")
    print("🌟 " * 40 + "\n")
    
    print("📋 Options disponibles:")
    print("   1. Exécuter le pipeline complet (recommandé)")
    print("   2. Exécuter uniquement l'étape 1 (téléchargement)")
    print("   3. Exécuter uniquement l'étape 2 (classification)")
    print("   4. Exécuter uniquement l'étape 3 (réorganisation)")
    print("   5. Quitter\n")
    
    choice = input("Votre choix (1-5): ")
    
    pipeline = PortraitPipeline()
    
    if choice == '1':
        pipeline.run_full_pipeline()
    elif choice == '2':
        pipeline.run_step_1_download()
    elif choice == '3':
        pipeline.run_step_2_classify()
    elif choice == '4':
        pipeline.run_step_3_reorganize()
    elif choice == '5':
        print("Au revoir!")
    else:
        print("Choix invalide")


if __name__ == "__main__":
    main()
