from flask import Flask
from dotenv import load_dotenv
import json
import os

app = Flask(__name__)
load_dotenv()


def load_json(filename):
    path = os.path.abspath(os.path.dirname(__file__)) + \
        filename
    app.logger.info(path)
    f = open(path, 'r')
    data = json.load(f)
    return data


@app.route('/')
def index():
    return 'Hello World!'


@app.route('/translate')
def translate():
    schema = load_json('/schemas/json.sample.json')

    for value in schema:
        app.logger.info(value)

    response = json.dumps(schema)
    return response


@ app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET, POST, PATCH, DELETE, OPTIONS')
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


if __name__ == '__main__':
    app.run(debug=True, use_debugger=True, use_reloader=True)
