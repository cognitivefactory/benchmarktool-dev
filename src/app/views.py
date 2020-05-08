
from flask import render_template, request, make_response, jsonify
from app import app
from flask_socketio import SocketIO

import json
from dataset import Dataset, TrainData
from model import Model, SpacyModel

spacy_model = None
train_data  = None
socketio    = SocketIO(app, async_mode=None, logger=True, engineio_logger=True)


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
    global spacy_model
    if(spacy_model== None):
        return render_template("results.html", score = None, visuals = None)
    if (spacy_model.is_ready== False):
        return render_template("results.html", score = None, visuals = None)    
    
    test_text = [("On dit qu\'un cheval est calme",{
            'entities': [(13, 19, 'ANIMAL')]
            }),
            ("Un cheval endormi n\'est pas nécessairement un cheval calme",{
             'entities': [(3, 9, 'ANIMAL'),(46,51, 'ANIMAL')]   
            }),
            ("souhaitez vous apprendre à monter à cheval?",{
             'entities' : [(36,41,'ANIMAL')]
            }),
            ("Pour moi les chevaux sont les meilleurs animaux après les chats",{
             'entities' : [(13,20,'ANIMAL'),(58,63, 'ANIMAL')]
            })
           ]
    score=spacy_model.test(test_text)  
    visuals=spacy_model.get_visuals()
    for key, value in score.items() :
        if (key == "ents_per_type"):
            score=value
            return render_template("results.html", score = score, visuals = visuals) 

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

                print(train_data)
                print(train_data.get_labels())
                
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

'''
To do :
in JS : 
add eventlistener to know when the user wants to train a model
with socketio, send information as a json 

In Flask :
@socketio.on('train_model')
    - handle custom event to retrieve
    information concerning the model (which library? ...)
    - inform the client that the training has begun 
    - train model using train dataset (global var: train)
    - when it's done socketio.emit
    
in JS : create a notification popup when we receive a message from socketio
'''


@socketio.on('start_training')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    name = str(json)
    global train_data

    if not train_data :
        return socketio.emit('training', 0)

    socketio.emit('training', 1)
    global spacy_model
    spacy_model = SpacyModel(name,train_data,15, None, None)
    spacy_model.convert_format()
    spacy_model.train()
    socketio.emit('training_done', 1)


    """TODO : train the model here"""
