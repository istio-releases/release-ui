"""Connects to the Cloud SQL database."""
import os
import MySQLdb

# These environment variables are configured in app.yaml.
CLOUDSQL_CONNECTION_NAME = os.environ.get('CLOUDSQL_CONNECTION_NAME')
CLOUDSQL_USER = os.environ.get('CLOUDSQL_USER')
CLOUDSQL_PASSWORD = os.environ.get('CLOUDSQL_PASSWORD')
CLOUDSQL_HOST = os.environ.get('CLOUDSQL_HOST')
CLOUDSQL_DB = os.environ.get('CLOUDSQL_DB')

if CLOUDSQL_CONNECTION_NAME is None:
  CLOUDSQL_CONNECTION_NAME = 'istio-release-ui:us-central1:prod-airflow-snapshot-sandbox'  # pylint: disable=line-too-long
  CLOUDSQL_USER = 'root'
  CLOUDSQL_PASSWORD = ''
  CLOUDSQL_HOST = '35.193.234.53'
  CLOUDSQL_DB = 'airflow-db'


class AirflowDB(object):
  """"Provides the methods which allow interaction with the Airflow SQL database."""  # pylint: disable=line-too-long

  def __init__(self):
    """Connects to the Cloud SQL database."""

    # When deployed to App Engine, the `SERVER_SOFTWARE` environment variable
    # will be set to 'Google App Engine/version'.
    if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
      # Connect using the unix socket located at
      # /cloudsql/cloudsql-connection-name.
      cloudsql_unix_socket = os.path.join(
          '/cloudsql', CLOUDSQL_CONNECTION_NAME)

      db = MySQLdb.connect(
          unix_socket=cloudsql_unix_socket,
          user=CLOUDSQL_USER,
          passwd=CLOUDSQL_PASSWORD,
          db=CLOUDSQL_DB)

    else:
      db = MySQLdb.connect(
          host=CLOUDSQL_HOST,
          user=CLOUDSQL_USER,
          passwd=CLOUDSQL_PASSWORD,
          db=CLOUDSQL_DB)

    self.db = db

  def query(self, request):
    """Sends an SQL query to the airflow database.

    Args:
        request: the SQL request (string)

    Returns:
        The database result (tuple)
    """
    # db = connect_to_cloudsql()
    cursor = self.db.cursor()
    cursor.execute(request)
    response = cursor.fetchall()
    cursor.close()

    return response

# TODO(dommarques):
#   - get the data into something usable (currently a tuple, possibly shunt to adapter portion)
#   - implement the Adapter
#   - make the connection secure
#   - switch to production airflow server
