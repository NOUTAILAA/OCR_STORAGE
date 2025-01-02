from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import json

app = Flask(__name__)
CORS(app)

# Configuration de la base de données MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/extraction_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modèle pour stocker les données extraites sous forme de JSON
class ExtractionData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    extracted_text = db.Column(db.JSON, nullable=False)  # JSON au lieu de texte simple
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, extracted_text):
        self.extracted_text = extracted_text


# Route pour stocker les données extraites
@app.route('/store_data', methods=['POST'])
def store_data():
    data = request.json
    if not data:
        return jsonify({"error": "Aucune donnée reçue"}), 400

    try:
        extracted_entry = ExtractionData(extracted_text=json.dumps(data))  # Stocker en JSON
        db.session.add(extracted_entry)
        db.session.commit()
        return jsonify({"message": "Données enregistrées avec succès"}), 201
    except Exception as e:
        print(f"[ERROR] Erreur lors de l'insertion : {str(e)}")  # Log précis
        db.session.rollback()
        return jsonify({"error": f"Erreur lors de l'insertion en base : {str(e)}"}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crée la table si elle n'existe pas
    app.run(host='0.0.0.0', port=5002, debug=True)
