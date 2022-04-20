import os
from flask import Flask, jsonify
import model
import re
from datetime import datetime

app = Flask(__name__)


# Error messages and pattern matchings

wrongPointErr = "Request bad formed. Please try to enter a geometry that follows this pattern: '-3.83 40.39' (long lat)"
pointPattern = re.compile("^(-?[0-9]+.?[0-9]+ -?[0-9]+.?[0-9]+)+$")
wrongDateErr = "Request bad formed. Please try to enter a date that follows this pattern: '2015-03-16' (yyyy-mm-dd)"
datePattern = re.compile("^([0-9]+-?)+$")


# Global actions

def conn():
    conndb = model.connect()
    if conndb:
        return conndb
    else:
        return False

def pointValidation(inputPoint):
    if not pointPattern.match(inputPoint):
        return False
    else:
        return True

def dateValidation(inputDate):
    if not datePattern.match(inputDate):
        return False
    year, month, day = inputDate.split('-')
    isValidDate = True
    try:
        datetime(int(year), int(month), int(day))
    except ValueError:
        isValidDate = False
    if not isValidDate:
        return False
    else:
        return True


# Entrypoints routing

@app.route('/', methods=['GET'])
def welcome():
    if conn():
        return jsonify({'status': 'Database connection successfully'})
    else:
        return jsonify({'status': 'Database connection error'})

@app.route('/<inputPoint>/<inputDate>/', methods=['GET'])
def dateData(inputPoint, inputDate):
    if pointValidation(inputPoint):
        if dateValidation(inputDate):
            return jsonify({
                'title': 'TURNOVER BY AGE AND GENDER',
                'data': model.elem1(conn(), inputPoint, inputDate)
            })
        else:
            return wrongDateErr
    else:
        return wrongPointErr
    
@app.route('/<inputPoint>/ts<inputDate>/', methods=['GET'])
def timeSeries(inputPoint, inputDate):
    if pointValidation(inputPoint):
        startDate, endDate = inputDate.split()
        if dateValidation(startDate):
            if dateValidation(endDate):
                return jsonify({
                    'title': 'TIME SERIES',
                    'data': model.timeSeries(conn(), inputPoint, startDate, endDate)
                })
            else:
                return wrongDateErr
        else:
            return wrongDateErr
    else:
        return wrongPointErr

@app.route('/madrid/<inputDate>/', methods=['GET'])
def madrid(inputDate):
    if dateValidation(inputDate):
        return jsonify({
            'title': 'TOTAL COMUNIDAD DE MADRID',
            'data': model.madrid(conn(), inputDate)
        })
    else:
        return wrongDateErr


app.run(host='0.0.0.0', port=os.getenv('PORT'))