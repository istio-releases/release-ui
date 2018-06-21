#---------------------UI Server, Connects all Components-------------------------#

from flask import Flask, make_response
from flask_restful import Api
from rest_api import RestAPI


# creating the Flask application
app = Flask(__name__)
api = Api(app)

RestAPI = RestAPI()

api.add_resource(RestAPI.releases, '/releases')
api.add_resource(RestAPI.release, '/release')
api.add_resource(RestAPI.labels, '/labels')
api.add_resource(RestAPI.tasks, '/tasks')

if __name__ == '__main__':
     app.run(port='8080', debug=True)

@app.route('/')
def basic_pages():
    return make_response(open('templates/index.html').read())
