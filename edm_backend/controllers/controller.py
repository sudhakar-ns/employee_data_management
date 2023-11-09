# routes/main.py
from flask import Blueprint

from config import *
from services.lol import poc
from services.web_automation import WebAutomation

automate_route = Blueprint('main', __name__)

@automate_route.route('/', methods=['GET'])
def main():
    return 'Welcome to Automation Service!'


@automate_route.route('/automate_job', methods=['GET'])
def automate_job():
    return poc()