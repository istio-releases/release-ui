from flask import Flask, jsonify, request, render_template
from flask import send_file, make_response, abort
from flask.views import MethodView
import json
import read_fake_data
from google.appengine.api import memcache


# creating the Flask application
app = Flask(__name__)
json_data = open("fake_data.json").read()
parsed_json = json.loads(json_data)
memcache.add(key="releases", value=parsed_json)

result = memcache.get('releases')
result = json.dumps(result)
@app.route('/')
@app.route('/details')
def basic_pages():
    return make_response(open('templates/index.html').read())


def getReleases():
    # return render_template('details.html')
    return result, 200


class ListResults(MethodView):
    def get(self):
            result = memcache.get('releases')
            result = jsonify(result)
            return result


#app.add_url_rule(
#    '/list',
#    view_func=ListResults.as_view('list')
#)
# @app.route('/list)
# def list():
#     # Get list of releases from memcache or adapter interface
#     result = memcache.get('releases')
#     request.data = result
#     request.data = json.dumps(request.data)
#     return request.data, 200
