"""The Airflow Adapter."""
from airflow_connector import AirflowDB
from from_sql import read_releases
from from_sql import read_tasks
from release_data_abc import ReleaseData
from to_sql import to_sql_release
from to_sql import to_sql_releases
from to_sql import to_sql_tasks


class AirflowAdapter(object):
  """It's the mythical Airflow Adapter!"""

  def __init__(self):
    self.airflow_db = AirflowDB(CLOUDSQL_CONNECTION_NAME='istio-release-ui:us-central1:prod-airflow-snapshot-sandbox',  # pylint: disable=line-too-long
                                CLOUDSQL_USER='root',
                                CLOUDSQL_PASSWORD='',
                                CLOUDSQL_HOST='35.193.234.53',
                                CLOUDSQL_DB='airflow-db')

  def get_tasks(self, execution_date):
    task_query = to_sql_tasks(execution_date)
    task_data = self.airflow_db.query(task_query)
    task_objects = read_tasks(task_data)
    return task_objects

  def get_releases(self, args):
    release_query = to_sql_releases(args)  # build the SQL query
    release_data = self.airflow_db.query(release_query)
    releases_data = read_releases(release_data=release_data)
    return releases_data

  def get_release(self, release_id):
    sql_query = to_sql_release(release_id)
