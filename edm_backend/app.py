import os

from flask import Flask
from dotenv import load_dotenv
from flask_cors import CORS

from controllers.controller import edm_route
from services.helpers import read_org_data

app = Flask(__name__)

# Register the Blueprints
app.register_blueprint(edm_route)


if __name__ == '__main__':
    CORS(app)
    app.run(host="0.0.0.0", port = os.environ.get('APP_PORT'), debug = True)