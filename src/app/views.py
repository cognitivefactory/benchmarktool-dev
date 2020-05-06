from flask import render_template, request, make_response, jsonify
from app import app
from flask_socketio import SocketIO

import json
from dataset import Dataset

train_data = None
socketio = SocketIO(app, async_mode=None, logger=True, engineio_logger=True)

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
                train_data = Dataset()

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

                message = print(train_data)
                print(message)
                
                return make_response(jsonify({"message" : message}), 200) #200 = success

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

    return socketio.emit('training', 1)
    
    """TODO : train the model here"""
