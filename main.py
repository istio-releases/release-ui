from flask import Flask, jsonify, request
<<<<<<< HEAD
from flask_restful import Api, Resource, reqparse
import read_fake_data


=======
from flask_restful import Resource, Api
>>>>>>> 1ffcb6be6fc470ab3dfd397b1cccae91d14dd2bf

# creating the Flask application
app = Flask(__name__)
api = Api(app)
<<<<<<< HEAD
read_fake_data # read and load the data from fake_data.py into memcache
@app.route('/', methods=['GET', 'POST'])
def index():
    # fake1 = {"version":"xxx-xxx-123","status":1,"creation":"01 Jan 1970 00:00:00","last_mod":"01 Jan 1970 00:00:00","last_active":"task123","tags":[1,3]}
    # fake2 = {"version":"xxx-xxx-456","status":2,"creation":"04 Dec 2017 00:12:00","last_mod":"04 Dec 2017 00:12:00","last_active":"task456","tags":[2]}
    # fake3 = {"version":"xxx-xxx-789","status":3,"creation":"29 Jun 1999 4:30:30","last_mod":"29 Jun 1999 4:30:30","last_active":"task789","tags":[4]}
    # fake4 = {"version":"xxx-xxx-000","status":4,"creation":"04 Dec 1995 00:12:00","last_mod":"04 Dec 1995 00:12:00","last_active":"task000","tags":[1,2]}
    # fakeData = [fake1, fake2, fake3, fake4]
    fakeData = memcache.get('releases')
    if request.method = 'GET':
        return jsonify(fakeData), 200
=======


@app.route('/')
def index():

    return jsonify(fakeData)

@app.route('/list', methods=["GET"])
def release_list():
    # Get list of releases from memcache or adapter interface
    result = ""
    return Response(json.dumps(result), mimetype="application/json")
>>>>>>> 1ffcb6be6fc470ab3dfd397b1cccae91d14dd2bf
