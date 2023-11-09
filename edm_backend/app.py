import os

from flask import Flask
from dotenv import load_dotenv
from flask_cors import CORS

from controllers.controller import automate_route

app = Flask(__name__)

# Register the Blueprints
app.register_blueprint(automate_route)


if __name__ == '__main__':
    CORS(app)
    app.run(host="0.0.0.0", port = os.environ.get('APP_PORT'), debug = True)