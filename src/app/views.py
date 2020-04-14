from flask import render_template, request, make_response, jsonify
import json
from app import app
from dataset import Dataset

@app.route('/')
def index():
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
    print("----\n")
    print(request.headers)
    data = request.files['file']
    res = data.read()
    res = json.loads(res)
    d = Dataset()
    if not d.isCorrect(res):
        return make_response(jsonify({"message " ": file does not correspond to the standard"}), 100)
    print(d)
    return make_response(jsonify({"message": ":JSON received"}), 200)