
from flask import Flask, jsonify, request, json, render_template
from flask_restful import Api, Resource, reqparse
from flask import send_file, make_response, abort
from flask.views import MethodView
import json
import read_fake_data
from google.appengine.api import memcache


# creating the Flask application
app = Flask(__name__)
api = Api(app)

json_data = open("fake_data.json").read()
parsed_json = json.loads(json_data)
memcache.add(key="releases", value=parsed_json)



class Releases(Resource):
    def get(self):
        result = memcache.get('releases')
        result = json.dumps(result)
        return result, 200

api.add_resource(Releases, '/releases')

if __name__ == '__main__':
     app.run(port='8080')

@app.route('/')
@app.route('/details')
def basic_pages():
    return make_response(open('templates/index.html').read())


@app.route('/getReleases')
def getReleases():
    # return render_template('details.html')
    result = memcache.get('releases')
    result = json.dumps(result)
    return result, 200

# @app.route('/list)
# def list():
#     # Get list of releases from memcache or adapter interface
#     result = memcache.get('releases')
#     request.data = result
#     request.data = json.dumps(request.data)
#     return request.data, 200
