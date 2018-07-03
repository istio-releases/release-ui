"""Converts the request arguments to a SQL query."""
import datetime


def to_sql_releases(args):
  """Converts a set of parameters contained in 'args' to a SQL query.

  Gets the releases(AKA dag runs) which fit the parameters.

  Args:
    args: a dict of values which contains all of the required filter params

  Returns:
    sql_query: a string which is dynamically constructed using all of the params
  """
  start_date = int(args['start_date'])
  end_date = int(args['end_date'])
  datetype = str(args['datetype'])
  state = str(int(args['state']))
  # label = str(args['label'])
  sort_method = int(args['sort_method'])
  sql_query = 'SELECT * FROM dag_run'
  # convert start and end date from unix to python datetime
  start_date = datetime.datetime.fromtimestamp(start_date)
  end_date = datetime.datetime.fromtimestamp(end_date)
  # append the date filter to the query based on:
  # datetype, start_date, and end_date
  if datetype == 0:
    sql_query += ' WHERE execution_date BETWEEN"%d" AND "%i"' %(start_date, end_date)  # pylint: disable=line-too-long
  else:
    sql_query += ' WHERE execution_date BETWEEN"%d" AND "%i"' %(start_date, end_date)  # pylint: disable=line-too-long
  # append a state filter, if there is one available -- '0' means all states
  if state != 0:
    sql_query += ' AND state = %s' %(convert_state(state))
  # add sorting parameter
  sql_query = add_sorting(sql_query, sort_method)
  # TODO(dommarques) - add label filtering, probably just the dag_id
  sql_query += ';'   # put the finishing touch on it
  return sql_query


def to_sql_release(release_id):
  sql_query = 'SELECT * FROM dag_run'
  sql_query += ' WHERE run_id = ' + release_id
  sql_query += ';'   # put the finishing touch on it
  return sql_query


def to_sql_tasks(execution_date):
  sql_query = 'SELECT * FROM task_insance'
  sql_query = ' WHERE execution_date = ' + execution_date
  sql_query += ';'   # put the finishing touch on it
  return sql_query


def convert_state(state):
  """Converts the state enumeration into the format needed for the SQL query.

  Args:
    state: the integer which enumerates the requested state (int)

  Returns:
    state: string format which follows the same format in the SQl db (str)
  """
  if state == 0:
    return 'None'
  elif state == 1:
    return 'running'
  elif state == 2:
    return 'success'
  elif state == 3:
    return 'failed'
  elif state == 4:
    return 'shutdown'


def add_sorting(sql_query, sort_method):
  """Adds sorting parameter to SQL query.

  Args:
    sql_query: the query so far, which will have sorting appended to end (str)
    sort_method: the sort method (int).

  Returns:
    sql_query: now with sorting! (str)
  """
  if sort_method == 1:
    sql_query += 'ORDER BY run_id ASC'
  elif sort_method == 2:
    sql_query += 'ORDER BY run_id DESC'
  elif sort_method == 3:
    sql_query += 'ORDER BY execution_date DESC'
  elif sort_method == 4:
    sql_query += 'ORDER BY execution_date ASC'
  # TODO(dommarques) - finish adding sort methods 5,6,7,8
  return sql_query
