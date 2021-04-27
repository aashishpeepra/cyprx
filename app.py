import os
import flask
from index4 import rounder
app=flask.Flask(__name__)
app_settings = os.getenv(
    'APP_SETTINGS'
)
app.config.from_object(app_settings)

@app.route("/",methods=["GET"])
def home():
    return str(rounder(1.23))