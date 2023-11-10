

from flask import Response, jsonify, request
from sqlalchemy import (Engine, Insert, MetaData, Select, Table, Update,
                        create_engine, delete, update)
from sqlalchemy.sql import select

from config import SQL_ALCHEMY_URI

# Create a MetaData instance
metadata = MetaData(schema="system_config")


def create_postgres_engine():
    return create_engine(SQL_ALCHEMY_URI, isolation_level='AUTOCOMMIT', pool_size=10)


def execute_query(engine: Engine, obj: Select) -> dict:
    with engine.connect() as connection:
        result = connection.execute(obj)
        data = [dict(row) for row in result.mappings()]
    return data


def read_org_data() -> Response:
    try:
        engine = create_postgres_engine()
        table = Table('organization', metadata, autoload_with=engine)
        select_obj = select(table)
        data = execute_query(engine, select_obj)
        return jsonify({"message": data}), 200
    except Exception as err:
        print(err)
        return jsonify({"message": "Error while fetching the record"}), 400


def read_emp_data() -> Response:
    try:
        engine = create_postgres_engine()
        table = Table('employee', metadata, autoload_with=engine)
        select_obj = select(table).order_by(table.c.emp_name)
        data = execute_query(engine, select_obj)
        res_msg = jsonify({"message": data})
        res_code = 200
    except Exception as err: 
        res_msg = jsonify({"message": "Error while fetching the record"})
        res_code = 400
    finally:
        return res_msg, res_code        



def add_new_employee() -> Response:
    engine = create_postgres_engine()
    connection = engine.connect()
    try:
        emp_data = request.get_json()
        table = Table('employee', metadata, autoload_with=engine)
        employee_data = {
            "org_id": emp_data.get('org_id'),
            "emp_id": emp_data.get('emp_id'),
            "emp_name": emp_data.get('emp_name'),
            "date_of_joining": emp_data.get('date_of_joining'),
            "emp_role": emp_data.get('emp_role'),
            "emp_location": emp_data.get('emp_location'),
        }
        # Create an Insert object
        stmt = Insert(table).values(employee_data)

        # Execute the statement
        connection.execute(stmt)
        update_org_count(org_id=emp_data.get('org_id'), employees_count=emp_data.get('employees_count')+1)
        res_msg = jsonify({"message": "Employee added successfully"})
        res_code = 200
    except Exception as err:
        print(err) 
        connection.rollback()
        res_msg = jsonify({"message": "Error while adding a new employee"})
        res_code = 400
    finally: 
        connection.close()
        return res_msg, res_code
    


def update_org_count(org_id: str, employees_count: int) -> None:
    try:
        engine = create_postgres_engine()
        table = Table('organization', metadata, autoload_with=engine)
        stmt = (
            update(table).
            where(table.c.org_id == org_id).
            values(employees_count = employees_count)
        )
        
        with engine.connect() as connection: connection.execute(stmt)
    except Exception as err: print(err)



def update_emp_data() -> Response:
    engine = create_postgres_engine()
    connection = engine.connect()
    res_msg = None
    res_code = 200
    try:
        # Get the data from the request's JSON
        emp_data = request.get_json()
        table = Table('employee', metadata, autoload_with=engine)
        employee_data = {
            "org_id": emp_data.get('org_id'),
            "emp_id": emp_data.get('emp_id'),
            "emp_name": emp_data.get('emp_name'),
            "date_of_joining": emp_data.get('date_of_joining'),
            "emp_role": emp_data.get('emp_role'),
            "emp_location": emp_data.get('emp_location'),
        }
        stmt = (
            update(table).
            where(table.c.emp_id == emp_data.get('emp_id')).
            values(**employee_data)
        )
        
        with engine.connect() as connection:
            connection.execute(stmt)
        
        res_msg = jsonify({"message": "Employee updated successfully"})
    except Exception as err:
        print(err) 
        connection.rollback()
        res_msg = jsonify({"message": "Error while updating an employee"})
        res_code = 400
    finally: 
        connection.close()
        return res_msg, res_code


def delete_emp_data() -> Response:
    engine = create_postgres_engine()
    connection = engine.connect()
    res_msg = None
    res_code = 200
    try:
        # Get the data from the request's JSON
        emp_data = request.get_json()
        table = Table('employee', metadata, autoload_with=engine)
        stmt = delete(table).where(table.c.emp_id == emp_data.get('emp_id'))
        
        with engine.connect() as connection: connection.execute(stmt)
        update_org_count(org_id=emp_data.get('org_id'), employees_count=emp_data.get('employees_count')-1)
        res_msg = jsonify({"message": "Employee record deleted successfully"})
    except Exception as err:
        print(err) 
        connection.rollback()
        res_msg = jsonify({"message": "Error while deleting the employee record"})
        res_code = 400
    finally: 
        connection.close()
        return res_msg, res_code