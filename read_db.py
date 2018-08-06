"""This script creates a json dump of the SQL database of releases.

Simply run it to get a dump of the release database in JSON format, at the
DUMP_FILE_NAME location.

It is designed to be run on a local workstation, and because of this the machine's
IP address must be whitelisted on the SQL database. It also requires MySQLdb to
be installed on the machine.
"""
import json
import time
from adapters.airflow_connector import AirflowDB
from adapters.from_sql import read_releases, read_tasks
from adapters.to_sql import to_sql_task
from resources.release_id_parser import release_id_parser


CLOUDSQL_CONNECTION_NAME = 't35db24833ba76815-tp:us-central1:us-central1-istio-release-e-79a693d8-sql'
CLOUDSQL_HOST = '35.193.234.53'
CLOUDSQL_USER = 'root'
CLOUDSQL_PASSWORD = ''
CLOUDSQL_DB = 'airflow-db'
GCS_LOGS_BUCKET = 'us-central1-istio-release-e-79a693d8-bucket'
DUMP_FILE_NAME = 'data/data_dump/release_dump.json'  # what you want the new json file to be called

airflow_db = AirflowDB(host=CLOUDSQL_HOST,
                       user=CLOUDSQL_USER,
                       password=CLOUDSQL_PASSWORD,
                       db=CLOUDSQL_DB)

raw_release_data = airflow_db.query('SELECT dag_id, execution_date FROM dag_run')
release_objects = read_releases(raw_release_data, airflow_db)

releases = {}
releases_read = 0
for release in release_objects.values():
  releases_read += 1
  tasks = []
  release_id = release.release_id
  dag_id, execution_date = release_id_parser(release_id)
  execution_date = int(time.mktime(execution_date.timetuple()))
  for task in release.tasks:
    sql_query = to_sql_task(dag_id, task, execution_date)
    raw_task_data = airflow_db.query(sql_query)
    task_data = read_tasks(raw_task_data)
    task = task_data[0].to_json()
    task['last_modified'] = int(task['last_modified'])
    task['started'] = int(task['started'])
    tasks.append(task)
  release = release.to_json()
  release['tasks'] = tasks
  release['started'] = int(release['started'])
  release['last_modified'] = int(release['last_modified'])
  releases[release_id] = release
  print 'Release "%s" downloaded' % release_id


target_file = open(DUMP_FILE_NAME, 'w+')
json.dump(releases, target_file, indent=2)
print 'File created as "%s", containing information for %i releases' % (DUMP_FILE_NAME, releases_read)
