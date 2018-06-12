from flask import Flask, jsonify, request, json, render_template
from flask_restful import Api, Resource, reqparse
from flask.views import MethodView
from google.appengine.api import memcache
import json


# creating the Flask application
app = Flask(__name__)
api = Api(app)

json_data = open("fake_data.json").read()
parsed_json = json.loads(json_data)
memcache.add(key="releases", value=parsed_json)



# class Releases(Resource):
#     def get(self):
#         result = memcache.get('releases')
#         result = json.dumps(result)
#         return result, 200
#
# api.add_resource(Releases, '/releases')
#
# if __name__ == '__main__':
#      app.run(port='8080')

@app.route('/')
def index():
    # result = memcache.get('releases')
    # result = jsonify(result)
    print "HI!"
    return render_template('index.html')


@app.route('/getReleases')
def getReleases():
    # return render_template('details.html')
    result = memcache.get('releases')
    result = json.dumps(result)
    return result, 200

# @app.route('/fake_data.json')
# def fake_data():
#     return send_from_directory('fake_data.json')



# @app.route('/list)
# def list():
#     # Get list of releases from memcache or adapter interface
#     result = memcache.get('releases')
#     request.data = result
#     request.data = json.dumps(request.data)
#     return request.data, 200
