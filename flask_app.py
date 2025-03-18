from flask import Flask, jsonify, request, render_template, url_for
import pandas as pd
import pickle
import numpy as np
import requests
from loguru import logger

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Charger le dataset
DATA_PATH = "data/microbes.csv"
df = pd.read_csv(DATA_PATH)

BACKEND_URL='https://fast-317097237537.europe-west1.run.app'

@app.route('/')
def home():
    return render_template('index.html')

# Prédiction via formulaire
@app.route('/predict', methods=['POST'])
def predict_microbe():
    # Prédiction avec le modèle
    r = requests.post(f'{BACKEND_URL}/predict', json=request.form)
    
    # Chercher le microbe associé et son image
    predicted_microbe = r.json()['class_predicted'][0]
    microbe_data = df[df["microorganisms"] == predicted_microbe].iloc[0]

    
    # Récupérer le chemin de l'image et générer l'URL
    image_filename = microbe_data['microorganisms']  # Nom du fichier image
    image_path = url_for('static', filename='img/' + image_filename + '.png')
    
    logger.info(f'aaaaaaaaaaaaaaa {image_path}')
    
    # Retourner la page de résultat avec le microbe et l'image
    return render_template('results.html', microbe=predicted_microbe, image_path=image_path)
    

if __name__ == '__main__':
    app.run(debug=True)
    
    