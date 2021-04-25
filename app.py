import os
import flask

app=flask.Flask(__name__)
app_settings = os.getenv(
    'APP_SETTINGS'
)
app.config.from_object(app_settings)

@app.route("/",methods=["GET"])
def home():
    return json({"header":"Starting the server"})