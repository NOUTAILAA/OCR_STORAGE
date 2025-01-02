import unittest
import sys
import os

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db, ExtractionData

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Base de données en mémoire pour les tests
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_store_data(self):
        payload = {
            "prenom": "NOUTAILA",
            "nom": "BENZALA",
            "ddn": "2003-01-19",
            "ville": "Marrakech",
            "numcin": "EE699601"
        }
        response = self.app.post('/store_data', json=payload)
        self.assertEqual(response.status_code, 201)
        
        # Utilisation de get_json() pour éviter les problèmes d'encodage
        response_data = response.get_json()
        self.assertEqual(response_data['message'], "Données enregistrées avec succès")

    def test_store_data_missing_fields(self):
        payload = {
            "prenom": "Ali"
        }
        response = self.app.post('/store_data', json=payload)
        self.assertEqual(response.status_code, 201)
        
        response_data = response.get_json()
        self.assertEqual(response_data['message'], "Données enregistrées avec succès")

    def test_store_data_no_payload(self):
        response = self.app.post('/store_data', json={})
        self.assertEqual(response.status_code, 400)
        
        response_data = response.get_json()
        self.assertEqual(response_data['error'], "Aucune donnée reçue")

if __name__ == '__main__':
    unittest.main()
