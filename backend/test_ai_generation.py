"""
Test rapide: Génère 3 portraits pour vérifier que l'API fonctionne
"""
import asyncio
from generate_ai_portraits import AIPortraitGenerator
import os

async def quick_test():
    """Test avec 3 portraits"""
    print("🧪 TEST RAPIDE - Génération de 3 portraits IA\n")
    
    api_key = os.getenv('EMERGENT_LLM_KEY', 'sk-emergent-376483c6134A69bAb0')
    
    # Créer un dossier de test
    generator = AIPortraitGenerator(
        api_key=api_key,
        base_path="/app/backend/static/portraits_test"
    )
    
    # Modifier temporairement pour générer seulement 3 portraits
    generator.TARGET_PER_GENDER = 3
    
    print("📋 Test avec 3 portraits:")
    print("   1. Afrique - Homme")
    print("   2. Asie - Femme") 
    print("   3. Europe - Homme\n")
    
    try:
        # Test Afrique Male
        print("=" * 60)
        success = await generator.generate_portraits_for_continent('africa', 'male')
        if not success:
            print("\n❌ Test échoué pour Afrique")
            return
        
        print("\n✅ Test 1/3 réussi\n")
        await asyncio.sleep(2)
        
        # Test Asie Female  
        print("=" * 60)
        success = await generator.generate_portraits_for_continent('asia', 'female')
        if not success:
            print("\n❌ Test échoué pour Asie")
            return
        
        print("\n✅ Test 2/3 réussi\n")
        await asyncio.sleep(2)
        
        # Test Europe Male
        print("=" * 60)
        success = await generator.generate_portraits_for_continent('europe', 'male')
        if not success:
            print("\n❌ Test échoué pour Europe")
            return
        
        print("\n✅ Test 3/3 réussi\n")
        
        print("=" * 60)
        print("🎉 TOUS LES TESTS RÉUSSIS !")
        print("=" * 60)
        print("\n💡 L'API fonctionne correctement.")
        print("   Vous pouvez lancer la génération complète:")
        print("   python generate_ai_portraits.py")
        print("\n📁 Images de test dans: /app/backend/static/portraits_test/")
        
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        print("   Vérifiez votre clé API et votre crédit")

if __name__ == "__main__":
    asyncio.run(quick_test())
