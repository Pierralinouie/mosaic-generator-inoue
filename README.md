# 🎨 Mosaic Generator API - Inouïe Distribution

Service Python Flask pour générer des mosaïques 2x2 d'images avec texte personnalisé.

## 📋 Fichiers inclus

- `app.py` - Application Flask principale
- `requirements.txt` - Dépendances Python
- `Procfile` - Configuration pour Railway/Render
- `runtime.txt` - Version Python

## 🚀 Déploiement sur Railway.app (GRATUIT)

### Étape 1 : Créer un compte Railway

1. Allez sur https://railway.app/
2. Cliquez sur "Start a New Project"
3. Connectez-vous avec GitHub (recommandé)

### Étape 2 : Créer un nouveau projet

1. Cliquez sur "New Project"
2. Sélectionnez "Deploy from GitHub repo"
3. **OU** sélectionnez "Empty Project" si vous voulez uploader manuellement

### Étape 3A : Déploiement via GitHub (RECOMMANDÉ)

1. Créez un nouveau repository GitHub
2. Uploadez les 4 fichiers (`app.py`, `requirements.txt`, `Procfile`, `runtime.txt`)
3. Dans Railway, sélectionnez ce repository
4. Railway détectera automatiquement Python et déploiera

### Étape 3B : Déploiement manuel (ALTERNATIVE)

1. Dans Railway, créez un "Empty Project"
2. Cliquez sur "New" > "Empty Service"
3. Allez dans "Settings" > "Source"
4. Uploadez les 4 fichiers via l'interface
5. Railway déploiera automatiquement

### Étape 4 : Obtenir l'URL du service

1. Une fois déployé, allez dans l'onglet "Settings"
2. Scrollez jusqu'à "Domains"
3. Cliquez sur "Generate Domain"
4. Copiez l'URL (ex: `https://votre-app.up.railway.app`)

**✅ Votre API est maintenant en ligne !**

---

## 🚀 Alternative : Déploiement sur Render.com (GRATUIT)

### Étape 1 : Créer un compte Render

1. Allez sur https://render.com/
2. Inscrivez-vous (GitHub recommandé)

### Étape 2 : Créer un Web Service

1. Cliquez sur "New +"
2. Sélectionnez "Web Service"
3. Connectez votre repository GitHub (ou uploadez les fichiers)
4. Configurez :
   - **Name** : `mosaic-generator`
   - **Environment** : `Python 3`
   - **Build Command** : `pip install -r requirements.txt`
   - **Start Command** : `gunicorn app:app`
   - **Plan** : `Free`

5. Cliquez sur "Create Web Service"

### Étape 3 : Obtenir l'URL

Une fois déployé (2-3 minutes), votre URL sera :
`https://mosaic-generator.onrender.com`

---

## 🔧 Configuration dans Make.com

### Module HTTP dans Make.com

**URL :**
```
https://VOTRE-URL-RAILWAY.up.railway.app/generate-mosaic
```
*(Ou votre URL Render)*

**Method :** `POST`

**Headers :**

| Name | Value |
|------|-------|
| Content-Type | application/json |

**Body type :** `Raw`

**Content type :** `JSON (application/json)`

**Request content :**
```json
{
  "images": [
    "{{1.carousel_images[1]}}",
    "{{1.carousel_images[2]}}",
    "{{1.carousel_images[3]}}",
    "{{1.carousel_images[4]}}"
  ],
  "date_text": "Vendredi {{formatDate(now; 'DD/MM/YYYY')}}"
}
```

### Récupérer l'image générée

La réponse sera un fichier JPEG. Dans Make.com :

1. Le module HTTP retournera l'image dans `{{data}}`
2. Pour l'utiliser dans LinkedIn/Facebook/Instagram, utilisez directement cette data
3. Ou sauvegardez-la temporairement avec un module "HTTP - Download a file"

---

## 🧪 Tester votre API

### Test 1 : Health Check

```bash
curl https://VOTRE-URL.up.railway.app/health
```

Réponse attendue :
```json
{"status": "ok", "service": "mosaic-generator"}
```

### Test 2 : Générer une mosaïque

```bash
curl -X POST https://VOTRE-URL.up.railway.app/generate-mosaic \
  -H "Content-Type: application/json" \
  -d '{
    "images": [
      "https://i.scdn.co/image/ab67616d0000b273...",
      "https://i.scdn.co/image/ab67616d0000b273...",
      "https://i.scdn.co/image/ab67616d0000b273...",
      "https://i.scdn.co/image/ab67616d0000b273..."
    ],
    "date_text": "Vendredi 23/11/2024"
  }' \
  --output mosaic.jpg
```

Vous devriez obtenir un fichier `mosaic.jpg` de 1080x1080 pixels.

---

## 📝 Format de l'API

### Endpoint : POST /generate-mosaic

**Request Body :**
```json
{
  "images": [
    "string (URL)",
    "string (URL)", 
    "string (URL)",
    "string (URL)"
  ],
  "date_text": "string (optionnel)"
}
```

**Response :**
- **Success** : Fichier JPEG (1080x1080 pixels)
- **Error** : JSON avec `{"error": "message"}`

### Codes de retour

- `200` : Succès, image générée
- `400` : Erreur de validation (nombre d'images incorrect, URL invalide)
- `500` : Erreur serveur

---

## 🎯 Caractéristiques de la mosaïque

- **Taille finale** : 1080 x 1080 pixels (format Instagram/Facebook)
- **Disposition** : Grille 2x2 (540x540 par image)
- **Format** : JPEG, qualité 95%
- **Texte** : Centré en bas, fond noir semi-transparent
- **Police** : DejaVu Sans Bold, 40pt, blanc

---

## 💰 Coûts

### Railway.app (Plan gratuit)
- ✅ 500 heures/mois (21 jours continus)
- ✅ Largement suffisant pour votre usage
- ✅ Aucune carte bancaire requise

### Render.com (Plan gratuit)
- ✅ 750 heures/mois
- ⚠️ Service en veille après 15min d'inactivité (redémarre en ~30 secondes)
- ✅ Aucune carte bancaire requise

**Les deux sont gratuits à vie pour votre usage !**

---

## 🐛 Dépannage

### Erreur : "Failed to download image"
- Vérifiez que les URLs d'images sont accessibles publiquement
- Vérifiez que les URLs commencent par `https://`

### Erreur : "Exactly 4 image URLs required"
- Assurez-vous d'envoyer exactement 4 URLs dans le tableau `images`

### Service inaccessible
- Vérifiez que le déploiement est terminé (icône verte sur Railway/Render)
- Testez le endpoint `/health` pour vérifier que le service répond

### Timeout sur Make.com
- Augmentez le timeout du module HTTP à 60 secondes
- Les images volumineuses peuvent prendre quelques secondes à télécharger

---

## 📧 Support

Pour toute question :
- pierrealexandre@zproduction.org
- pa.gauthier@inouiedistribution.com

---

**Made with ❤️ for Inouïe Distribution & Palmier Rouge**
