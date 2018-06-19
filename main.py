#---------------------UI Server, Connects all Components-------------------------#

from flask import Flask, jsonify, request, json, render_template, send_file, make_response, abort
from flask_restful import Api, Resource, reqparse
from restAPI import Releases, Pagination, GetLabels, GetTasks


# creating the Flask application
app = Flask(__name__)
api = Api(app)

api.add_resource(Releases, '/releases')
api.add_resource(Pagination, '/page')
api.add_resource(GetLabels, '/labels')
api.add_resource(GetTasks, '/tasks')

if __name__ == '__main__':
     app.run(port='8080', debug=True)

@app.route('/')
@app.route('/details')
def basic_pages():
    return make_response(open('templates/index.html').read())
