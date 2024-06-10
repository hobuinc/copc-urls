import logging

import requests, os
from flask import Flask, redirect, jsonify
from flask import request

from flask_cors import cross_origin

from constants import WEBHOOK, NOT_FOUND_URL, SECRET_KEY
from models import ShortURL
from zappa.asynchronous import task

import uuid
import hashlib
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

MAIN = False

whitelist = ['https://viewer.copc.io', 'https://eptium.com','http://localhost','https://moonlidar.com']
app = Flask(__name__, static_url_path='/no_static')
# cors = CORS(app, resources={r"*": {"origins": origin}})


#@app.after_request
#def after_request(response):
#    response.headers.add('Access-Control-Allow-Origin', origin)
#    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
#    return response

def create_short_url(state):
    hash = hashlib.sha256(state.encode('utf-8')).hexdigest()
    return hash



@app.route('/', methods=['POST'])
@cross_origin(whitelist)
def create_url():
    state = request.json['state']
    url = create_short_url(state)
    ShortURL(url=url, state=state).save()
    return jsonify(url=url, success=True), 200


@app.route('/<path:path>', methods=['GET', 'DELETE'])
@cross_origin(whitelist)
def redirect_url(path):
    try:
        short = ShortURL.get(path)
        if request.method == 'DELETE':
            ShortURL.delete(path)
            return jsonify(""), 200
        return jsonify(state=short.state, success=True), 200
    except ShortURL.DoesNotExist:
        return jsonify(error="Not found"), 404


# We only need this for local development.
if __name__ == '__main__':
    MAIN = True
    app.run(host='0.0.0.0', port=5601)
