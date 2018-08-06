"""Converts the data from SQL to expected format."""
from collections import namedtuple
import json
import logging
import time
from adapters.to_sql import to_sql_tasks
from adapters.to_sql import to_sql_xcom
from data.release import Release
from data.state import State
from data.state import STRING_FROM_STATE
from data.state import STATE_FROM_STRING
from data.task import Task
from data.xcom_keys import xcomKeys
try:
  from google.appengine.api import urlfetch
except ImportError:
  import requests
import xml.etree.ElementTree as ElementTree



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
    item = release_named_tuple(*item)
    release = Release()  # initialize the release object
    execution_date = item.execution_date
    started = int(time.mktime(execution_date.timetuple()))
    task_ids, most_recent_task, state = get_task_info(item.dag_id, started, airflow_db)
    xcom_dict, green_sha = get_xcom(started, item.dag_id, airflow_db)
    release.release_id = item.dag_id + '@' + str(item.execution_date)
    release.tasks = task_ids
    release.started = int(started)
    release.labels = [item.dag_id]
    release.state = state
    if green_sha is None:
      release.links = [{'name': 'no links available', 'url': None}]
    else:
      release.links = construct_repo_links(green_sha)  # TODO(dommarques) these need to be implemented into airflow first, or we make our own way to get the links pylint: disable=line-too-long
    if xcom_dict is None:
      continue
    else:
      release.name = xcom_dict[xcomKeys.VERSION]
      try:
        release.branch = xcom_dict[xcomKeys.BRANCH]
        release.download_link = construct_download_link(xcom_dict[xcomKeys.GCS_BUILD_PATH])
      except KeyError:
        _, release.branch = parse_dag_id(item.dag_id)
      try:
        # it seems that some xcom dicts do not have this value for some reason?
        release.release_type = xcom_dict[xcomKeys.RELEASE_TYPE]
      except KeyError:
        # old releases don't have release types, so this is a fallback
        release.release_type, _ = parse_dag_id(item.dag_id)
    if most_recent_task:
      # allows for continuation even if tasks have not begun/been generated yet
      last_modified = most_recent_task.last_modified
      release.last_modified = int(time.mktime(last_modified.timetuple()))
      release.last_active_task = most_recent_task.task_name
    else:
      release.last_modified = int(time.mktime(execution_date.timetuple()))
      release.last_active_task = ''
    release_objects[release.release_id] = release
    logging.info('Release ' + str(release.release_id) + ' has been read')

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
    item = task_named_tuple(*item)
    task.task_name = item.task_id
    task.add_dependency = None  # TODO(dommarques): figure out how to get this - dag info?
    if item.start_date is None:
      execution_date = item.execution_date
      task.started = int(time.mktime(execution_date.timetuple()))
    else:
      start_date = item.start_date
      task.started = int(time.mktime(start_date.timetuple()))
    task.log_url = construct_log_link(item.dag_id, item.execution_date, item.task_id)  # TODO(dommarques): figure out how to get the log in here
    if item.end_date is None:
      if item.start_date is None:
        execution_date = item.execution_date
        task.last_modified = int(time.mktime(execution_date.timetuple()))
      else:
        start_date = item.start_date
        task.last_modified = int(time.mktime(start_date.timetuple()))
    else:
      end_date = item.end_date
      task.last_modified = int(time.mktime(end_date.timetuple()))
    if item.state is None:
      task.status = STATE_FROM_STRING.get('not_started')
      task.error = 'not started'
    elif item.state == 'running':
      task.status = STATE_FROM_STRING.get('running')
      task.error = STRING_FROM_STATE.get(task.status)
    elif item.start_date is None:
      task.status = STATE_FROM_STRING.get('queued')
      task.error = item.state
    else:
      task.error = item.state
      if str(item.state) in STATE_FROM_STRING:
        task.status = STATE_FROM_STRING.get(str(item.state))
      else:
        task.status = STATE_FROM_STRING.get('none')
    task_objects.append(task)
  return task_objects


def get_task_info(dag_id, execution_date, airflow_db):
  """Gets task-related info to fill in missing release object info.

  Args:
    dag_id: str
    execution_date: a python datetime.datetime
    airflow_db: the database connection object

  Returns:
    most_recent_task: the most recent active task
    state: the state of the release based on the task states
  """
  task_query = to_sql_tasks(dag_id, execution_date)
  task_data = airflow_db.query(task_query)
  task_objects = read_tasks(task_data)
  state = 1
  task_ids = []
  if task_objects:
    most_recent_task = task_objects[-1]
  else:
    most_recent_task = None
  for task in task_objects:
    task_ids.append(task.task_name)
    if state == STATE_FROM_STRING.get('failed'):
      continue
    elif task.status == STATE_FROM_STRING.get('failed'):
      state = task.status
      most_recent_task = task
    elif task.status == STATE_FROM_STRING.get('running'):
      state = task.status
      most_recent_task = task
    elif task.status > state:
      state = task.status
    logging.debug(task.status)
  return task_ids, most_recent_task, state


def read_xcom_vars(xcom_data):
  """Reads the xcom data to get the dict of vars and the green build SHA."""
  # occasionally, the xcom data doesn't exist yet. This is a workaround

  # The index 0 is here because the data returns in a tuple
  try:
    xcom_dict = xcom_data[0][0]
    if len(xcom_data) > 1:
      green_sha = xcom_data[1][0]
    else:
      green_sha = None
    logging.info('Data from xcom: ' + str(xcom_dict))
    logging.info('SHA: ' + str(green_sha))
    xcom_dict = json.loads(xcom_dict)
    return xcom_dict, green_sha
  except IndexError:
    logging.debug('Index Error')
    return None, None
  except TypeError:
    logging.debug('Type Error')
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
  if type(xcom_dict) == type({'hello':'world'}):
    return xcom_dict, green_sha
  else:
    return None, green_sha


def construct_repo_links(green_sha):
  """Takes the green build sha and derives the repo links from that."""
  response = []
  # get rid of the quotes that enclose the SHA
  green_sha = green_sha.replace('"', '').strip()
  green_build_link = 'https://github.com/istio/green-builds/blob/' + green_sha  + '/build.xml'
  response.append({'name': 'istio/green-builds', 'url':green_build_link})
  request_link = 'https://raw.githubusercontent.com/istio/green-builds/' + green_sha + '/build.xml'
  try:  # allows for local running, and for read_db.py to run
    r = urlfetch.fetch(request_link)
    data = ElementTree.fromstring(r.content)
  except NameError:
    r = requests.get(request_link)
    data = ElementTree.fromstring(r.text)
  for project in data.iter('project'):
    link_dict = {}
    name = project.attrib['name']
    sha = project.attrib['revision']
    link = 'https://github.com/' + name + '/commit/' + sha
    link_dict['name'] = name
    link_dict['url'] = link
    response.append(link_dict)
  logging.info('Links constructed:' + str(link_dict))
  return response


def construct_log_link(dag_id, execution_date, task_id):
  url = 'https://istio-release-ui.appspot.com/logs'
  url += '?release_id=' + str(dag_id) + '@' + str(execution_date)
  url += '&task_name=' + str(task_id)
  return url


def construct_download_link(gcs_build_path):
  link = 'https://gcsweb.istio.io/gcs/'
  link += gcs_build_path
  return link


def parse_dag_id(dag_id):
  """Parses the dag_id for the release branch and type.

  Args:
    dag_id: string

  Returns:
    branch: string
    release_type: string
  """
  info = dag_id.split('_')
  if len(info) in [2, 3]:
    return info[-2], info[-1]
