# 🚀 GUIDE RAPIDE - Génération de 7200 Portraits

## ⚡ Démarrage Rapide (3 commandes)

### 1. Lancer la génération
```bash
cd /app/backend
bash start_portraits_generation.sh
```

### 2. Surveiller la progression
```bash
bash monitor_portraits.sh
```

### 3. Voir les logs en temps réel
```bash
tail -f /app/backend/logs/portraits_pipeline.log
```

---

## 📊 Comprendre la Progression

Le système fonctionne en **3 étapes automatiques** :

### Étape 1 : Téléchargement (30-60 min)
- Télécharge 12,000 images depuis thispersondoesnotexist.com
- Voir progression : `ls /app/backend/static/portraits/temp/*.jpg | wc -l`

### Étape 2 : Classification (1-2h)
- Analyse chaque image avec IA (ethnicité, genre, âge)
- Fichier de résultats : `/app/backend/static/portraits/classification_results.json`

### Étape 3 : Réorganisation (5 min)
- Copie les images dans les bons dossiers
- Structure finale : `/app/backend/static/portraits/{continent}/{gender}/`

---

## 🛑 Arrêter le Processus

```bash
pkill -f generate_portraits_pipeline
```

**Note** : La progression est sauvegardée, vous pouvez relancer sans perdre le travail.

---

## 🔄 Relancer après Interruption

```bash
cd /app/backend
python generate_portraits_pipeline_auto.py
```

Le script détecte automatiquement :
- ✅ Images déjà téléchargées
- ✅ Images déjà classifiées  
- ✅ Images déjà réorganisées

Et reprend là où il s'était arrêté !

---

## 📁 Vérifier le Résultat Final

```bash
# Compter les images par continent
for continent in africa asia europe north_america south_america oceania; do
    echo "$continent:"
    echo "  Male: $(ls /app/backend/static/portraits/$continent/male/*.jpg 2>/dev/null | wc -l)"
    echo "  Female: $(ls /app/backend/static/portraits/$continent/female/*.jpg 2>/dev/null | wc -l)"
done
```

**Attendu** : 600 images par genre = 1200 par continent = 7200 total

---

## ⚙️ Mode Avancé (Exécution Manuelle)

Si vous préférez contrôler chaque étape :

```bash
cd /app/backend

# Étape 1
python download_random_faces.py

# Étape 2  
python classify_faces.py

# Étape 3
python reorganize_faces.py
```

---

## 🐛 Dépannage Express

### "Mémoire insuffisante"
→ Machine plus grande automatiquement allouée ✅

### "Téléchargement trop lent"
→ Normal, le serveur limite les requêtes. Soyez patient.

### "Images manquantes dans certaines catégories"
→ Téléchargez plus d'images : modifiez `total_images=15000` dans le script

### "Classification échoue"
→ Vérifiez les logs : `/app/backend/logs/portraits_pipeline.log`

---

## 📞 Monitoring Continu

Créer une boucle de monitoring :
```bash
watch -n 30 bash /app/backend/monitor_portraits.sh
```

Rafraîchit les statistiques toutes les 30 secondes.

---

## ✅ Critères de Succès

Le processus est terminé quand :
- ✅ 7200 images dans `/app/backend/static/portraits/`
- ✅ 6 dossiers de continents créés
- ✅ 600 images male + 600 female par continent
- ✅ Message "🎉 PIPELINE TERMINÉ" dans les logs

---

## 🎯 Utilisation dans l'Application

Les portraits sont accessibles via :
```
/static/portraits/{continent}/{gender}/portrait_XXXX.jpg
```

Exemples :
- `/static/portraits/africa/male/portrait_0001.jpg`
- `/static/portraits/asia/female/portrait_0350.jpg`
- `/static/portraits/europe/male/portrait_0599.jpg`

---

**Temps estimé total : 2-3 heures**

**💡 Conseil** : Lancez le processus et revenez plus tard !
