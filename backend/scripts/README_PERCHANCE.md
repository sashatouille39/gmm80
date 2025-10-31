# Générateur de Portraits Perchance

Ce dossier contient deux scripts pour générer et télécharger des portraits d'hommes asiatiques depuis https://perchance.org/ai-face-generator

## 📋 Scripts disponibles

### 1. Script Automatique (Playwright)
**Fichier:** `generate_perchance_portraits.py`

Script qui automatise tout le processus : navigation, génération et téléchargement.

**Utilisation:**
```bash
cd /app/backend
python scripts/generate_perchance_portraits.py
```

**Avantages:**
- Entièrement automatique
- Peut générer plusieurs lots
- Gère les âges aléatoires (20, 30, 40 ans)

**Inconvénients:**
- Peut être bloqué par le site
- Plus complexe à déboguer

---

### 2. Script Manuel (Recommandé)
**Fichier:** `download_perchance_manual.py`

Script simple qui télécharge les images depuis les URLs que vous copiez.

**Utilisation:**

1. **Générez les images sur le site:**
   - Allez sur https://perchance.org/ai-face-generator
   - Entrez le prompt suivant :
     ```
     face d'un homme asiatique de l'est qui a {20|30|40} ans en gros plan, 
     tête droite de face, photo professionnelle sur fond blanc. 
     on ne voit que la tête et rien en dessous du cou car la tete prend toute l'image
     ```
   - Sélectionnez **9** dans "How many"
   - Cliquez sur "Generate"

2. **Copiez les URLs des images:**
   - Clic droit sur chaque image → "Copier l'adresse de l'image"
   - Répétez pour les 9 images

3. **Exécutez le script:**
   ```bash
   cd /app/backend
   python scripts/download_perchance_manual.py
   ```

4. **Suivez les instructions:**
   - Choisissez la tranche d'âge (1 ou 2)
   - Collez toutes les URLs (une par ligne)
   - Appuyez sur Entrée deux fois
   - Les images seront téléchargées automatiquement

**Avantages:**
- Très fiable
- Contrôle total sur les images
- Facile à déboguer
- Pas de risque de blocage

---

## 📁 Organisation des fichiers

Les images sont sauvegardées dans :
```
/app/backend/static/realistic_portraits/asia/asian/M/
```

**Nomenclature:**
- `asia_asian_M_21_35_XXXX.jpg` → Hommes de 20-35 ans
- `asia_asian_M_34_50_XXXX.jpg` → Hommes de 34-50 ans

Les numéros sont automatiquement incrémentés pour éviter les doublons.

---

## 🎯 Prompt utilisé

```
face d'un homme asiatique de l'est qui a {20|30|40} ans en gros plan, 
tête droite de face, photo professionnelle sur fond blanc. 
on ne voit que la tête et rien en dessous du cou car la tete prend toute l'image
```

**Variations possibles:**
- Remplacez `{20|30|40}` par un âge spécifique
- Ajoutez des détails : "souriant", "sérieux", "lunettes", etc.
- Modifiez le fond : "fond gris", "fond neutre", etc.

---

## 📊 Statistiques actuelles

Pour voir combien d'images vous avez déjà :
```bash
ls -1 /app/backend/static/realistic_portraits/asia/asian/M/ | wc -l
```

Pour voir la répartition par âge :
```bash
ls -1 /app/backend/static/realistic_portraits/asia/asian/M/*21_35* | wc -l  # 20-35 ans
ls -1 /app/backend/static/realistic_portraits/asia/asian/M/*34_50* | wc -l  # 34-50 ans
```

---

## 🔧 Dépendances

**Script automatique:**
```bash
pip install playwright
playwright install chromium
```

**Script manuel:**
```bash
pip install requests
```
(déjà installé normalement)

---

## 💡 Conseils

1. **Utilisez le script manuel** pour plus de contrôle et de fiabilité
2. **Générez par lots de 9** pour être efficace
3. **Vérifiez la qualité** des images avant de les télécharger en masse
4. **Variez les âges** pour avoir une bibliothèque diversifiée
5. **Sauvegardez régulièrement** votre progression

---

## ⚠️ Notes importantes

- Les images sont automatiquement numérotées pour éviter les écrasements
- Le script détecte les fichiers existants et continue la numérotation
- Les deux scripts créent automatiquement le dossier de sortie si nécessaire
- Les images sont au format JPG
