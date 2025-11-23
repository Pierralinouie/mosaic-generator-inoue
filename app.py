from flask import Flask, request, jsonify, send_file
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import os
from datetime import datetime

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "ok", "service": "mosaic-generator"})

@app.route('/generate-mosaic', methods=['POST'])
def generate_mosaic():
    """
    Génère une mosaïque 2x2 à partir de 4 URLs d'images
    
    Body JSON attendu:
    {
        "images": ["url1", "url2", "url3", "url4"],
        "date_text": "Vendredi 23/11/2024" (optionnel)
    }
    """
    try:
        data = request.get_json()
        
        # Validation
        if not data or 'images' not in data:
            return jsonify({"error": "Missing 'images' array in request"}), 400
        
        image_urls = data['images']
        
        if len(image_urls) != 4:
            return jsonify({"error": "Exactly 4 image URLs required"}), 400
        
        date_text = data.get('date_text', f"Vendredi {datetime.now().strftime('%d/%m/%Y')}")
        
        # Télécharger les images
        print("📥 Téléchargement des images...")
        images = []
        for i, url in enumerate(image_urls):
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                img = Image.open(BytesIO(response.content))
                # Convertir en RGB si nécessaire
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                images.append(img)
                print(f"✓ Image {i+1} téléchargée")
            except Exception as e:
                return jsonify({"error": f"Failed to download image {i+1}: {str(e)}"}), 400
        
        # Créer la mosaïque
        print("🎨 Création de la mosaïque...")
        mosaic_size = 1080
        tile_size = mosaic_size // 2  # 540x540 par image
        
        # Créer le canvas blanc
        mosaic = Image.new('RGB', (mosaic_size, mosaic_size), 'white')
        
        # Positionner les 4 images
        positions = [
            (0, 0),           # Haut gauche
            (tile_size, 0),   # Haut droite
            (0, tile_size),   # Bas gauche
            (tile_size, tile_size)  # Bas droite
        ]
        
        for img, pos in zip(images, positions):
            # Redimensionner en carré en cropant au centre
            img_resized = img.resize((tile_size, tile_size), Image.Resampling.LANCZOS)
            mosaic.paste(img_resized, pos)
        
        # Ajouter le texte de date
        print("✍️ Ajout du texte...")
        draw = ImageDraw.Draw(mosaic)
        
        # Essayer de charger une police, sinon utiliser la police par défaut
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
        except:
            try:
                font = ImageFont.truetype("arial.ttf", 40)
            except:
                font = ImageFont.load_default()
        
        # Calculer la position centrée du texte
        bbox = draw.textbbox((0, 0), date_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        text_x = (mosaic_size - text_width) // 2
        text_y = mosaic_size - text_height - 30
        
        # Ajouter un fond semi-transparent pour le texte
        padding = 10
        draw.rectangle(
            [text_x - padding, text_y - padding, text_x + text_width + padding, text_y + text_height + padding],
            fill=(0, 0, 0, 180)
        )
        
        # Dessiner le texte en blanc
        draw.text((text_x, text_y), date_text, fill='white', font=font)
        
        # Sauvegarder l'image en mémoire
        print("💾 Sauvegarde de l'image...")
        img_io = BytesIO()
        mosaic.save(img_io, 'JPEG', quality=95)
        img_io.seek(0)
        
        print("✅ Mosaïque générée avec succès!")
        
        # Retourner l'image
        return send_file(
            img_io,
            mimetype='image/jpeg',
            as_attachment=True,
            download_name=f'mosaic_{datetime.now().strftime("%Y%m%d_%H%M%S")}.jpg'
        )
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET'])
def index():
    """Page d'accueil avec documentation"""
    return """
    <html>
    <head><title>Mosaic Generator API</title></head>
    <body style="font-family: Arial; max-width: 800px; margin: 50px auto; padding: 20px;">
        <h1>🎨 Mosaic Generator API</h1>
        <p>Service de génération de mosaïques 2x2 pour Inouïe Distribution</p>
        
        <h2>Endpoints:</h2>
        <ul>
            <li><strong>GET /health</strong> - Health check</li>
            <li><strong>POST /generate-mosaic</strong> - Générer une mosaïque</li>
        </ul>
        
        <h2>Utilisation:</h2>
        <pre style="background: #f4f4f4; padding: 15px; border-radius: 5px;">
POST /generate-mosaic
Content-Type: application/json

{
  "images": [
    "https://example.com/image1.jpg",
    "https://example.com/image2.jpg",
    "https://example.com/image3.jpg",
    "https://example.com/image4.jpg"
  ],
  "date_text": "Vendredi 23/11/2024"
}
        </pre>
        
        <h2>Réponse:</h2>
        <p>Fichier JPEG de 1080x1080 pixels</p>
        
        <hr>
        <p style="color: #666;">Made with ❤️ for Inouïe Distribution & Palmier Rouge</p>
    </body>
    </html>
    """

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
