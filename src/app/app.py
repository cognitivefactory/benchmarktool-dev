from flask import Flask, render_template

app = Flask(__name__, instance_relative_config=True)


# Load the views
from app import views

app.config.from_object('config')