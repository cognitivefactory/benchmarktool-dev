import os
from flask import render_template, request, make_response, jsonify
from app import app
from flask_socketio import SocketIO

import json
from dataset import *
from model import *

models_list = []
train_data  = None
test_data  = None
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

                    # only display the 3 most frequent labels
                    # stored in a list to be displayed using Jinja
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

                    # convert dictionnary to list
                    # format : [['key'], values]
                    data["options"] = list(map(list, data["options"].items()))
                    files.append(data)

            except:
                print("cannot read the metafile")    
    except:
        print("directory doesn't exist")
    
    return render_template("models.html", files = files)

@app.route('/results')
def results():
    global test_data
    global models_list
    print(models_list)
    print(f"jeu de test = {test_data}")

    if (test_data==None or models_list == [] ):
        return render_template("results.html",score = None, visuals = None)
    else:
        print(models_list)
        score = {}
        for model in models_list:
            if (model.is_ready== True):
                scores=model.test(test_data)  
                if(model.model_format=="spacy_format"):
                    for key, value in scores.items() :
                        if (key == "ents_per_type"):
                            scores=value
                            score[model.model_name] = scores
                if(model.model_format=="bio_format"):
                    score[model.model_name] = scores
        print(score)
        #return render_template("results.html", score = score, visuals = visuals)
        return render_template("results.html", score = score, visuals = None)
    #return render_template("results.html",score = None, visuals = None)

            

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
                
                
                
             
                        
                return make_response(jsonify({"message" : "JSON received"}), 200)

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
    global models_list
    global train_data

    library = data["options"]["library"]

    # only keep parameters
    del data["options"]["library"]
        
    if not train_data :
        return socketio.emit('training', 0)
    
    try:
        class_model = library.capitalize() + "Model"

        model = eval(class_model + "(parameters=" + str(data["options"]) +")")
        model.add_training_data(train_data)
        models_list.append(model)

        socketio.emit("training", 1)
        model.train()
        socketio.emit('training_done', 1)

    except: 
        return socketio.emit('model', 0)