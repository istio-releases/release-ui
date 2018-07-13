"""UI Server, Connects all Components."""
from flask import Flask
from flask import make_response
from flask_restful import Api
from resources import Resources


# creating the Flask application
APP = Flask(__name__)
API = Api(APP)

REST = Resources()

# adding resource endpoints to different urls
API.add_resource(REST.releases, '/releases')
API.add_resource(REST.release, '/release')
API.add_resource(REST.labels, '/labels')
API.add_resource(REST.tasks, '/tasks')
API.add_resource(REST.airflowdb, '/airflowdb')  # TODO(dommarques): Delete when done

if __name__ == '__main__':
  APP.run(port='8080', debug=True)


# route to the first page
@APP.route('/')
def basic_pages():
  """Serves Webpage."""
  return make_response(open('templates/index.html').read())
