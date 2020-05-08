# app/__init__.py

from flask import Flask
from flask_socketio import SocketIO
from flaskext.markdown import Markdown

# Initialize the app
app = Flask(__name__, instance_relative_config=True)
Markdown(app)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)

# Load the views
from app import views

# Load the config file
app.config.from_object('config')