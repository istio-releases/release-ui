from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse
from google.appengine.api import memcache
import read_fake_data
from google.appenginge.api import memcache


# creating the Flask application
app = Flask(__name__)
api = Api(app)
read_fake_data # reads fake_data.json and puts it in memecache

<<<<<<< HEAD
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
=======
@app.route('/releases', methods=["GET"])
def getReleases() :
    return jsonify(memcache.get("releases"))

@app.route('/')
def index():
    return jsonify(memcache.get("releases"))
>>>>>>> 3e7b0dfc9176e88e2cc53b616d3334f3c548320a
