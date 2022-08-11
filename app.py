from flask import Flask
from dotenv import load_dotenv
import os

import json
import csv
from pandas.io.json import json_normalize
import pydash
import functools
import re

app = Flask(__name__)
load_dotenv()


# File fetching
def load_json(filename):
    path = os.path.abspath(os.path.dirname(__file__)) + \
        filename
    # app.logger.info(path)
    f = open(path, 'r', encoding='utf-8-sig')
    data = json.load(f)
    f.close()
    return data


def load_csv(filename, delimiter='|', quotechar='"'):
    path = os.path.abspath(os.path.dirname(__file__)) + \
        filename

    reader = None
    file = open(path, 'r', encoding='utf-8-sig')
    reader = csv.reader(file, delimiter=delimiter, quotechar=quotechar)

    return file, reader


def cleanup(file):
    file.close()
    return file


# Templating
def replace_variables(json_string, data, lookup):
    # Lookup is a dictionary of column name to index
    for key, value in lookup.items():
        app.logger.info(key, value)
        json_string = re.sub(r'{{ (.*' + key + '?) }}',
                             data[lookup[key]], json_string)
    return json_string


# https://towardsdatascience.com/flattening-json-objects-in-python-f5343c794b10
def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '.')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '.')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out


# Relevant columns
def getColNames(reader):
    column_names = []
    for row in reader:
        for column in row:
            column_names.append(column)
        break
    return column_names


def getColumnIndexes(reader, data_template):
    # Used for replacing variables in json template
    # by providing an index to the relevant column
    # ie row[lookup[Title]]

    column_names = getColNames(reader)
    relevantColumns = {}
    for value in data_template.values():
        value = value.replace("{{ ", '').replace(" }}", '')
        relevantColumns[value] = column_names.index(value)
    return relevantColumns


def convert(
        migration_source_pathname,
        schema_pathname,
        delimiter='|',
        quotechar='"'):
    schema = load_json(schema_pathname)
    file, reader = load_csv(migration_source_pathname, delimiter, quotechar)

    # Generate
    data_template = flatten_json(schema)
    relevantColumns = getColumnIndexes(reader, data_template)
    # Generate entries from csv
    entries = []
    for row in reader:
        entry = json.loads(replace_variables(
            json.dumps(schema), row, relevantColumns))
        entries.append(entry)

    cleanup(file)

    # Make filename
    filename = file.name.replace(
        'migration-source', 'migrated').rsplit('.', maxsplit=1)[0] + '.json'
    with open(filename, 'w', encoding='utf-8-sig') as outfile:
        json.dump(entries, outfile)

    return json.dumps(entries)


# Flask Routes
@app.route('/')
def index():
    return 'Hello World!'


@app.route('/translate')
def translate():
    sources = [
        # '/migration-source/customers.csv',
        # '/migration-source/dealers.csv',
        # '/migration-source/orders.csv',
        # '/migration-source/products.csv',
        # '/migration-source/reviews.csv'
    ]

    schemas = [
        # '/schemas/customers.json',
        # '/schemas/dealers.json',
        # '/schemas/orders.json',
        # '/schemas/products.json',
        # '/schemas/reviews.json'
    ]

    for i in range(0, len(sources)):
        app.logger.info(i)
        convert(sources[i], schemas[i], ",", '"')

    return "success"


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
