"""Parses the release_id for dag_id and execution_date."""
from datetime import datetime


def dag_name_parser(dag_name):
  info = dag_name.split('@')
  dag_id = info[0]
  execution_date = info[1]
  try:
    execution_date = datetime.strptime(str(execution_date), '%Y-%m-%d %H:%M:%S')
  except:
    execution_date = datetime.strptime(str(execution_date), '%Y-%m-%d %H:%M:%S.%f')

  return dag_id, execution_date
