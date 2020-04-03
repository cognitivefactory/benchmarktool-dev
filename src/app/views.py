from flask import render_template

from app import app

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