import datetime
from to_timestamp import to_timestamp

def dag_name_parser(dag_name):
  for i, char in enumerate(dag_name):
    if char == '@':
      dag_id = dag_name[0:i]
      execution_date = [i+1:len(dag_name)]
      execution_date = strptime(execution_date, '%Y-%m-%d %H:%m:%S.%f')
      execution_date = to_timestamp(execution_date)

  return dag_id, execution_date
