"""Connects to the Cloud SQL database."""
import os
import MySQLdb

# These environment variables are configured in app.yaml.
CLOUDSQL_CONNECTION_NAME = os.environ.get('CLOUDSQL_CONNECTION_NAME')
CLOUDSQL_USER = os.environ.get('CLOUDSQL_USER')
CLOUDSQL_PASSWORD = os.environ.get('CLOUDSQL_PASSWORD')


def connect_to_cloudsql():
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
        passwd=CLOUDSQL_PASSWORD)

  else:
    db = MySQLdb.connect(
        host='35.193.234.53',
        user=CLOUDSQL_USER, passwd=CLOUDSQL_PASSWORD, db="airflow-db")

  return db
