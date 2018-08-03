"""The Airflow Adapter."""
import os
import json
from datetime import datetime
import logging
import threading
import time
from adapter_abc import Adapter
from from_sql import read_releases
from from_sql import read_tasks
import lib.cloudstorage as gcs
from resources.filter_releases import filter_releases
from resources.filter_releases import sort
from resources.release_id_parser import release_id_parser
from to_sql import to_sql_release
from to_sql import to_sql_releases
from to_sql import to_sql_task
from to_sql import to_sql_tasks
from data.release import Release
from data.task import Task


CACHE_TTL = 1800

class AirflowAdapter(Adapter):
  """Provides a way to interact with the Airflow Database, and get data from it."""

  def __init__(self, airflow_db):
    self._airflow_db = airflow_db
    self._lock = threading.Lock()
    self._release_types = set()
    self._branches = set()
    self._cache_last_updated = datetime.fromtimestamp(0)
    self._releases = {}
    self._tasks = {}
    self._update_cache()
    self._load_dump('data/data_dump/release_dump.json')

  def get_releases(self, filter_options):
    """Gets all releases fitting filter_options.

    Args:
      filter_options: object containing all filter parameters

    Returns:
      releases_data: a filtered, sorted list of release objects
    """
    # build the SQL query
    release_query = to_sql_releases(filter_options)
    # get the data from SQL
    release_data = self._airflow_db.query(release_query)
    # package the data into release objects with all neccessary info
    releases_data = self._releases
    # reading the SQL data after the data dump ensures the most up-to-date
    # info is shown
    releases_data.update(read_releases(release_data, self._airflow_db))
    # filter for the stuff that SQL can't natively filter for,
    # due to some data being based on a tasks
    releases_data = filter_releases(releases_data, filter_options)
    # sort with the stuff that SQL can't natively sort according to,
    # due to some data being based on tasks
    releases_data = sort(releases_data, filter_options)

    return releases_data

  def get_release(self, release_id):
    """Gets a single release, defined by release_id.

    Args:
      release_id: str, unique release identifier

    Returns:
      release_data: a release object in a list
    """
    dag_id, execution_date = release_id_parser(release_id)
    # construct SQL query
    release_query = to_sql_release(dag_id, execution_date)
    # get data from SQL
    release_data = self._airflow_db.query(release_query)
    # package data into a release object
    release_data = read_releases(release_data, self._airflow_db)

    return release_data

  def get_tasks(self, release_id):
    """Retrieve all task information.

    Args:
      release_id: str, unique release identifier

    Returns:
      Dictionary of Task objects.
    """
    if release_id in self._releases:
      tasks = json.loads(self._releases['release_id'].tasks)
      task_objects = []
      for k, v in tasks:
        task_objects.append(Task(v))
      return task_objects
    dag_id, execution_date = release_id_parser(release_id)
    execution_date = time.mktime(execution_date.timetuple())
    # build SQl query
    task_query = to_sql_tasks(execution_date)
    # get data from SQL
    task_data = self._airflow_db.query(task_query)
    # package data into task objects
    task_objects = read_tasks(task_data)

    return task_objects

  def get_task(self, task_name, release_id):

    """Retrieves a task object.

    Args:
      task_name: str
      release_id: str, unique release identifier

    Returns:
      Dictionary with Task object.
    """
    if release_id in self._releases:
      return self._tasks[task_name]


    dag_id, execution_date = release_id_parser(release_id)
    execution_date = time.mktime(execution_date.timetuple())

    task_query = to_sql_task(dag_id, task_name, execution_date)
    task_data = self._airflow_db.query(task_query)
    task_data = read_tasks(task_data)

    return task_data

  def get_labels(self):
    """Retrieve all possible labels for UI.

    Returns:
      Array of labels as strings.
    """
    pass

  def get_branches(self):
    """Retrieve all possible branches for UI.

    Returns:
      Array of branches as strings.
    """
    # check if cache is older than CACHE_TTL secs. If true, then update cache
    self._update_cache()
    with self._lock:
      return self._branches

  def get_release_types(self):
    """Retrieve all possible types for UI.

    Returns:
      Array of types as strings.
    """
    self._update_cache()
    with self._lock:
      return self._release_types

  def get_logs(self, bucket_name, release_id, task_name, log_file='1.log'):
    """Gets the logs for a task from GCS.

    Args:
      bucket_name: str
      release_id: str
      task_name: str
      log_file: str

    Returns:
      Structured log text
    """
    dag_id, execution_date = release_id_parser(release_id)
    execution_date = str(execution_date).replace(' ', 'T')  # put into same format as gcs bucket
    filename = os.path.join(os.path.sep, bucket_name , 'logs' , dag_id , task_name, str(execution_date),  log_file)
    gcs_file = gcs.open(filename)
    contents = gcs_file.read()
    gcs_file.close()
    return contents

  def _load_dump(self, filename):
    with open(filename) as f:
      releases = f.read()
    releases = json.loads(releases)

    for k, v in releases.iteritems():
      task_ids = []
      for task in v['tasks']:
        task_id = task['task_name'] + '@' + k
        self._tasks[task_id] = Task(task)
        task_ids.append(task_id)
      v['tasks'] = task_ids
      self._releases[k] = Release(v)
    logging.info('Releases read from %s' % filename)

  def _update_cache(self):
    if (datetime.now() - self._cache_last_updated).total_seconds() < CACHE_TTL:
      return

    logging.info('Type and Branch cache updated')
    raw_release_data = self._airflow_db.query('SELECT dag_id, execution_date FROM dag_run;')
    releases = read_releases(raw_release_data, self._airflow_db)
    branches = set()
    types = set()
    for release in releases:
      branches.add(releases[release].branch)
      types.add(releases[release].release_type)

      with self._lock:
        self._branches = list(branches)
        self._release_types = list(types)
        self._cache_last_updated = datetime.now()
