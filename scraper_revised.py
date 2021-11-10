# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 18:01:41 2021
"""

from flask import Flask, request, jsonify, make_response
from flask_httpauth import HTTPBasicAuth
import requests
import pymongo
from bs4 import BeautifulSoup

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
auth = HTTPBasicAuth()

# MongoDB instance
db = pymongo.MongoClient().scraper

#api keys
#weatherkey = 


@auth.get_password
def get_password(username):
    if username == 'admin':
        return 'secret'
    elif username:
        pswd = db.utilization.find_one({'username': {'$in': [f'{username}']}})
        pswd = pswd['password']
        return pswd
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

@app.route('/Weather/<city>', methods=['GET'])
@auth.login_required
def Weather(city):
    r = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weatherkey}')
    response = r.json()
    return response

@app.route('/COVID/<state>', methods=['GET'])
@auth.login_required
def COVID(state):
    state = state.lower() #ensures the input is lowercase
    r = requests.get(f'http://worldometers.info/coronavirus/usa/{state}/')
    soup = BeautifulSoup(r.content, 'html.parser')
    stats = soup.find_all(id='maincounter-wrap')
    for stat in stats:
        if 'Cases' in stat.text.strip():
            cases = stat.find(class_='maincounter-number').text.strip()
        elif 'Deaths' in stat.text.strip():
            deaths = stat.find(class_='maincounter-number').text.strip()
        elif 'Recovered' in stat.text.strip():
            recovered = stat.find(class_='maincounter-number').text.strip()
    return jsonify({'state': state, 'total cases': cases, 'total deaths': deaths, 'total recovered':recovered})

@app.route('/Update', methods=['POST'])
@auth.login_required
def Update():
    new_user = str(request.args.get('new_user'))
    new_pass = str(request.args.get('new_pass'))
    if new_user and new_pass:
        db.utilization.insert_one({'username': new_user, 'password': new_pass})
        return 'success'
    return 'failure'

if __name__ == '__main__':
    app.run(host='localhost', port=9000,debug=False)