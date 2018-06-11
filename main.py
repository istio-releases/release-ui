from flask import Flask, jsonify, request, json
from flask_restful import Api, Resource, reqparse
from flask.views import MethodView
from google.appengine.api import memcache
import json
import read_fake_data



# creating the Flask application
app = Flask(__name__)
api = Api(app)
read_fake_data # reads fake_data.json and puts it in memecache

@app.route('/')
def index():

    result = memcache.get('releases')
    result = jsonify(result)
    return result, 200

@app.route('/getReleases')
def getReleases():
    result = memcache.get('releases')
    result = jsonify(result)
    #return result, 200
    template.render('releases.html', releases=result)

class ListResults(MethodView):
    def get(self):
            result = memcache.get('releases')
            result = jsonify(result)
            return result

app.add_url_rule(
    '/list',
    view_func=ListResults.as_view('list')
)
# @app.route('/list)
# def list():
#     # Get list of releases from memcache or adapter interface
#     result = memcache.get('releases')
#     request.data = result
#     request.data = json.dumps(request.data)
#     return request.data, 200
