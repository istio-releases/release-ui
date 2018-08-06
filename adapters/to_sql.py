"""Converts the request arguments to a SQL query."""
import datetime
from resources.release_id_parser import release_id_parser
from data.state import State
from data.state import STRING_FROM_STATE


def to_sql_releases(filter_options):
  """Converts a set of parameters contained in 'args' to a SQL query.

  Gets the releases(AKA dag runs) which fit the parameters.

  Args:
    filter_options: object with filtering parameters

  Returns:
    sql_query: a string which is dynamically constructed using all of the params
  """
  sql_query = 'SELECT dag_id, execution_date FROM dag_run'
  # convert start and end date from unix to python datetime
  start_date = datetime.datetime.fromtimestamp(filter_options.start_date)
  end_date = datetime.datetime.fromtimestamp(filter_options.end_date)
  # append the date filter to the query based on:
  # datetype, start_date, and end_date
  sql_query += ' WHERE execution_date BETWEEN "' + str(start_date) + '" AND "'+ str(end_date) + '"'  # pylint: disable=line-too-long
  # append a state filter, if there is one available -- '0' means all states
  # if filter_options.state != 0:
  #   sql_query += ' AND state = "%s"' %(STRING_FROM_STATE.get(filter_options.state))
  # add sorting parameter
  sql_query = add_sorting(sql_query, filter_options.sort_method, filter_options.reverse)
  # TODO(dommarques) - add label filtering, probably just the dag_id
  sql_query += ';'   # put the finishing touch on it
  return sql_query


def to_sql_release(dag_id, execution_date):
  # construct query
  sql_query = 'SELECT dag_id, execution_date FROM dag_run'
  sql_query += ' WHERE dag_id = "' + dag_id + '"'
  # Using 'LIKE' below allows for execution_date with nanoseconds to be considered
  # and returned, such as manually triggered releases
  sql_query += ' AND execution_date LIKE "%' + str(execution_date) + '%"'
  sql_query += ';'   # put the finishing touch on it
  return sql_query


def to_sql_tasks(dag_id, execution_date):
  sql_query = 'SELECT task_id, dag_id, execution_date, start_date, end_date, state FROM task_instance'
  # Using 'LIKE' below allows for execution_date with nanoseconds to be considered
  # and returned, such as manually triggered releases
  sql_query += ' WHERE execution_date LIKE "%' + str(datetime.datetime.fromtimestamp(execution_date)) + '%"'
  sql_query += ' AND dag_id = "' + str(dag_id) + '"'
  sql_query += ' ORDER BY start_date ASC'
  sql_query += ';'   # put the finishing touch on it
  return sql_query


def to_sql_task(dag_id, task_name, execution_date):
  sql_query = 'SELECT task_id, dag_id, execution_date, start_date, end_date, state FROM task_instance'
  # Using 'LIKE' below allows for execution_date with nanoseconds to be considered
  # and returned, such as manually triggered releases
  sql_query += ' WHERE execution_date LIKE "%' + str(datetime.datetime.fromtimestamp(execution_date)) + '%"'
  sql_query += ' AND task_id = "' + task_name + '"'
  sql_query += ' AND dag_id = "' + str(dag_id) + '"'
  sql_query += ' ORDER BY start_date ASC'
  sql_query += ';'   # put the finishing touch on it
  return sql_query


def to_sql_xcom(dag_id, execution_date):
  sql_query = 'SELECT value FROM xcom'
  # Using 'LIKE' below allows for execution_date with nanoseconds to be considered
  # and returned, such as manually triggered releases
  sql_query += ' WHERE execution_date LIKE "%' + str(datetime.datetime.fromtimestamp(execution_date)) + '%"'
  sql_query += ' AND dag_id = "' + dag_id + '"'
  sql_query += ';'
  return sql_query


def add_sorting(sql_query, sort_method, reverse):
  """Adds sorting parameter to SQL query.

  Args:
    sql_query: the query so far, which will have sorting appended to end (str)
    sort_method: the sort method (int).
    reverse: boolean

  Returns:
    sql_query: now with sorting! (str)
  """
  if sort_method == 1:
    sql_query += ' ORDER BY run_id'
  elif sort_method == 2:
    sql_query += ' ORDER BY execution_date'
  elif sort_method > 2:
    # ensure that the non-relevant sort methods don't cause errors
    return sql_query
  if reverse:
    sql_query += ' DESC'
  else:
    sql_query += ' ASC'
  return sql_query
