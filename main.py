from flask import Flask, jsonify, request
from flask_restful import Resource, Api

# creating the Flask application
app = Flask(__name__)
api = Api(app)


@app.route('/')
def index():

    return jsonify(fakeData)

@app.route('/list', methods=["GET"])
def release_list():
    # Get list of releases from memcache or adapter interface
    result = ""
    return Response(json.dumps(result), mimetype="application/json")
