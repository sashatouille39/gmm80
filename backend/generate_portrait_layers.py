"""
Script pour générer un ensemble complet de calques de portraits par IA
Génère des variations multiples, surtout pour les cheveux (10-15 coupes différentes)
Les calques sont cohérents avec la nationalité et le sexe du personnage
"""
import os
import sys
import asyncio
from dotenv import load_dotenv

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.portrait_generator_service import portrait_service

load_dotenv()


async def generate_portrait_library():
    """
    Génère une bibliothèque complète de calques de portraits
    Nationalités représentatives par continent avec plusieurs variations
    """
    
    # Nationalités représentatives par continent (préjugés typiques)
    representative_nationalities = {
        # Europe du Nord (blonds, yeux bleus, peau claire)
        'Nordic': ['Suédois', 'Norvégien', 'Finlandais'],
        
        # Europe de l'Ouest (varié)
        'Western Europe': ['Français', 'Allemand', 'Britannique'],
        
        # Europe du Sud (méditerranéens, cheveux bruns/noirs)
        'Mediterranean': ['Italien', 'Espagnol', 'Grec'],
        
        # Europe de l'Est (blonds/châtains, yeux clairs)
        'Eastern Europe': ['Russe', 'Polonais'],
        
        # Asie de l'Est (cheveux noirs raides, yeux bridés)
        'East Asia': ['Japonais', 'Coréen', 'Chinois'],
        
        # Asie du Sud (peau plus foncée, cheveux noirs)
        'South Asia': ['Indien'],
        
        # Moyen-Orient (peau olive, cheveux noirs/bruns)
        'Middle East': ['Turc', 'Iranien'],
        
        # Afrique (peau foncée, cheveux crépus)
        'Africa': ['Nigérian'],
        
        # Amérique Latine (varié, peau olive/brune)
        'Latin America': ['Mexicain', 'Brésilien', 'Argentin'],
        
        # Amérique du Nord / Mixte (très varié)
        'North America': ['Américain', 'Canadien'],
    }
    
    # Sexes
    genders = ['male', 'female']
    
    # Nombre de variations par combinaison nationalité/sexe
    # Pour les cheveux, on génère plus de variations
    base_variations = 3  # 3 variations de base (forme de tête)
    eyes_variations = 3  # 3 variations d'yeux
    hair_variations = 12  # 12 variations de cheveux (BEAUCOUP DE COUPES)
    mouth_variations = 3  # 3 variations de bouche
    nose_variations = 3  # 3 variations de nez
    
    total_nationalities = sum(len(countries) for countries in representative_nationalities.values())
    total_portraits = total_nationalities * len(genders)
    
    print("=" * 80)
    print("🎨 GÉNÉRATEUR DE BIBLIOTHÈQUE DE PORTRAITS PAR CALQUES")
    print("=" * 80)
    print(f"\n📊 Configuration:")
    print(f"   • Continents: {len(representative_nationalities)}")
    print(f"   • Nationalités: {total_nationalities}")
    print(f"   • Sexes: {len(genders)}")
    print(f"   • Variations par type de calque:")
    print(f"      - Base (tête): {base_variations} variations")
    print(f"      - Yeux: {eyes_variations} variations")
    print(f"      - Cheveux: {hair_variations} variations ⭐")
    print(f"      - Bouche: {mouth_variations} variations")
    print(f"      - Nez: {nose_variations} variations")
    print(f"\n📈 Total à générer: {total_portraits} portraits complets")
    print(f"   • Total calques: ~{total_portraits * (base_variations + eyes_variations + hair_variations + mouth_variations + nose_variations)}")
    print(f"\n⏱️  Temps estimé: ~3-5 heures (chaque calque prend ~15-20 secondes)")
    print(f"\n💡 Les calques seront réutilisables et mixables!")
    print("=" * 80)
    print()
    
    response = input("🚀 Commencer la génération? (yes/no): ")
    if response.lower() not in ['yes', 'y', 'oui', 'o']:
        print("❌ Génération annulée")
        return
    
    print("\n🎬 Démarrage de la génération...\n")
    
    total_generated = 0
    total_errors = 0
    
    for continent, nationalities in representative_nationalities.items():
        print(f"\n{'='*80}")
        print(f"🌍 CONTINENT: {continent}")
        print(f"{'='*80}")
        
        for nationality in nationalities:
            for gender in genders:
                gender_label = "Homme" if gender == 'male' else "Femme"
                print(f"\n📸 {nationality} - {gender_label}")
                print(f"   {'-'*60}")
                
                try:
                    # Générer les variations de BASE
                    print(f"   🎭 Génération de {base_variations} variations de base...")
                    for i in range(1, base_variations + 1):
                        try:
                            layers = await portrait_service.generate_portrait_layers_set(
                                nationality=nationality,
                                gender=gender,
                                age=25,
                                set_id=i,
                                layer_types=['base']  # Seulement la base
                            )
                            if layers:
                                print(f"      ✅ Base #{i} générée")
                                total_generated += 1
                            await asyncio.sleep(1)  # Petit délai entre les requêtes
                        except Exception as e:
                            print(f"      ❌ Erreur base #{i}: {str(e)}")
                            total_errors += 1
                    
                    # Générer les variations d'YEUX
                    print(f"   👁️  Génération de {eyes_variations} variations d'yeux...")
                    for i in range(1, eyes_variations + 1):
                        try:
                            layers = await portrait_service.generate_portrait_layers_set(
                                nationality=nationality,
                                gender=gender,
                                age=25,
                                set_id=i,
                                layer_types=['eyes']
                            )
                            if layers:
                                print(f"      ✅ Yeux #{i} générés")
                                total_generated += 1
                            await asyncio.sleep(1)
                        except Exception as e:
                            print(f"      ❌ Erreur yeux #{i}: {str(e)}")
                            total_errors += 1
                    
                    # Générer les variations de CHEVEUX (BEAUCOUP!)
                    print(f"   💇 Génération de {hair_variations} variations de cheveux...")
                    for i in range(1, hair_variations + 1):
                        try:
                            layers = await portrait_service.generate_portrait_layers_set(
                                nationality=nationality,
                                gender=gender,
                                age=25,
                                set_id=i,
                                layer_types=['hair']
                            )
                            if layers:
                                print(f"      ✅ Cheveux #{i} générés")
                                total_generated += 1
                            await asyncio.sleep(1)
                        except Exception as e:
                            print(f"      ❌ Erreur cheveux #{i}: {str(e)}")
                            total_errors += 1
                    
                    # Générer les variations de BOUCHE
                    print(f"   👄 Génération de {mouth_variations} variations de bouche...")
                    for i in range(1, mouth_variations + 1):
                        try:
                            layers = await portrait_service.generate_portrait_layers_set(
                                nationality=nationality,
                                gender=gender,
                                age=25,
                                set_id=i,
                                layer_types=['mouth']
                            )
                            if layers:
                                print(f"      ✅ Bouche #{i} générée")
                                total_generated += 1
                            await asyncio.sleep(1)
                        except Exception as e:
                            print(f"      ❌ Erreur bouche #{i}: {str(e)}")
                            total_errors += 1
                    
                    # Générer les variations de NEZ
                    print(f"   👃 Génération de {nose_variations} variations de nez...")
                    for i in range(1, nose_variations + 1):
                        try:
                            layers = await portrait_service.generate_portrait_layers_set(
                                nationality=nationality,
                                gender=gender,
                                age=25,
                                set_id=i,
                                layer_types=['nose']
                            )
                            if layers:
                                print(f"      ✅ Nez #{i} généré")
                                total_generated += 1
                            await asyncio.sleep(1)
                        except Exception as e:
                            print(f"      ❌ Erreur nez #{i}: {str(e)}")
                            total_errors += 1
                    
                    print(f"   ✅ {nationality} {gender_label} terminé!")
                    
                except Exception as e:
                    print(f"   ❌ Erreur majeure pour {nationality} {gender_label}: {str(e)}")
                    total_errors += 1
                    continue
    
    print(f"\n{'='*80}")
    print("🎉 GÉNÉRATION TERMINÉE!")
    print(f"{'='*80}")
    print(f"✅ Calques générés avec succès: {total_generated}")
    print(f"❌ Erreurs: {total_errors}")
    print(f"📁 Emplacement: /app/backend/static/portraits/")
    print(f"\n💡 Les portraits peuvent maintenant être utilisés par le système de génération de joueurs!")
    print("=" * 80)


if __name__ == "__main__":
    print("🎨 Générateur de bibliothèque de portraits par calques\n")
    print("Ce script va générer des centaines de calques de portraits par IA")
    print("Les calques seront cohérents avec la nationalité et le sexe\n")
    
    asyncio.run(generate_portrait_library())
