from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

app.run(port=5000, host="localhost")