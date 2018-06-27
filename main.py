"""UI Server, Connects all Components."""

from flask import Flask
from flask import make_response
from flask_restful import Api
from rest_api import RestAPI


# creating the Flask application
APP = Flask(__name__)
API = Api(APP)

REST = RestAPI()

API.add_resource(REST.releases, '/releases')
API.add_resource(REST.release, '/release')
API.add_resource(REST.labels, '/labels')
API.add_resource(REST.tasks, '/tasks')
API.add_resource(REST.airflowdb, '/airflowdb')

if __name__ == '__main__':
  APP.run(port='8080', debug=True)


@APP.route('/')
def basic_pages():
  """Serves Webpage."""
  return make_response(open('templates/index.html').read())
