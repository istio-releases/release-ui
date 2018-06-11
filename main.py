from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS
import read_fake_data
from google.appenginge.api import memcache


# creating the Flask application
app = Flask(__name__)
CORS(app)
api = Api(app)
read_fake_data # reads fake_data.json and puts it in memecache

@app.route('/releases', methods=["GET"])
def getReleases() :
    return jsonify(memcache.get("releases"))

@app.route('/')
def index():
    return jsonify(memcache.get("releases"))
