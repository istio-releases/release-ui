"""The Airflow Adapter."""
from datetime import datetime
import threading
from adapter_abc import Adapter
from from_sql import read_releases
from from_sql import read_tasks
from resources.filter_releases import filter_releases
from resources.filter_releases import sort
from to_sql import to_sql_releases
from to_sql import to_sql_release
from to_sql import to_sql_task
from to_sql import to_sql_tasks
import logging
from resources.dag_name_parser import dag_name_parser
import time

CACHE_TTL = 1800

class AirflowAdapter(Adapter):
  """Provides a way to interact with the Airflow Database, and get data from it."""

  def __init__(self, airflow_db):
    self._airflow_db = airflow_db
    self._lock = threading.Lock()
    self._release_types = set()
    self._branches = set()
    self._cache_last_updated = datetime.fromtimestamp(0)
    self._update_cache()

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
    releases_data = read_releases(release_data, self._airflow_db)
    # filter for the stuff that SQL can't natively filter for,
    # due to some data being based on a tasks
    releases_data = filter_releases(releases_data, filter_options)
    # sort with the stuff that SQL can't natively sort according to,
    # due to some data being based on tasks
    releases_data = sort(releases_data, filter_options)

    return releases_data

  def get_release(self, release_name):
    dag_id, execution_date = dag_name_parser(release_name)
    # construct SQL query
    release_query = to_sql_release(dag_id, execution_date)
    # get data from SQL
    release_data = self._airflow_db.query(release_query)
    # package data into a release object
    release_data = read_releases(release_data, self._airflow_db)

    return release_data

  def get_tasks(self, dag_name):
    """Retrieve all task information.

    Args:
      dag_id: str
      execution_date: unix format

    Returns:
      Dictionary of Task objects.
    """
    dag_id, execution_date = dag_name_parser(dag_name)
    execution_date = time.mktime(execution_date.timetuple())
    # build SQl query
    task_query = to_sql_tasks(execution_date)
    # get data from SQL
    task_data = self._airflow_db.query(task_query)
    # package data into task objects
    task_objects = read_tasks(task_data)

    return task_objects

  def get_task(self, task_name, dag_name):
    dag_id, execution_date = dag_name_parser(dag_name)
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

  def _update_cache(self):
    if (datetime.now() - self._cache_last_updated).total_seconds() < CACHE_TTL:
      return
    else:
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
