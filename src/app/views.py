import os
from flask import render_template, request, make_response, jsonify
from app import server
from flask_socketio import SocketIO
import csv
import pandas as pd
import json
from dataset import *
from model import *

"""global variables"""
models_list = []
train_data  = None
test_data  = None
socketio    = SocketIO(server, async_mode=None, logger=True, engineio_logger=True)



@server.route('/')
def index():
    return render_template("index.html")

@server.route('/data_train')
def data_train():
    """ parsing of the metadata files"""
    path = "datasets"
    files = []
    try:
        metafiles = os.listdir(path)
        print(metafiles)
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

@server.route('/models')
def models():
    """ parsing of the metadata files"""
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

@server.route('/results')
def results():
    global test_data
    global models_list

    if (test_data==None or models_list == [] ):
        return render_template("results.html",score = None, visuals = None)
    else:
        with open('./src/tmp/results.csv', mode='a') as csv_file:
            for model in models_list:
                #is_ready = 1 : model has been trained and is ready to be tested
                if (model.is_ready== 1):
                    scores = model.test(test_data)
                    model.write_data(scores,csv_file)
                    #is_ready = 2 : model has already been tested
                    model.is_ready = 2
        return render_template("dash.html", dash_url = '/dash/')

            

@server.route('/processing', methods=['POST'])
def processing():
    status = 100 # = fail
    try:
        content = request.files['file']
        # get the file name without its extension
        filename = (content.filename).replace(".json", "")

        content = content.read().decode('utf-8')
        content = json.loads(content)

        tmp_dataset = Dataset("test_data")

        if not tmp_dataset.filter_json(content) : 
            message = "incorrect test data structure (1)"
            print(message)
            return make_response(jsonify({"message" : message}), status)

        if not tmp_dataset.is_correct() :
            message = "incorrect test data structure (2)"
            print(message)
            return make_response(jsonify({"message" : message}), status)

        global test_data
        test_data = Dataset()
        test_data.copy_object(tmp_dataset)

        status = 200
        return make_response(jsonify({"message" : "JSON received"}), status)

    except:
        return make_response(jsonify({"message" : "cannot open the file"}), status)


@server.route('/progression')
def progression():
    return render_template("progression.html")


@server.route('/add_train', methods=['POST'])
def add_train():
    status = 100 # = fail
    try:
        content = request.files['file']
        # get the file name without its extension
        filename = (content.filename).replace(".json", "")
        
        content = content.read().decode('utf-8')
        content = json.loads(content)

        global train_data
        train_data = TrainData(filename)
            
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
        
        # save metafile
        train_data.create_metafile()
        status = 200
        return make_response(jsonify({"message" : "JSON received"}), status) #200 = success

    except:
        return make_response(jsonify({"message" : "cannot open the file"}), status)



@socketio.on('select_train_data')
def select_train_data(filename, methods=['POST']):
    global train_data

    try:
        with open("./datasets/" + filename['filename'], 'r') as file:
            train_data = TrainData()
            train_data.from_metadata(json.load(file))
        
            socketio.emit('selected_train_data', 1)

    except:
        socketio.emit('selected_train_data', 0)




@socketio.on('start_training')
def start_training(data, methods=['POST']):
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
