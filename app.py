from flask import Flask
from dotenv import load_dotenv
import os

import json
import csv
import re
import importlib.util

app = Flask(__name__)
load_dotenv()


# File fetching
def load_json(filename):
    path = os.path.abspath(os.path.dirname(__file__)) + \
        filename
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


def load_middlware(filename):
    path = os.path.abspath(os.path.dirname(__file__)) + \
        filename
    # extract filename from /middleware/' + filename + '.py'
    module_name = filename.replace('.py', '').replace('/middleware/', '.')
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
        return module
    except Exception as e:
        return None


def cleanup(file):
    file.close()
    return file


# Templating
def parseMiddleware(key, value, middleware):
    try:
        func_name = key.title().replace(' ', '')  # sign Up -> SignUp
        middleware_function = getattr(middleware, func_name)
        return middleware_function(value)
    except:
        return value


def replace_variables(json_string, data, lookup, middleware):
    # Lookup is a dictionary of column name to index
    for key, value in lookup.items():
        value = parseMiddleware(key, data[lookup[key]], middleware)
        json_string = re.sub(r'{{ (.*' + key + '?) }}',
                             value, json_string)
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
        middleware_pathname,
        delimiter='|',
        quotechar='"'):
    schema = load_json(schema_pathname)
    file, reader = load_csv(migration_source_pathname, delimiter, quotechar)
    middleware = load_middlware(middleware_pathname)

    # Generate
    data_template = flatten_json(schema)
    relevantColumns = getColumnIndexes(reader, data_template)
    # Generate entries from csv
    entries = []
    for row in reader:
        entry_string = replace_variables(
            json.dumps(schema),
            row,
            relevantColumns,
            middleware
        )
        # clean up any empty key value pairs
        entry_string = re.sub(r'(, "\w+": "")|("\w+": "",)',
                              '', entry_string)
        entry = json.loads(entry_string)
        entries.append(entry)

    cleanup(file)

    # Make filename
    filename = file.name.replace(
        'migration-source', 'migrated').rsplit('.', maxsplit=1)[0] + '.json'
    with open(filename, 'w', encoding='utf-8-sig') as outfile:
        json.dump(entries, outfile)

    return json.dumps(entries)


# Flask Routes
@app.route('/translate')
def translate():
    filenames = [
        'sample',
        # 'dealers',
        # 'orders',
        # 'products',
        # 'reviews',
    ]

    # generate source files from filenames at /migration-source/xxx.csv
    for filename in filenames:
        convert(
            '/migration-source/' + filename + '.csv',
            '/schemas/' + filename + '.json',
            '/middleware/' + filename + '.py',
        )

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
