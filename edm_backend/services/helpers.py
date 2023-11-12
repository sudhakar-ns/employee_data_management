

import csv
import io

import pandas as pd
from flask import Response, jsonify, request
from pandas import DataFrame
from sqlalchemy import (Engine, Insert, MetaData, Select, Table, create_engine,
                        delete, text, update)
from sqlalchemy.sql import select

from config import SQL_ALCHEMY_URI

# Create a MetaData instance
metadata = MetaData(schema="system_config")


def create_postgres_engine() -> Engine:
    return create_engine(SQL_ALCHEMY_URI, pool_size=10)


def execute_query(engine: Engine, obj: Select) -> dict:
    with engine.connect() as connection:
        result = connection.execute(obj)
        data = [dict(row) for row in result.mappings()]
    return data


def validate_columns(origin: list, to_validate: list) -> bool | tuple:
    try:
        for x, y in zip(origin, to_validate):
            if x != y: return False, "Columns don't match"
        return True
    except Exception as err: return False, err


def import_emp_data() -> Response:
    engine = create_postgres_engine()
    connection = engine.connect()
    res_msg = None
    res_code = 200
    try:
        columns_to_validate = ['org_id', 'emp_id', 'emp_name', 'date_of_joining', 'emp_role', 'emp_location']
        if 'file' in request.files:
            uploaded_file = request.files['file']
            df: DataFrame = None
            if uploaded_file.filename.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
                header = df.columns.to_list()
            elif uploaded_file.filename.endswith('.xls') or uploaded_file.filename.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file)
                header = df.columns.to_list()
            is_valid = validate_columns(columns_to_validate, header)
            _type = str(type(is_valid))
            if 'tuple' in _type: return jsonify({"message": is_valid[1]}), 400
            connection.execute(text("TRUNCATE TABLE system_config.employee;"))
            columns = ", ".join(columns_to_validate)
            table_values = df.values.tolist()
            for record in table_values:
                value = str(record)[1: len(str(record))-1]
                connection.execute(text(f"INSERT INTO system_config.employee ({columns}) VALUES ({value});"))
            connection.commit()
            res_msg = jsonify({"message": 'File Imported Successfully'})
    except Exception as err: 
        connection.rollback()
        res_msg = jsonify({"message": str(err)})
        res_code = 400
    finally:
        connection.close()
        return res_msg, res_code


def export_emp_data() -> Response:
    try:
        engine = create_postgres_engine()
        table = Table('employee', metadata, autoload_with=engine)
        select_obj = select(table)
        data = execute_query(engine, select_obj)
        # Create an in-memory text stream
        si = io.StringIO()
        fieldnames = data[0].keys()  # Get field names from first row
        writer = csv.DictWriter(si, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(data)

        # Get the CSV data
        output = si.getvalue()

        # Send the CSV file as a response
        return Response(
            output,
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment;filename=export.csv"}
        )
    except Exception as err:
        print(err)
        return jsonify({"message": "Error while fetching the record"}), 400


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
        res_msg = jsonify({"message": str(err)})
        res_code = 400
    finally:
        return res_msg, res_code        


def add_new_employee() -> Response:
    engine = create_postgres_engine()
    connection = engine.connect()
    res_msg = None
    res_code = 200
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
        connection.commit()
        res_msg = jsonify({"message": "Employee added successfully"})
    except Exception as err:
        connection.rollback()
        res_msg = jsonify({"message": str(err)})
        res_code = 400
    finally: 
        connection.close()
        return res_msg, res_code


def update_org_count(org_id: str, employees_count: int) -> None:
    engine = create_postgres_engine()
    connection = engine.connect()
    try:
        table = Table('organization', metadata, autoload_with=engine)
        stmt = (
            update(table).
            where(table.c.org_id == org_id).
            values(employees_count = employees_count)
        )
        connection.execute(stmt)
        connection.commit()
    except Exception as err:
        print(err) 
        connection.rollback()



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
        connection.commit()
        res_msg = jsonify({"message": "Employee record deleted successfully"})
    except Exception as err:
        print(err) 
        connection.rollback()
        res_msg = jsonify({"message": "Error while deleting the employee record"})
        res_code = 400
    finally: 
        connection.close()
        return res_msg, res_code