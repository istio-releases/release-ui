"""Converts the data from SQL to expected format."""
from release import Release
from task import Task
from to_sql import to_sql_tasks
from to_timestamp import to_timestamp
from datetime import datetime


def read_releases(release_data, airflow_db):
  """Reads in releases in the SQL tuple format, transforms them into objects.

  Args:
    release_data: the raw release data from SQL (tuple)
    airflow_db: the airflow database connection object

  Returns:
    release_objects
  """
  release_objects = []
  for item in release_data:  # iterate through each release in release_data
    release = Release()  # initialize the release object
    started = to_timestamp(item[2])
    task_ids, most_recent_task, state = get_task_info(started, airflow_db)
    release.name = item[4]
    release.tasks = task_ids
    release.started = to_timestamp(item[2])
    release.links = ['https://youtu.be/dQw4w9WgXcQ']  # TODO(dommarques) these need to be implemented into airflow first pylint: disable=line-too-long
    release.labels = [item[1]]
    release.state = state
    if most_recent_task:
      release.last_modified = to_timestamp(most_recent_task.last_modified)
      release.last_active_task = most_recent_task.task_name
    else:
      release.last_modified = to_timestamp(item[2])
    release_objects.append(release)

  return release_objects


def read_tasks(task_data):
  """Reads the tasks, transforms them into objects.

  Args:
    task_data: a tuple of tuples with task info

  Returns:
    task_objects
  """
  task_objects = []
  for item in task_data:
    task = Task()
    task.task_name = item[0]
    task.add_dependency = None  # TODO(dommarques): figure out how to get this - dag info?
    task.started = to_timestamp(item[3])
    task.status = state_from_string(item[6])
    task.last_modified = to_timestamp(item[4])
    task.log_url = "https://youtu.be/dQw4w9WgXcQ"  # TODO(dommarques): figure out how to get the log in here
    task.error = item[6]
    task_objects.append(task)
  return task_objects


def get_task_info(execution_date, airflow_db):
  """Gets task-related info to fill in missing release object info.

  Args:
    execution_date: a python datetime.datetime
    airflow_db: the database connection object

  Returns:
    most_recent_task: the most recent active task
    state: the state of the release based on the task states
  """
  task_query = to_sql_tasks(execution_date)
  task_data = airflow_db.query(task_query)
  task_objects = read_tasks(task_data)
  state = 0
  task_ids = []
  if task_objects:
    most_recent_task = task_objects[-1]
  else:
    most_recent_task = None
  for task in task_objects:
    if task.status > state:
      state = task.status
    task_ids.append(execution_date)
  return task_ids, most_recent_task, state


def from_sql_releases(release_data, airflow_db):
  """Assembles complete release objects given release data from SQL.

  Args:
    release_data: a tuple of tuples with info from dag_run
    airflow_db: the airflow database connection/object

  Returns:
    release_objects
  """
  releases = read_releases(release_data, airflow_db)


def from_sql_tasks(task_data):
  """Assembles complete task objects given task data from SQL.

  Args:
    task_data: a tuple of tuples with info from task_instance

  Returns:
    task_objects
  """


def state_from_string(state):
  if state == 'none':
    return 0
  elif state == 'running':
    return 1
  elif state == 'success':
    return 2
  elif state == 'failed':
    return 3
  elif state == 'shutdown':
    return 4
  elif state == 'upstream_failed':  # here for the tasks
    return 1


# TODO(dommarques): The data adapter should be able to:
# - take in the relevant raw sql data, such as the release data and task data
# - relate the tasks and releases
# - put this information into the unified storage format
