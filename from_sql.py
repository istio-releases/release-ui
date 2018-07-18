"""Converts the data from SQL to expected format."""
import json
from release import Release
from task import Task
from to_sql import to_sql_tasks
from to_sql import to_sql_xcom
from to_timestamp import to_timestamp


def read_releases(release_data, airflow_db):
  """Reads in releases in the SQL tuple format, transforms them into objects.

  Args:
    release_data: the raw release data from SQL (tuple)
    airflow_db: the airflow database connection object

  Returns:
    release_objects
  """
  release_objects = {}  # resources.py expects a dict of objects
  for item in release_data:  # iterate through each release in release_data
    release = Release()  # initialize the release object
    started = to_timestamp(item[2])
    task_ids, most_recent_task, state = get_task_info(started, airflow_db)
    xcom_dict, green_sha = get_xcom(started, item[1], airflow_db)
    release.release_id = item[1] + '@' + str(item[2])
    release.tasks = task_ids
    release.started = started
    release.links = construct_links(green_sha)  # TODO(dommarques) these need to be implemented into airflow first, or we make our own way to get the links pylint: disable=line-too-long
    release.labels = [item[1]]
    release.state = state
    release.branch, release.release_type = parse_dag_id(item[1])
    if xcom_dict is None:
      # allows for continuation, even if xcom has not been generated yet
      release.name = release.release_id
    else:
      release.name = xcom_dict['VERSION']
    if most_recent_task:
      # allows for continuation even if tasks have not begun/been generated yet
      release.last_modified = to_timestamp(most_recent_task.last_modified)
      release.last_active_task = most_recent_task.task_name
    else:
      release.last_modified = to_timestamp(item[2])
      release.last_active_task = ''
    release_objects[release.name] = release

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
    task.log_url = 'https://youtu.be/dQw4w9WgXcQ'  # TODO(dommarques): figure out how to get the log in here
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
    most_recent_task = task_objects[len(task_objects) - 1]
  else:
    most_recent_task = None
  for task in task_objects:
    if task.status > state:
      state = task.status
    task_ids.append(task.task_name)
  return task_ids, most_recent_task, state


def read_xcom_vars(xcom_data):
  """Reads the xcom data to get the dict of vars and the green build SHA."""
  # occasionally, the xcom data doesn't exist yet. This is a workaround
  try:
    xcom_dict = json.loads(xcom_data[0][2])
    green_sha = xcom_data[1][2]
    return xcom_dict, green_sha
  except IndexError:
    return None, None


def get_xcom(execution_date, dag_id, airflow_db):
  """Gets relevant xcom data from SQL.

    Args:
      execution_date: int or float
      dag_id: str
      airflow_db: airflow database connection object

    Returns:
      xcom_dict: the dictionary of xcom information
      green_sha: the green build SHA
  """
  xcom_query = to_sql_xcom(dag_id, execution_date)
  xcom_data = airflow_db.query(xcom_query)
  xcom_dict, green_sha = read_xcom_vars(xcom_data)
  return xcom_dict, green_sha


def state_from_string(state):
  """Transforms the state from a string format to an enumerated version.

  Args:
    state: string

  Returns:
    int
  """
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


def construct_links(green_sha):
  """Takes the green build sha and derives the repo links from that."""
  # this does nothing right now, but in the future it will get the links for
  # each release
  return ['https://youtu.be/dQw4w9WgXcQ']


def parse_dag_id(dag_id):
  """Parses the dag_id for the release branch and type.

  Args:
    dag_id: string

  Returns:
    branch: string
    release_type: string
  """
  underscore_count = 0
  last_underscore = False
  for i, char in enumerate(dag_id):
    if char == '_':
      underscore_count += 1
    if underscore_count == 1 and not last_underscore:
      last_underscore = i
    elif underscore_count == 2:
      last_underscore += 1
      release_type = dag_id[last_underscore:i]
      branch = dag_id[i+1:len(dag_id)]
      return branch, release_type


# TODO(dommarques): The data adapter should be able to:
# - take in the relevant raw sql data, such as the release data and task data
# - relate the tasks and releases
# - put this information into the unified storage format
