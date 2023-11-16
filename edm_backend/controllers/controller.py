# routes/main.py
from flask import Blueprint

from config import *
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


@edm_route.route('/insert_employee_data', methods=['POST'])
def insert_employee_data():
    return import_emp_data()


@edm_route.route('/extract_employee_data', methods=['GET'])
def extract_employee_data():
    return export_emp_data()