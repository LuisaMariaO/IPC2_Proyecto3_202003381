from flask import Flask, request
from flask.json import jsonify
from manage import Manager
from xml.etree import ElementTree as ET

app = Flask(__name__)

manager = Manager()
@app.route('/')
def index():
    return "API is working jus fine! uwu"


if __name__=='__main__':
    app.run(host='localhost',debug=True)