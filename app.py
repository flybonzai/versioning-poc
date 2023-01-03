from flask import Flask, render_template
from yaml_utils import *
from integration_request_generator import *

app = Flask(__name__)


def get_schema_versions():
    return sorted([list(k.keys())[0] for k in load_changelog()['versions']])


@app.route('/')
def hello():
    return render_template('index.html', schema_versions=get_schema_versions())


# TODO think through index page and how to structure it
if __name__ == '__main__':
    app.run(debug=True, port=5001)
