"""UI Server, Connects all Components."""
from flask import Flask
from flask import make_response
from flask_restful import Api
from rest_api import RestAPI


# creating the Flask application
app = Flask(__name__)
api = Api(app)

rest_api = RestAPI()

api.add_resource(rest_api.releases, '/releases')
api.add_resource(rest_api.release, '/release')
api.add_resource(rest_api.labels, '/labels')
api.add_resource(rest_api.tasks, '/tasks')

if __name__ == '__main__':
  app.run(port='8080', debug=True)


@app.route('/')
def basic_pages():
  return make_response(open('templates/index.html').read())
