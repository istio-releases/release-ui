"""Connects to the Cloud SQL database."""


class AirflowDB(object):
  """"Provides the methods which allow interaction with the Airflow SQL database."""  # pylint: disable=line-too-long

  def __init__(self, db_connection):
    """Connects to the Cloud SQL database."""
    # If I try to put this in main.py, then I get a circular import error when
    # I try to import the connection/AiflowDB object into resources.py
    # I could put it somewhere else, but for now it's here. It also seems that
    # App Engine simply let me delete the env vars and everything is working finished

    self._db = db_connection

  def query(self, request):
    """Sends an SQL query to the airflow database.

    Args:
        request: the SQL request (string)

    Returns:
        The database result (tuple)
    """
    cursor = self._db.cursor()
    cursor.execute(request)
    response = cursor.fetchall()
    cursor.close()

    return response

# TODO(dommarques):
#   - get the data into something usable (currently a tuple, possibly shunt to adapter portion)  pylint: disable=line-too-long
#   - implement the Adapter
#   - make the connection secure
#   - switch to production airflow server
