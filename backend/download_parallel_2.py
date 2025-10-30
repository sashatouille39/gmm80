#!/usr/bin/env python3
"""
Script pour télécharger Moyen-Orient et Océanie en parallèle
"""
import asyncio
import sys
sys.path.insert(0, '/app/backend')

from download_parallel import download_multiple_continents

if __name__ == "__main__":
    continents_to_download = ["middle_east", "oceania"]
    
    print("🚀🚀 TÉLÉCHARGEMENT PARALLÈLE - 2 CONTINENTS")
    print("=" * 70)
    print("Continents : middle_east, oceania")
    print("=" * 70)
    
    asyncio.run(download_multiple_continents(continents_to_download))
    
    print("\n" + "=" * 70)
    print("✅ TÉLÉCHARGEMENT PARALLÈLE TERMINÉ")
    print("=" * 70)
