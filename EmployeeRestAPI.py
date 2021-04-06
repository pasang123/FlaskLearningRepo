from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
import json
import sqlite3
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
filehandler = logging.FileHandler("test.log")
logger.addHandler(filehandler)
formatter = logging.Formatter("%(asctime)s:%(name)s:%(message)s")
filehandler.setFormatter(formatter)
filehandler.setLevel(logging.ERROR)
StreamHandler = logging.StreamHandler()
logger.addHandler(StreamHandler)
StreamHandler.setFormatter(formatter)
# logging.basicConfig(filename="test.log", level=logging.DEBUG, format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")

app = Flask(__name__)
api = Api(app)


@app.route('/')
def home():
    return {'data': 'Welcome Home'}


class Employees(Resource):
    def get(self):
        conn = sqlite3.connect('chinook.db') # connect to database
        cur = conn.cursor()
        query = cur.execute("select * from employees") # This line performs query and returns json result
        return {'employees': [i[0] for i in query.fetchall()]} # Fetches first column that is Employee ID


class Tracks(Resource):
    def get(self):
        conn = sqlite3.connect('chinook.db')
        cur = conn.cursor()
        query = cur.execute("select trackid, name, composer, unitprice from tracks;")
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        final_result = json.load(result)
        return final_result


class Employees_Name(Resource):
    def get(self, employee_id):
        conn = sqlite3.connect('chinook.db')
        cur = conn.cursor()
        query = cur.execute("select * from employees where EmployeeId =%d "  %int(employee_id))
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        final_result = json.load(result)
        return final_result
        

api.add_resource(Employees, '/employees') # Route_1
api.add_resource(Tracks, '/tracks') # Route_2
api.add_resource(Employees_Name, '/employees/<employee_id>') # Route_3


if __name__ == '__main__':
    # logger.debug("Debug")
    # logger.info("InfO")
    # logger.warning("WarninG")
    # logger.error("Error")
    # logger.critical("Critical")

    try:
        y = 2/0
    except ZeroDivisionError:
        logger.exception("Zero Division Error")
    app.run(port=5002)