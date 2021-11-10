# -*- coding: utf-8 -*-
"""
Created on Sun Apr 11 22:00:03 2021
"""

from flask import Flask, request, jsonify, make_response
from flask_httpauth import HTTPBasicAuth
import requests
import hashlib
import time

scraperport = 9000
#apikey =
#privatekey =

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == 'admin':
        return 'secret'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

@app.route('/Marvel', methods=['GET'])
@auth.login_required
def Marvel():
    story = request.args.get('story')
    ts = str(time.time())
    hashkey = hashlib.md5((ts + privatekey + apikey).encode()).hexdigest()
    r = requests.get(f'http://gateway.marvel.com/v1/public/stories/{story}?apikey={apikey}&hash={hashkey}&ts={ts}')
    response = r.json()
    return jsonify({'story text': response['data']['results'][0]['description']})

@app.route('/Weather/<city>', methods=['POST'])
@auth.login_required
def Weather(city):
    user = str(request.form.get('user'))
    pswd = str(request.form.get('pass'))
    city = city.lower() #ensures it is lowercase
    r = requests.get(f'http://localhost:9000/Weather/{city}', auth=(user, pswd))
    response = r.json()
    return jsonify({'location': response['name'], 'temperature': response['main']['temp'], 'pressure': response['main']['pressure'], 'humidity':response['main']['humidity']})

@app.route('/COVID/<state>', methods=['POST'])
@auth.login_required
def COVID(state):
    user = str(request.form.get('user'))
    pswd = str(request.form.get('pass'))
    r = requests.get(f'http://localhost:9000/COVID/{state}', auth=(user, pswd))
    response = r.json()
    return response

@app.route('/Update', methods=['POST'])
@auth.login_required
def Update():
    user = str(request.form.get('user'))
    pswd = str(request.form.get('pass'))
    new_user = str(request.form.get('new_user'))
    new_pass = str(request.form.get('new_pass'))
    r = requests.post(f'http://localhost:9000/Update?new_user={new_user}&new_pass={new_pass}', auth=(user, pswd))
    return r.text

if __name__ == '__main__':
    app.run(host='localhost', port=5000,debug=False)