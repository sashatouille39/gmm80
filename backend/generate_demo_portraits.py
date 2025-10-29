"""
Script de test rapide pour générer quelques portraits de démonstration
Génère 2-3 portraits complets pour tester le système
"""
import os
import sys
import asyncio
from dotenv import load_dotenv

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.portrait_generator_service import portrait_service

load_dotenv()


async def generate_demo_portraits():
    """
    Génère quelques portraits de démonstration pour tester le système
    """
    
    print("=" * 80)
    print("🎨 GÉNÉRATEUR DE PORTRAITS DE DÉMONSTRATION")
    print("=" * 80)
    print("\n📊 Ce script va générer 6 portraits de test (3 hommes + 3 femmes)")
    print("   pour 3 nationalités représentatives:\n")
    print("   • Suédois (Europe du Nord - blond, yeux bleus)")
    print("   • Japonais (Asie de l'Est - cheveux noirs, traits asiatiques)")
    print("   • Nigérian (Afrique - peau foncée, cheveux crépus)\n")
    print("⏱️  Temps estimé: ~5-10 minutes\n")
    print("=" * 80)
    
    # Nationalités de test
    test_cases = [
        ('Suédois', 'male', '🇸🇪 Homme suédois'),
        ('Suédois', 'female', '🇸🇪 Femme suédoise'),
        ('Japonais', 'male', '🇯🇵 Homme japonais'),
        ('Japonais', 'female', '🇯🇵 Femme japonaise'),
        ('Nigérian', 'male', '🇳🇬 Homme nigérian'),
        ('Nigérian', 'female', '🇳🇬 Femme nigériane'),
    ]
    
    response = input("\n🚀 Lancer la génération de démonstration? (yes/no): ")
    if response.lower() not in ['yes', 'y', 'oui', 'o']:
        print("❌ Génération annulée")
        return
    
    print("\n🎬 Démarrage de la génération...\n")
    
    total_generated = 0
    total_errors = 0
    
    for nationality, gender, label in test_cases:
        print(f"\n{'='*80}")
        print(f"📸 Génération: {label}")
        print(f"{'='*80}")
        
        try:
            # Générer 1 set complet de calques
            print(f"   🎨 Génération du portrait complet...")
            layers = await portrait_service.generate_portrait_layers_set(
                nationality=nationality,
                gender=gender,
                age=25,
                set_id=1
            )
            
            if layers:
                print(f"\n   ✅ Portrait généré avec succès!")
                print(f"   📁 Calques générés:")
                for layer_type, path in layers.items():
                    print(f"      • {layer_type}: {path}")
                total_generated += 1
            else:
                print(f"   ❌ Échec de la génération")
                total_errors += 1
            
            # Petit délai entre les générations
            await asyncio.sleep(2)
            
        except Exception as e:
            print(f"   ❌ Erreur: {str(e)}")
            total_errors += 1
            continue
    
    print(f"\n{'='*80}")
    print("🎉 GÉNÉRATION DE DÉMONSTRATION TERMINÉE!")
    print(f"{'='*80}")
    print(f"✅ Portraits générés avec succès: {total_generated}/{len(test_cases)}")
    print(f"❌ Erreurs: {total_errors}")
    print(f"\n📁 Emplacement: /app/backend/static/portraits/")
    print(f"\n💡 Vous pouvez maintenant tester l'affichage des portraits dans le jeu!")
    print("=" * 80)


if __name__ == "__main__":
    print("🎨 Générateur de portraits de démonstration\n")
    print("Ce script génère quelques portraits pour tester le système\n")
    
    asyncio.run(generate_demo_portraits())
