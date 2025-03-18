from flask import Flask, jsonify, request, render_template, url_for
import pandas as pd
import pickle
import numpy as np
import requests
from loguru import logger
import os
import yaml

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

BACKEND_URL='https://fast-317097237537.europe-west1.run.app'

with open('static/microorganism.yaml', 'r') as file:
    microorganism_data = yaml.safe_load(file)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict_microbe():
    
    r = requests.post(f'{BACKEND_URL}/predict', json=request.form)
    
    predicted_microbe = r.json()['class_predicted'][0]
    
    image_path = url_for('static', filename='img/' + predicted_microbe + '.png')
    
    microbe_info = microorganism_data['microorganisms'].get(predicted_microbe, {})
    
    return render_template('results.html', 
                         microbe=predicted_microbe, 
                         image_path=image_path,
                         description=microbe_info.get('description', ''),
                         type=microbe_info.get('type', ''),
                         habitat=microbe_info.get('habitat', ''))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
    
    