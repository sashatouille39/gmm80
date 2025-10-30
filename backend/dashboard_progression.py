#!/usr/bin/env python3
"""
Dashboard de progression en temps réel
"""
import time
import os
from pathlib import Path

def get_portrait_count():
    base_dir = Path("/app/backend/static/realistic_portraits")
    counts = {}
    total = 0
    
    for continent in ["africa", "asia", "europe", "america", "middle_east", "oceania"]:
        continent_dir = base_dir / continent
        if continent_dir.exists():
            count = len(list(continent_dir.glob("**/*.jpg")))
            counts[continent] = count
            total += count
        else:
            counts[continent] = 0
    
    return counts, total

def create_progress_bar(current, total, width=40):
    percent = int((current / total) * 100) if total > 0 else 0
    filled = int((current / total) * width) if total > 0 else 0
    bar = "█" * filled + "░" * (width - filled)
    return f"[{bar}] {percent}%"

def main():
    print("🎨 SYSTÈME DE PORTRAITS RÉALISTES - DASHBOARD")
    print("=" * 80)
    
    start_counts, start_total = get_portrait_count()
    start_time = time.time()
    
    print(f"\n📊 État initial: {start_total}/7200 portraits ({int(start_total/7200*100)}%)")
    print("\nDémarrage du monitoring... (Ctrl+C pour arrêter)\n")
    
    iteration = 0
    
    try:
        while True:
            iteration += 1
            time.sleep(30)  # Mise à jour toutes les 30 secondes
            
            os.system('clear')
            
            print("🎨 SYSTÈME DE PORTRAITS RÉALISTES - DASHBOARD TEMPS RÉEL")
            print("=" * 80)
            
            counts, total = get_portrait_count()
            elapsed = time.time() - start_time
            progress_made = total - start_total
            
            # Calculs de vitesse
            minutes_elapsed = elapsed / 60
            portraits_per_minute = progress_made / minutes_elapsed if minutes_elapsed > 0 else 0
            remaining = 7200 - total
            minutes_remaining = remaining / portraits_per_minute if portraits_per_minute > 0 else 0
            
            print(f"\n⏱️  Temps écoulé: {int(minutes_elapsed)} min {int(elapsed % 60)} sec")
            print(f"⚡ Vitesse actuelle: {int(portraits_per_minute)} portraits/minute")
            print(f"⌛ Temps restant estimé: {int(minutes_remaining)} minutes\n")
            
            print("📊 PROGRESSION PAR CONTINENT:")
            print("-" * 80)
            
            continent_names = {
                "africa": "🌍 Afrique",
                "asia": "🌏 Asie",
                "europe": "🇪🇺 Europe",
                "america": "🌎 Amérique",
                "middle_east": "🕌 Moyen-Orient",
                "oceania": "🏝️  Océanie"
            }
            
            for continent in ["africa", "asia", "europe", "america", "middle_east", "oceania"]:
                count = counts[continent]
                name = continent_names[continent]
                bar = create_progress_bar(count, 1200, 50)
                
                status = "✅" if count >= 1200 else ("🔄" if count > 0 else "⏳")
                
                print(f"{status} {name:15} {count:4}/1200  {bar}")
            
            print("-" * 80)
            
            # Barre globale
            global_bar = create_progress_bar(total, 7200, 70)
            print(f"\n📈 PROGRESSION GLOBALE: {total:4}/7200")
            print(f"   {global_bar}\n")
            
            # Statistiques
            print("📊 STATISTIQUES:")
            print(f"   • Portraits téléchargés depuis démarrage: {progress_made}")
            print(f"   • Portraits restants: {remaining}")
            print(f"   • Pourcentage complété: {int(total/7200*100)}%")
            
            if portraits_per_minute > 0:
                eta_hours = int(minutes_remaining // 60)
                eta_minutes = int(minutes_remaining % 60)
                if eta_hours > 0:
                    print(f"   • ETA: {eta_hours}h {eta_minutes}min")
                else:
                    print(f"   • ETA: {eta_minutes} minutes")
            
            print(f"\n💡 Itération #{iteration} - Mise à jour toutes les 30 secondes")
            print("=" * 80)
            
    except KeyboardInterrupt:
        print("\n\n✅ Dashboard arrêté par l'utilisateur")
        counts, total = get_portrait_count()
        print(f"\n📊 État final: {total}/7200 portraits ({int(total/7200*100)}%)")

if __name__ == "__main__":
    main()
