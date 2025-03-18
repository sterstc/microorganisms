import pickle
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET'])
def california_index(): 
    # TODO : complete function
    ...


@app.route('/predict/', methods=['POST'])
def result():
    # TODO : complete function
    ...

if __name__ == '__main__':
    app.debug = True
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True)
