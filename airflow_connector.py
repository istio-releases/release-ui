"""Connects to the Cloud SQL database."""
import os
import MySQLdb


class AirflowDB(object):
  """"Provides the methods which allow interaction with the Airflow SQL database."""  # pylint: disable=line-too-long

  def __init__(self, db_connection):
    """Connects to the Cloud SQL database."""

    self._db = db_connection

  def query(self, request):
    """Sends an SQL query to the airflow database.

    Args:
        request: the SQL request (string)

    Returns:
        The database result (tuple)
    """
    # db = connect_to_cloudsql()
    print request
    cursor = self._db.cursor()
    cursor.execute(request)
    response = cursor.fetchall()
    cursor.close()

    return response

# TODO(dommarques):
#   - get the data into something usable (currently a tuple, possibly shunt to adapter portion)
#   - implement the Adapter
#   - make the connection secure
#   - switch to production airflow server
