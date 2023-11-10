# routes/main.py
from flask import jsonify, Blueprint

from config import *
import json
from services.helpers import *

edm_route = Blueprint('main', __name__)

@edm_route.route('/', methods=['GET'])
def main():
    return 'Welcome to Employee Data Management Service!'


@edm_route.route('/get_org_data', methods=['GET'])
def get_org_data():
    return read_org_data()


@edm_route.route('/get_employee_data', methods=['GET'])
def get_employee_data():
    return read_emp_data()

@edm_route.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    return add_new_employee()


@edm_route.route('/update_employee', methods=['GET', 'POST'])
def update_employee():
    return update_emp_data()


@edm_route.route('/remove_employee', methods=['POST'])
def remove_employee():
    return delete_emp_data()