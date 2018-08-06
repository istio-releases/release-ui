"""Connects to the Cloud SQL database."""
import logging
import MySQLdb
import threading
try:
  from mysql.connector import errorcode
except ImportError:
  from lib.mysql.connector import errorcode
class AirflowDB(object):
  """Provides the methods which allow interaction with the Airflow SQL database."""  # pylint: disable=line-too-long

  def __init__(self, user, password, db, host=None, unix_socket=None):
    """Initializes the connection vars and db connection.

    Args:
      user: str
      password: str
      db: list of databases
      host: str
      unix_socket: str
    """
    # creating the connection in the object allows for reconnection in event of
    # a lost connection
    self._unix_socket = unix_socket
    self._host = host
    self._user = user
    self._password = password
    self._db = db
    self._lock = threading.Lock()
    self._create_connection()

  def query(self, request):
    """Sends an SQL query to the airflow database.

    Args:
        request: the SQL request (string)

    Returns:
        The database result (tuple)
    """
    # The following ensures that the query executes and returns,
    # even if the db connection has been lost
    logging.info('Running query "%s" against Airflow DB' % request)
    # locking improves reliability for requests dramatically
    with self._lock:
      try:
        cursor = self._airflow_db.cursor()
        cursor.execute(request)
        response = cursor.fetchall()
      except MySQLdb.OperationalError, e:
        logging.error('Error %i triggered with MySQLdb: %s'  % (e[0], e[1]))
        if e[0] in [errorcode.CR_SERVER_GONE_ERROR, errorcode.CR_SERVER_LOST]:
          if cursor:
            cursor.close()
          self._create_connection()
          cursor = self._airflow_db.cursor()
          cursor.execute(request)
          response = cursor.fetchall()

      cursor.close()

    logging.info('Returns: ' + str(response))
    return response

  def _create_connection(self):
    """Connects to the Cloud SQL database."""
    if self._host:
      db = MySQLdb.connect(
          # unix_socket=self._unix_socket,
          host=self._host,
          user=self._user,
          passwd=self._password,
          db=self._db)
    else:
      db = MySQLdb.connect(
          unix_socket=self._unix_socket,
          user=self._user,
          passwd=self._password,
          db=self._db)
    self._airflow_db = db
    logging.info('MySQLdb connection restored.')

# TODO(dommarques):
#   - get the data into something usable (currently a tuple, possibly shunt to adapter portion)  pylint: disable=line-too-long
#   - implement the Adapter
#   - make the connection secure
#   - switch to production airflow server
