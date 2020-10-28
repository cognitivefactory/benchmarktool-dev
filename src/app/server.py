from flask import Flask, render_template

server = Flask(__name__, instance_relative_config=True)


# Load the views
from app import views

server.config.from_object('config')