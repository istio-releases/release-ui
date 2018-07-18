"""Connects to the Cloud SQL database."""
import MySQLdb


class AirflowDB(object):
  """"Provides the methods which allow interaction with the Airflow SQL database."""  # pylint: disable=line-too-long

  def __init__(self, user, password, db, host=None, unix_socket=None):
    # creating the connection in the object allows for reconnection in event of
    # a lost connection
    self._unix_socket = unix_socket
    self._host = host
    self._user = user
    self._password = password
    self._db = db
    self._airflow_db = self.create_connection()

  def query(self, request):
    """Sends an SQL query to the airflow database.

    Args:
        request: the SQL request (string)

    Returns:
        The database result (tuple)
    """
    # The following ensures that the query executes and returns,
    # even if the db connection has been lost
    print request
    try:
      cursor = self._airflow_db.cursor()
      cursor.execute(request)
      response = cursor.fetchall()
    except MySQLdb.OperationalError, e:
      print '*****************ERROR TRIGGERED WITH MYSQLDB*********'
      print 'Error: '
      print e
      print ''
      if e[0] == 2006:
        if cursor:
          cursor.close()
        self._airflow_db = self.create_connection()
        cursor = self._airflow_db.cursor()
        cursor.execute(request)
        response = cursor.fetchall()
        if response:
          print '**************SUCCESSFULLY RECONNECTED************'
      if e[0] == 2013:
        airflow_db = self.create_connection()
        cursor = airflow_db.cursor()
        cursor.execute(request)
        response = cursor.fetchall()
        if response:
          print '*************SUCCESSFULLY RECONNECTED************'

    cursor.close()

    return response

  def create_connection(self):
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
    return db

  def check_connection(self):
    passing = False
    try:
      cursor = self._airflow_db.cursor()
      cursor.execute('show tables;')
      response = cursor.fetchall()
      passing = True
    except MySQLdb.OperationalError, e:
      print "*****************ERROR TRIGGERED WITH MYSQLDB*********"
      print 'Error: '
      print e
      print ''
      if e[0] == 2006:
        self._airflow_db = self.create_connection()
        cursor = self._airflow_db.cursor()
      passing = False
    cursor.close()

    return passing

# TODO(dommarques):
#   - get the data into something usable (currently a tuple, possibly shunt to adapter portion)  pylint: disable=line-too-long
#   - implement the Adapter
#   - make the connection secure
#   - switch to production airflow server
