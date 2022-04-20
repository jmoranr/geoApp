import os
from flask import Flask, jsonify
import connect_db
import re
from datetime import datetime

app = Flask(__name__)

def conn():
    conndb = connect_db.connect()
    if conndb:
        return conndb
    else:
        return False



@app.route('/', methods=['GET'])
def welcome():
    if conn():
        return jsonify({'status': 'Database connection successfully'})
    else:
        return jsonify({'status': 'Database connection error'})


@app.route('/<inputPoint>/<inputDate>/', methods=['GET'])
def point(inputPoint, inputDate):

    # Date validation
    wrongDateErr = "Request bad formed. Please try to enter a date that follows this pattern: '2015-03-16'"
    datePattern = re.compile("^([0-9]+-?)+$")
    if not datePattern.match(inputDate):
        return wrongDateErr
    year, month, day = inputDate.split('-')
    isValidDate = True
    try:
        datetime(int(year), int(month), int(day))
    except ValueError:
        isValidDate = False
    if not isValidDate:
        return wrongDateErr

    # Point validation
    wrongPointErr = "Request bad formed. Please try to enter a geometry that follows this pattern: '-3.83 40.39'"
    pointPattern = re.compile("^(-?[0-9]+.?[0-9]+ -?[0-9]+.?[0-9]+)+$")
    if not pointPattern.match(inputPoint):
        return wrongPointErr
    else:
        return jsonify({'result': connect_db.elem1(conn(), inputPoint, inputDate)})


app.run(host='0.0.0.0', port=os.getenv('PORT'))