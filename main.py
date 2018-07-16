"""UI Server, Connects all Components."""
import os
from file_adapter import FileAdapter
from flask import Flask
from flask import make_response
from flask_restful import Api
import resources
from resources import Releases
from resources import Resources
from airflow_connector import AirflowDB

# creating the Flask application
APP = Flask(__name__)
API = Api(APP)
resources = Resources()


adapter = FileAdapter('fake_data/fake_release_data.json', 'fake_data/fake_task_data.json')
cloudsql_unix_socket = os.path.join('/cloudsql', 'istio-release-ui:us-central1:prod-airflow-snapshot-sandbox')
cloudsql_host = '35.193.234.53'
cloudsql_user = 'root'
cloudsql_password = ''
cloudsql_db = 'airflow-db'
airflow_db = AirflowDB(unix_socket=cloudsql_unix_socket,
                       host=cloudsql_host,
                       user=cloudsql_user,
                       password=cloudsql_password,
                       db=cloudsql_db)


my_resources = Releases(adapter)

# adding resource endpoints to different urls
API.add_resource(resources.releases, '/releases', resource_class_kwargs={'adapter': adapter})
API.add_resource(resources.release, '/release', resource_class_kwargs={'adapter': adapter})
API.add_resource(resources.branches, '/branches', resource_class_kwargs={'adapter': adapter})
API.add_resource(resources.types, '/types', resource_class_kwargs={'adapter': adapter})
API.add_resource(resources.tasks, '/tasks', resource_class_kwargs={'adapter': adapter})
API.add_resource(resources.airflowdb, '/airflowdb', resource_class_kwargs={'airflow_db': airflow_db})  # TODO(dommarques): Delete when done

if __name__ == '__main__':
  APP.run(port='8080', debug=True)


# route to the first page
@APP.route('/')
def basic_pages():
  """Serves Webpage."""
  return make_response(open('templates/index.html').read())
