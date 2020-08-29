import os
from flask import render_template, request, make_response, jsonify
from app import app
from flask_socketio import SocketIO

import json
from dataset import *
from model import *

spacy_model = None
train_data  = None
socketio    = SocketIO(app, async_mode=None, logger=True, engineio_logger=True)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/data_train')
def data_train():
    """ parcours des fichiers de métadonnées"""
    path = "datasets"
    files = []
    try:
        metafiles = os.listdir(path)
        for metafile in metafiles:
            try:
                with open(path + "/" + metafile) as json_file:
                    data = json.load(json_file)
                    labels = [None]*3
                    size = len(data["labels"])
                    for i in range(3):
                        if size <= i:
                            break
                        else:
                            labels[i] = (list(data["labels"])[i])
                    data["labels"] = labels

                    files.append(data)

            except:
                print("file doesn't exist")

    except:
        print("directory doesn't exist")
    
    return render_template("data_train.html", files = files)

@app.route('/models')
def models():
    """ parcours des fichiers de métadonnées"""
    path = "libraries"
    files = []
    try:
        metafiles = os.listdir(path)
        for metafile in metafiles:
            try:
                with open(path + "/" + metafile) as json_file:
                    data = json.load(json_file)

                    data["options"] = list(map(list, data["options"].items()))
                    files.append(data)

            except:
                print("cannot read the metafile")    
    except:
        print("directory doesn't exist")
    
    return render_template("models.html", files = files)

@app.route('/results')
def results():
    return render_template("results.html")

@app.route('/processing', methods=['POST'])
def processing():
    status = 100 # = fail
    try:
        content = request.files['file']
        try: 
            #TODO : récupérer le nom du fichier pour nommer l'objet dataset
            content = content.read()
            try:
                content = json.loads(content)
                global test_data
                test_data = Dataset("test_data")

                if not test_data.filter_json(content) : 
                    message = "incorrect test data structure (1)"
                    print(message)
                    return make_response(jsonify({"message" : message}), status)

                if not test_data.is_correct() :
                    message = "incorrect test data structure (2)"
                    print(message)
                    return make_response(jsonify({"message" : message}), status)
                
                
                
                #success
                global spacy_model
                if(spacy_model== None):
                    return render_template("results.html", score = None, visuals = None)
                if (spacy_model.is_ready== False):
                    return render_template("results.html", score = None, visuals = None)    
                
                

                score=spacy_model.test(test_data)  
                visuals=spacy_model.get_visuals()
                for key, value in score.items() :
                    if (key == "ents_per_type"):
                        score=value
                        
                return make_response(jsonify({"message" : "JSON received"}), 200)
                """
                return make_response(jsonify({"message" : "JSON received"}), 200), render_template("results.html", score = score, visuals = visuals) 
                """

            except:
                message = "JSON not correct"
                print(message)
                return make_response(jsonify({"message" : message}), status)
        except:
            message = "cannot read the file"
            print(message)
            return make_response(jsonify({"message" : message}), status)
    except:
        message = "cannot open the file"
        print(message)
        return make_response(jsonify({"message" : message}), status)


@app.route('/progression')
def progression():
    return render_template("progression.html")


@app.route('/add_train', methods=['POST'])
def add_train():
    status = 100 # = fail
    try:
        content = request.files['file']
        try: 
            content = content.read()
            try:
                content = json.loads(content)
                content = content
                global train_data
                train_data = TrainData("train_data")

                if not train_data.filter_json(content) : 
                    message = "incorrect data structure (1)"
                    print(message)
                    return make_response(jsonify({"message" : message}), status)

                if not train_data.is_correct() :
                    message = "incorrect data structure (2)"
                    print(message)
                    return make_response(jsonify({"message" : message}), status)

                if not train_data.metadata() :
                    message = "failed to create metadata"
                    print(message)
                    return make_response(jsonify({"message" : message}), status)
                
                if not train_data.create_metafile():
                    message = "failed to create metafile"
                    print(message)
                    return make_response(jsonify({"message" : message}), status)

                return make_response(jsonify({"message" : "JSON received"}), 200) #200 = success

            except:
                message = "JSON not correct"
                print(message)
                return make_response(jsonify({"message" : message}), status)
        except:
            message = "cannot read the file"
            print(message)
            return make_response(jsonify({"message" : message}), status)
    except:
        message = "cannot open the file"
        print(message)
        return make_response(jsonify({"message" : message}), status)



@socketio.on('start_training')
def handle_my_custom_event(data, methods=['POST']):
    print(data)
    print(data["options"]["library"])

    """
    name = str(json)
    global train_data

    if not train_data :
        return socketio.emit('training', 0)

    try:
        global spacy_model
        spacy_model = SpacyModel(model_format = "spacy_format",model_name = name,training_data = train_data, nb_iter=15, out_dir= None, model= None)
        
        socketio.emit('training', 1)
        spacy_model.train()
        socketio.emit('training_done', 1)

        
        global flair_model
        flair_model = FlairModel(model_format="bio_format", model_name=name, training_data=train_data, nb_iter=2)
        socketio.emit('training', 1)
        flair_model.train()
        
    except:
        return socketio.emit('model', 0)
    """