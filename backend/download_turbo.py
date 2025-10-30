#!/usr/bin/env python3
"""
Script ULTRA optimisé - 5 continents en parallèle sur machine puissante
"""
import asyncio
import sys
sys.path.insert(0, '/app/backend')

from download_parallel import download_multiple_continents

if __name__ == "__main__":
    # Télécharger TOUS les continents restants en parallèle
    continents_to_download = ["asia", "europe", "america", "middle_east", "oceania"]
    
    print("🚀🚀🚀🚀🚀 TÉLÉCHARGEMENT ULTRA RAPIDE - 5 CONTINENTS EN PARALLÈLE")
    print("=" * 70)
    print("Continents : asia, europe, america, middle_east, oceania")
    print("Machine puissante détectée - Mode turbo activé!")
    print("=" * 70)
    
    asyncio.run(download_multiple_continents(continents_to_download))
    
    print("\n" + "=" * 70)
    print("✅ TÉLÉCHARGEMENT ULTRA RAPIDE TERMINÉ")
    print("=" * 70)
