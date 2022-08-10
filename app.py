from flask import Flask, jsonify, request, Response
from py3dbp import Packer, Bin, Item
from urllib.parse import urlparse, parse_qs
from copy import deepcopy
import requests
from dotenv import load_dotenv
import os
from geopy.geocoders import Nominatim
from math import radians, cos, sin, asin, sqrt
import json

app = Flask(__name__)
load_dotenv()


@app.route('/')
def index():
    return 'Hello World!'


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET, POST, PATCH, DELETE, OPTIONS')
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


if __name__ == '__main__':
    app.run(debug=True, use_debugger=True, use_reloader=True)
