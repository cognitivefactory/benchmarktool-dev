from flask import render_template, request, jsonify
import json
from app import app

@app.route('/')
def index():
    json = request.get_json()
    return render_template("index.html")

@app.route('/data_train')
def data_train():
    return render_template("data_train.html")

@app.route('/models')
def models():
    return render_template("models.html")

@app.route('/results')
def results():
    return render_template("results.html")

@app.route('/analyse', methods=['POST'])
def analyse():
    data = request.files['file']
    res = data.read()
    res = json.loads(res)
    print(res)
    return render_template("data_train.html")