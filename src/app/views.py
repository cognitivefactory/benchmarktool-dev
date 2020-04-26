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
    print(request.headers)
    status = 100 # = fail
    message = ""
    try:
        content = request.files['file']
        try: 
            content = content.read()
            try:
                data = json.loads(content)
                status = 200 # = success
                message = data
                d = Dataset()
                if not d.isCorrect(data):
                    del d
                    status = 100 # = fail
                    print("data structure is incorrect\n")
            except:
                print("JSON not correct\n")
        except:
            print("cannot read the file\n")
    except:
        print("cannot open the file\n")

    print("-----------\n")
    print(message)
    print("\n")
    print(status)
    return make_response(jsonify({"message" : message}), status)
    