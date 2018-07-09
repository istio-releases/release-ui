"""Converts the data from SQL to expected format."""
import datetime
from to_sql import to_sql_tasks


def read_releases(release_data):
  """Reads in releases in the SQL tuple format, transforms them into objects.

  Args:
    release_data

  Returns:
    release_objects
  """
  return release_data


def read_tasks(task_data):
  """Reads the tasks, transforms them into objects.

  Args:
    task_data: a tuple of tuples with task info

  Returns:
    task_objects
  """

def get_task_info(execution_date, airflow_db):
  """Parses through a release's tasks, and returns the task-related info to fill in missing release object info.

  Args:
    execution_date: a python datetime.datetime
    airflow_db: the database connection object

  Returns:
    most_recent_task: the most recent active task
    state: the state of the release based on the task states
  """
  task_query = to_sql_tasks(execution_date)
  task_data = airflow_db.query(task_query)
  for task in task_data:
    # do the stuff, find the most recent task and state
    most_recent_task = 'something'
    state = 'something'

  return most_recent_task, state


def from_sql_releases(release_data, airflow_db):
  """Assembles complete release objects given release data from SQL.

  Args:
    release_data: a tuple of tuples with info from dag_run
    airflow_db: the airflow database connection/object

  Returns:
    release_objects
  """
  releases = read_releases(release_data)



def from_sql_tasks(task_data):
  """Assembles complete task objects given task data from SQL.

  Args:
    task_data: a tuple of tuples with info from task_instance

  Returns:
    task_objects
  """



# TODO(dommarques): The data adapter should be able to:
# - take in the relevant raw sql data, such as the release data and task data
# - relate the tasks and releases
# - put this information into the unified storage format
