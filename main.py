from flask import Flask, jsonify, request, json, render_template, send_file, make_response, abort
from flask_restful import Api, Resource, reqparse
import restAPI


# creating the Flask application
app = Flask(__name__)
api = Api(app)


api.add_resource(restAPI.Releases, '/releases')
api.add_resource(restAPI.Pagination, '/page')
api.add_resource(restAPI.GetLabels, '/labels')

if __name__ == '__main__':
     app.run(port='8080', debug=True)

#---------------------Handlers-------------------------#
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

# TODO(dommarques):
#    - implement a way to log and cache all of the labels in each release
