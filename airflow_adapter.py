"""The Airflow Adapter."""
from airflow_connector import AirflowDB
from from_sql import releases_from_sql
from release_data_abc import ReleaseData
from to_sql import sql_to_releases


class AirflowAdapter(ReleaseData):
  """It's the mythical Airflow Adapter!"""

  def __init__(self):
    self.airflow_db = AirflowDB()

  def get_releases(self, args):
    sql_query = sql_to_releases(args)  # build the SQL query
    sql_data = self.airflow_db.query(sql_query)
    releases_data = from_sql_releases(sql_data)

    return releases_data
