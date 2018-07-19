"""Parses the release_id for dag_id and execution_date."""
from datetime import datetime
from to_timestamp import to_timestamp


def dag_name_parser(dag_name):
  for i, char in enumerate(dag_name):
    if char == '@':
      dag_id = dag_name[0:i]
      execution_date = dag_name[i+1:len(dag_name)]
      try:
        execution_date = datetime.strptime(str(execution_date), '%Y-%m-%d %H:%M:%S')
      except:
        execution_date = datetime.strptime(str(execution_date), '%Y-%m-%d %H:%M:%S.%f')

  return dag_id, execution_date
