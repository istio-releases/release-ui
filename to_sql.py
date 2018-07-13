"""Converts the request arguments to a SQL query."""
import datetime


def to_sql_releases(start_date, end_date, datetype, state,
                    sort_method, descending):
  """Converts a set of parameters contained in 'args' to a SQL query.

  Gets the releases(AKA dag runs) which fit the parameters.

  Args:
    start_date: unix timestamp format
    end_date: unix timestamp format
    datetype: what to filter by - created or last last_modified
    state: state enumeration
    sort_method: sort method enumeration
    descending: boolean

  Returns:
    sql_query: a string which is dynamically constructed using all of the params
  """
  sql_query = 'SELECT * FROM dag_run'
  # convert start and end date from unix to python datetime
  start_date = datetime.datetime.fromtimestamp(start_date)
  end_date = datetime.datetime.fromtimestamp(end_date)
  # append the date filter to the query based on:
  # datetype, start_date, and end_date
  if datetype == 0:
    sql_query += ' WHERE execution_date BETWEEN "' + str(start_date) + '" AND "'+ str(end_date) + '"'  # pylint: disable=line-too-long
  else:
    sql_query += ' WHERE execution_date BETWEEN "' + str(start_date) + '" AND "'+ str(end_date) + '"'  # pylint: disable=line-too-long
  # append a state filter, if there is one available -- '0' means all states
  if state != 0:
    sql_query += ' AND state = "%s"' %(convert_state(state))
    print convert_state(state)
  # add sorting parameter
  sql_query = add_sorting(sql_query, sort_method, descending)
  # TODO(dommarques) - add label filtering, probably just the dag_id
  sql_query += ';'   # put the finishing touch on it
  return sql_query


def to_sql_release(release_id):
  sql_query = 'SELECT * FROM dag_run'
  sql_query += ' WHERE run_id = ' + release_id
  sql_query += ';'   # put the finishing touch on it
  return sql_query


def to_sql_tasks(execution_date):
  sql_query = 'SELECT * FROM task_instance'
  sql_query += ' WHERE execution_date = "' + str(datetime.datetime.fromtimestamp(execution_date)) + '"'
  sql_query += ' ORDER BY execution_date'
  sql_query += ';'   # put the finishing touch on it
  return sql_query


def to_sql_task(task_name, execution_date):
  sql_query = 'SELECT * FROM task_instance'
  sql_query += ' WHERE execution_date = ' + datetime.datetime.fromtimestamp(execution_date)
  sql_query += ' AND task_id = ' + task_name
  sql_query += ' ORDER BY execution_date'
  sql_query += ';'   # put the finishing touch on it
  return sql_query


def convert_state(state):
  """Converts the state enumeration into the format needed for the SQL query.

  Args:
    state: the integer which enumerates the requested state (int)

  Returns:
    state: string format which follows the same format in the SQl db (str)
  """
  state = int(state)
  if state == 0:
    return 'none'
  elif state == 1:
    return 'running'
  elif state == 2:
    return 'success'
  elif state == 3:
    return 'failed'
  elif state == 4:
    return 'shutdown'


def add_sorting(sql_query, sort_method, descending):
  """Adds sorting parameter to SQL query.

  Args:
    sql_query: the query so far, which will have sorting appended to end (str)
    sort_method: the sort method (int).
    descending: boolean

  Returns:
    sql_query: now with sorting! (str)
  """
  if sort_method == 1:
    sql_query += ' ORDER BY run_id'
  elif sort_method == 2:
    sql_query += ' ORDER BY execution_date'
  elif sort_method > 2:
    return sql_query
  if descending:
    sql_query += ' DESC'
  else:
    sql_query += ' ASC'
  # TODO(dommarques) - finish adding sort methods 5,6,7,8
  return sql_query
