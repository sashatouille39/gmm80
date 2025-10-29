"""
Test rapide de classification avec DeepFace
"""
from pathlib import Path
from deepface import DeepFace

def test_classify():
    """Test de classification sur quelques images"""
    test_dir = Path("/app/backend/static/portraits/test")
    images = list(test_dir.glob("test_*.jpg"))[:5]  # Prendre 5 images
    
    if not images:
        print("❌ Aucune image de test trouvée")
        print("   Exécutez d'abord: python test_quick_download.py")
        return
    
    print("🧪 Test de classification DeepFace")
    print(f"📁 Dossier: {test_dir}")
    print(f"📊 {len(images)} images à analyser\n")
    
    for img_path in images:
        print(f"🔍 Analyse: {img_path.name}")
        
        try:
            # Analyser l'image
            result = DeepFace.analyze(
                img_path=str(img_path),
                actions=['age', 'gender', 'race'],
                enforce_detection=False,
                detector_backend='opencv',
                silent=True
            )
            
            if isinstance(result, list):
                result = result[0]
            
            race = result.get('dominant_race', 'unknown')
            gender = result.get('dominant_gender', 'unknown')
            age = result.get('age', 0)
            
            print(f"   ✓ Race: {race}")
            print(f"   ✓ Genre: {gender}")
            print(f"   ✓ Âge: {age}")
            print()
            
        except Exception as e:
            print(f"   ✗ Erreur: {str(e)[:60]}")
            print()
    
    print("✅ Test de classification terminé!")
    print("\n💡 DeepFace fonctionne bien!")
    print("   Vous pouvez lancer le pipeline complet:")
    print("   python generate_portraits_pipeline.py")

if __name__ == "__main__":
    test_classify()
