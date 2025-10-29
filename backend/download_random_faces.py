"""
Étape 1 : Téléchargement massif d'images depuis thispersondoesnotexist.com
Télécharge environ 12,000 images aléatoires pour avoir assez de diversité
"""
import os
import time
import requests
from pathlib import Path
from tqdm import tqdm


class RandomFaceDownloader:
    """Télécharge des visages aléatoires depuis thispersondoesnotexist.com"""
    
    def __init__(self, temp_dir: str = "/app/backend/static/portraits/temp"):
        self.temp_dir = Path(temp_dir)
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        self.url = "https://thispersondoesnotexist.com/"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def download_single_image(self, index: int, max_retries: int = 3) -> bool:
        """Télécharge une seule image"""
        save_path = self.temp_dir / f"temp_{index:05d}.jpg"
        
        # Si le fichier existe déjà, passer
        if save_path.exists() and save_path.stat().st_size > 10000:  # > 10KB
            return True
        
        for attempt in range(max_retries):
            try:
                # Ajouter un timestamp pour éviter le cache
                response = self.session.get(
                    self.url,
                    params={'t': time.time()},
                    timeout=30,
                    stream=True
                )
                
                if response.status_code == 200:
                    # Vérifier que c'est bien une image
                    content_type = response.headers.get('content-type', '')
                    if 'image' not in content_type:
                        time.sleep(2)
                        continue
                    
                    # Sauvegarder l'image
                    with open(save_path, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    
                    # Vérifier la taille du fichier
                    if save_path.stat().st_size > 10000:  # > 10KB
                        return True
                    else:
                        save_path.unlink()  # Supprimer le fichier corrompu
                        
                time.sleep(1)  # Pause entre les tentatives
                
            except Exception as e:
                if attempt == max_retries - 1:
                    print(f"\n   ⚠️ Erreur pour image {index}: {e}")
                time.sleep(2)
        
        return False
    
    def download_batch(self, total_images: int = 12000, batch_size: int = 100):
        """Télécharge un lot d'images avec barre de progression"""
        print("=" * 80)
        print("📥 TÉLÉCHARGEMENT MASSIF D'IMAGES ALÉATOIRES")
        print("=" * 80)
        print(f"\n📦 Source: {self.url}")
        print(f"📁 Destination: {self.temp_dir}")
        print(f"🎯 Objectif: {total_images} images")
        print(f"\n⏰ Temps estimé: {total_images * 1.5 / 60:.0f} minutes")
        print("\n" + "=" * 80)
        
        # Compter les images existantes
        existing = len(list(self.temp_dir.glob("temp_*.jpg")))
        if existing > 0:
            print(f"\nℹ️ {existing} images déjà téléchargées, reprise...")
            start_index = existing
        else:
            start_index = 0
        
        # Télécharger avec barre de progression
        downloaded = 0
        failed = 0
        
        with tqdm(total=total_images, initial=start_index, desc="Téléchargement") as pbar:
            for i in range(start_index, total_images):
                success = self.download_single_image(i)
                
                if success:
                    downloaded += 1
                else:
                    failed += 1
                
                pbar.update(1)
                pbar.set_postfix({
                    'OK': downloaded,
                    'Échec': failed
                })
                
                # Pause toutes les 100 images pour ne pas surcharger le serveur
                if (i + 1) % batch_size == 0:
                    time.sleep(5)
        
        # Statistiques finales
        total_files = len(list(self.temp_dir.glob("temp_*.jpg")))
        
        print("\n" + "=" * 80)
        print("✅ TÉLÉCHARGEMENT TERMINÉ")
        print("=" * 80)
        print(f"\n📊 Statistiques:")
        print(f"   • Images téléchargées: {total_files}")
        print(f"   • Nouvelles images: {downloaded}")
        print(f"   • Échecs: {failed}")
        print(f"   • Emplacement: {self.temp_dir}")
        print("\n💡 Passez à l'étape suivante : classification des visages")
        print("   Commande: python classify_faces.py")


def main():
    """Point d'entrée principal"""
    print("\n🚀 Démarrage du téléchargement...")
    print("\n⚠️ Ce processus peut prendre 30-60 minutes")
    print("   Vous pouvez l'arrêter (Ctrl+C) et le relancer plus tard.\n")
    
    downloader = RandomFaceDownloader()
    downloader.download_batch(total_images=12000, batch_size=100)


if __name__ == "__main__":
    main()
