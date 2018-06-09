from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse
from google.appengine.api import memcache
import read_fake_data



# creating the Flask application
app = Flask(__name__)
api = Api(app)
read_fake_data # reads fake_data.json and puts it in memecache

@app.route('/', methods=['GET'])
def index():


@app.route('/list', methods=["GET"])
def release_list():
    # Get list of releases from memcache or adapter interface
    result = memcache.get('releases')
    print result
    if request.method == 'GET':
        return Response(json.dumps(result), mimetype="application/json")
    return 404
