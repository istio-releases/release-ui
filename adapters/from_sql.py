"""Converts the data from SQL to expected format."""
import json
from data.release import Release
from data.task import Task
from adapters.to_sql import to_sql_tasks
from adapters.to_sql import to_sql_xcom
from resources.to_timestamp import to_timestamp
from data.state import State
from collections import namedtuple
import logging

STATE_FROM_STRING = {'none': State.UNUSED_STATUS,
                     'running': State.PENDING,
                     'success': State.FINISHED,
                     'failed': State.FAILED,
                     'shutdown': State.ABANDONED,
                     'upstream_failed': State.PENDING}

def read_releases(release_data, airflow_db):
  """Reads in releases in the SQL tuple format, transforms them into objects.

  Args:
    release_data: the raw release data from SQL (tuple)
    airflow_db: the airflow database connection object

  Returns:
    release_objects
  """
  release_named_tuple = namedtuple('Row', ['dag_id', 'execution_date'])
  release_objects = {}  # resources.py expects a dict of objects
  for item in release_data:  # iterate through each release in release_data
    item = release_named_tuple._make(item)
    release = Release()  # initialize the release object
    started = to_timestamp(item.execution_date)
    task_ids, most_recent_task, state = get_task_info(started, airflow_db)
    xcom_dict, green_sha = get_xcom(started, item.dag_id, airflow_db)
    release.release_id = item.dag_id + '@' + str(item.execution_date)
    release.tasks = task_ids
    release.started = started
    release.links = construct_links(green_sha)  # TODO(dommarques) these need to be implemented into airflow first, or we make our own way to get the links pylint: disable=line-too-long
    release.labels = [item.dag_id]
    release.state = state
    release.branch, release.release_type = parse_dag_id(item.dag_id)
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
      release.last_modified = to_timestamp(item.execution_date)
      release.last_active_task = ''
    release_objects[release.release_id] = release

  return release_objects


def read_tasks(task_data):
  """Reads the tasks, transforms them into objects.

  Args:
    task_data: a tuple of tuples with task info

  Returns:
    task_objects
  """
  task_named_tuple = namedtuple('Row', ['task_id', 'dag_id', 'execution_date', 'start_date', 'end_date', 'state'])
  task_objects = []
  for item in task_data:
    task = Task()
    logging.debug(item)
    item = task_named_tuple._make(item)
    task.task_name = item.task_id
    task.add_dependency = None  # TODO(dommarques): figure out how to get this - dag info?
    if item.start_date == None:
      task.started = to_timestamp(item.execution_date)
    else:
      task.started = to_timestamp(item.start_date)
    if item.state == None:
      task.status = STATE_FROM_STRING.get('none')
    else:
      task.status = STATE_FROM_STRING.get(item.state)
    if item.end_date == None:
      task.last_modified = to_timestamp(item.execution_date)
    else:
      task.last_modified = to_timestamp(item.end_date)
    task.log_url = 'https://youtu.be/dQw4w9WgXcQ'  # TODO(dommarques): figure out how to get the log in here
    if item.state == None:
      item.state == 'none'
    else:
      task.error = item.state
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
  xcom_named_tuple = namedtuple('Row', ['xcom_dict', 'green_sha'])
  try:
    xcom_data = xcom_named_tuple._make(xcom_data)
    # The index 0 is here because the data returns in a tuple
    xcom_dict = json.loads(xcom_data.xcom_dict[0])
    green_sha = xcom_data.green_sha[0]
    return xcom_dict, green_sha
  except IndexError:
    return None, None
  except TypeError:
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
