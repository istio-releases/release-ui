"""UI Server, Connects all Components."""
import os
from adapters.airflow_adapter import AirflowAdapter
from adapters.airflow_connector import AirflowDB
from flask import Flask
from flask import make_response
from flask_restful import Api
import resources.resources as resources
from collections import namedtuple

# creating the Flask application
APP = Flask(__name__)
API = Api(APP)
# creates the proper database connection depending on whether the app is
# deployed locally or on App Engine
AirflowConfig = namedtuple('AirflowConfig', ['db', 'bucket_name'])
airflow_configs = []
for i in range(1, (int(os.environ.get('DB_NUM')) + 1)):
  if os.getenv('SERVER_SOFTWARE', '').startswith('Development/'):
    db = AirflowDB(host=os.environ.get('CLOUDSQL_HOST_' + str(i)),
                   user=os.environ.get('CLOUDSQL_USER_' + str(i)),
                   password=os.environ.get('CLOUDSQL_PASSWORD_' + str(i)),
                   db=os.environ.get('CLOUDSQL_DB_' + str(i)))
    bucket_name = os.environ.get('GCS_LOGS_BUCKET_' + str(i))
    airflow_configs.append(AirflowConfig(*(db, bucket_name)))
  else:
    # Connect using the unix socket located at
    # /cloudsql/cloudsql-connection-name.
    CLOUDSQL_CONNECTION_NAME = os.environ.get('CLOUDSQL_CONNECTION_NAME_' + str(i))
    CLOUDSQL_UNIX_SOCKET = os.path.join('/cloudsql', CLOUDSQL_CONNECTION_NAME)
    db = AirflowDB(unix_socket=CLOUDSQL_UNIX_SOCKET,
                   user=os.environ.get('CLOUDSQL_USER_' + str(i)),
                   password=os.environ.get('CLOUDSQL_PASSWORD_' + str(i)),
                   db=os.environ.get('CLOUDSQL_DB_' + str(i)))
    bucket_name = os.environ.get('GCS_LOGS_BUCKET_' + str(i))
    airflow_configs.append(AirflowConfig(*(db, bucket_name)))

adapter = AirflowAdapter(airflow_configs)


# adding resource endpoints to different urls
API.add_resource(resources.Releases, '/releases', resource_class_kwargs={'adapter': adapter})
API.add_resource(resources.Release, '/release', resource_class_kwargs={'adapter': adapter})
API.add_resource(resources.Branches, '/branches', resource_class_kwargs={'adapter': adapter})
API.add_resource(resources.Types, '/types', resource_class_kwargs={'adapter': adapter})
API.add_resource(resources.Tasks, '/tasks', resource_class_kwargs={'adapter': adapter})
API.add_resource(resources.Logs, '/logs', resource_class_kwargs={'adapter': adapter, 'bucket_name': bucket_name})

if __name__ == '__main__':
  APP.run(port='8080', debug=True)  # TODO(dommarques): Delete debug when app is done


# route to the first page
@APP.route('/')
def basic_pages():
  """Serves Webpage."""
  return make_response(open('templates/index.html').read())
