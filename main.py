"""UI Server, Connects all Components."""
import os
from airflow_connector import AirflowDB
from file_adapter import FileAdapter
from flask import Flask
from flask import make_response
from flask_restful import Api
from resources.rest_api import RestAPI


# creating the Flask application
APP = Flask(__name__)
API = Api(APP)


adapter = FileAdapter('fake_data/fake_release_data.json', 'fake_data/fake_task_data.json')

# creating the connection in the object allows for reconnection in event of
# a lost connection
airflow_db = AirflowDB(unix_socket=os.environ.get('CLOUDSQL_UNIX_SOCKET'),
                       host=os.environ.get('CLOUDSQL_HOST'),
                       user=os.environ.get('CLOUDSQL_USER'),
                       password=os.environ.get('CLOUDSQL_PASSWORD'),
                       db=os.environ.get('CLOUDSQL_DB'))

# adding resource endpoints to different urls
API.add_resource(resources.Releases, '/releases', resource_class_kwargs={'adapter': adapter})
API.add_resource(resources.Release, '/release', resource_class_kwargs={'adapter': adapter})
API.add_resource(resources.Branches, '/branches', resource_class_kwargs={'adapter': adapter})
API.add_resource(resources.Types, '/types', resource_class_kwargs={'adapter': adapter})
API.add_resource(resources.Tasks, '/tasks', resource_class_kwargs={'adapter': adapter})
API.add_resource(resources.AirflowDBTesting, '/airflowdb', resource_class_kwargs={'airflow_db': airflow_db})  # TODO(dommarques): Delete when done

if __name__ == '__main__':
  APP.run(port='8080', debug=True)


# route to the first page
@APP.route('/')
def basic_pages():
  """Serves Webpage."""
  return make_response(open('templates/index.html').read())
