from flask import Flask, jsonify, request, render_template, url_for
import pandas as pd
import pickle
import numpy as np
import requests
from loguru import logger

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

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
    
    # Récupérer le chemin de l'image et générer l'URL
    image_path = url_for('static', filename='img/' + predicted_microbe + '.png')
        
    # Retourner la page de résultat avec le microbe et l'image
    return render_template('results.html', microbe=predicted_microbe, image_path=image_path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
    
    