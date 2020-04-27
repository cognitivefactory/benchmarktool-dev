from flask import render_template, request, make_response, jsonify
import json
from app import app
from train_dataset import TrainDataset

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

@app.route('/progression')
def progression():
    return render_template("progression.html")


@app.route('/analyse', methods=['POST'])
def analyse():
    status = 100 # = fail
    try:
        content = request.files['file']
        try: 
            content = content.read()
            try:
                file = json.loads(content)
                train_data = TrainDataset()
                data = train_data.filter_json(file)
                if not file : 
                    message = "incorrect data structure (1)"
                    return make_response(jsonify({"message" : message}), status)

                if not train_data.is_correct(data) :
                    message = "incorrect data structure (2)"
                    return make_response(jsonify({"message" : message}), status)

                if not train_data.metadata(data) :
                    message = "failed to create metadata"
                    return make_response(jsonify({"message" : message}), status)

                message = print(train_data)
                return make_response(jsonify({"message" : message}), 200) #200 = success

            except:
                message = "JSON not correct"
                return make_response(jsonify({"message" : message}), status)
        except:
            message = "cannot read the file"
            return make_response(jsonify({"message" : message}), status)
    except:
        message = "cannot open the file"
        return make_response(jsonify({"message" : message}), status)