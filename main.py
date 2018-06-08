from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse
import read_fake_data



# creating the Flask application
app = Flask(__name__)
api = Api(app)
read_fake_data # reads fake_data.json and puts it in memecache

@app.route('/')
def index():

    return jsonify(fakeData)

@app.route('/list', methods=["GET"])
def release_list():
    # Get list of releases from memcache or adapter interface
    result = ""
    return Response(json.dumps(result), mimetype="application/json")
