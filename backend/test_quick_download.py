"""
Test rapide : Télécharge 10 images et vérifie que tout fonctionne
"""
import requests
import time
from pathlib import Path

def test_download():
    """Test rapide de téléchargement"""
    test_dir = Path("/app/backend/static/portraits/test")
    test_dir.mkdir(parents=True, exist_ok=True)
    
    url = "https://thispersondoesnotexist.com/"
    
    print("🧪 Test de téléchargement depuis thispersondoesnotexist.com")
    print(f"📁 Dossier de test: {test_dir}\n")
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    
    for i in range(10):
        print(f"[{i+1}/10] Téléchargement...", end=' ')
        
        try:
            response = session.get(url, params={'t': time.time()}, timeout=15)
            
            if response.status_code == 200:
                save_path = test_dir / f"test_{i+1:02d}.jpg"
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                
                size = save_path.stat().st_size
                print(f"✓ ({size/1024:.1f} KB)")
            else:
                print(f"✗ (HTTP {response.status_code})")
            
            time.sleep(1.5)  # Pause entre les requêtes
            
        except Exception as e:
            print(f"✗ ({str(e)[:40]})")
    
    # Compter les fichiers téléchargés
    downloaded = len(list(test_dir.glob("test_*.jpg")))
    
    print(f"\n✅ Test terminé: {downloaded}/10 images téléchargées")
    print(f"📁 Images dans: {test_dir}")
    
    if downloaded >= 8:
        print("\n💡 Le téléchargement fonctionne bien!")
        print("   Vous pouvez lancer le pipeline complet:")
        print("   python generate_portraits_pipeline.py")
    else:
        print("\n⚠️ Taux de succès faible. Vérifiez votre connexion internet.")

if __name__ == "__main__":
    test_download()
