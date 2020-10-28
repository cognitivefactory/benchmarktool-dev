# server/__init__.py

from flask import Flask
from flask_socketio import SocketIO
from flaskext.markdown import Markdown
from app import dash_server
import pandas as pd

# Initialize the server
server = Flask(__name__, instance_relative_config=True)
Markdown(server)
server.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(server)


# Load the views
from app import views


# Load the config file
server.config.from_object('config')


# Load Dash
server = dash_server.create_Dash(server)




