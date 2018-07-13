"""REST API."""
import json
import os
import MySQLdb
from airflow_connector import AirflowDB
from file_adapter import FileAdapter
from filter_releases import filter_releases
from filter_releases import sort
from flask_restful import reqparse
from flask_restful import Resource
from airflow_adapter import AirflowAdapter
# from main import airflow_db
# from main import db_connection

# adapter = FileAdapter('fake_data/fake_release_data.json', 'fake_data/fake_task_data.json')
release_requests = {}
# initiate a connection with the airflow database
cloudsql_unix_socket = os.path.join('/cloudsql', 'istio-release-ui:us-central1:prod-airflow-snapshot-sandbox')
db_connection = MySQLdb.connect(
    unix_socket=cloudsql_unix_socket,
    host='35.193.234.53',
    user='root',
    passwd='',
    db='airflow-db')
airflow_db = AirflowDB(db_connection=db_connection)
adapter = AirflowAdapter(airflow_db=airflow_db)


def in_cache(args):
  """Checks if request arguments are in cache."""

  # parse args into different parameters
  start_date = hex(int(args['start_date']))
  end_date = hex(int(args['end_date']))
  datetype = str(args['datetype'])
  state = str(int(args['state']))
  branch = str(args['branch'])
  release_type = str(args['release_type'])
  sort_method = str(int(args['sort_method']))
  descending = str(args['descending'])

  # create an autogenerated key for cache
  key = start_date + end_date + datetype + state + branch + release_type + sort_method + descending

  # check if key has already been requested
  if key in release_requests:
    return key, release_requests[key]
  else:
    return False, key


def to_json(objects):
  """Turns list of objects (tasks or releases) to json."""
  output = []
  for item in objects:
    output.append(item.to_json())
  return json.dumps(output)


class Releases(Resource):
  """"Resource for all releases GET request."""

  def get(self):
    # parse the post request for the requisite info
    parser = reqparse.RequestParser()
    parser.add_argument('start_date')
    parser.add_argument('end_date')
    parser.add_argument('datetype')
    parser.add_argument('state')
    parser.add_argument('branch')
    parser.add_argument('release_type')
    parser.add_argument('sort_method')
    parser.add_argument('limit')
    parser.add_argument('offset')
    parser.add_argument('descending')
    args = parser.parse_args()
    print args
    if not bool(args['descending']):
      args['descending'] = 1

    # check if limit and offset exist, if not provide defaults
    if not args['limit']:
      args['limit'] = 100
    if not args['offset']:
      args['offset'] = 0

    # define start and end of desired array section
    array_from = int(args['offset'])
    array_to = int(args['limit'])+int(args['offset'])

    # checks if the filtered, sorted data is already in memcache

    # cache_exists, cache_results = in_cache(args)
    # if cache_exists:
    #   return to_json(cache_results[array_from:array_to])
    # else:
    #   # filter and sort all releases with given parsed arguments
    #   response = filter_releases(adapter.get_releases(), args['state'], args['branch'], args['release_type'], args['start_date'], args['end_date'], args['datetype'], args['descending'])
    #   response = sort(response, args['sort_method'])
    #   release_requests[cache_results] = response

      # returns a jsonified array with the determined start and end indices
    response = adapter.get_releases(start_date=float(args['start_date']),
                                    end_date=float(args['end_date']),
                                    datetype=str(args['datetype']),
                                    state=int(args['state']),
                                    branch=str(args['branch'])
                                    release_type=str(args['release_type'])
                                    sort_method=int(args['sort_method']),
                                    descending=int(args['descending']))
    print response
    return to_json(response[array_from:array_to])


class Release(Resource):
  """"Resource for single release GET request."""

  def get(self):
    parser = reqparse.RequestParser()
    parser.add_argument('release')
    args = parser.parse_args()

    return json.dumps(adapter.get_release(str(args['release'])).to_json())


class Branches(Resource):
  """"Resource for Branches GET request."""

  def get(self):
    return json.dumps(adapter.get_branches())


class Types(Resource):
  """"Resource for types GET request."""

  def get(self):
    return json.dumps(adapter.get_types())


class Tasks(Resource):
  """"Resource for tasks GET request."""

  def get(self):
    parser = reqparse.RequestParser()
    parser.add_argument('release')
    args = parser.parse_args()

    release_tasks = adapter.get_release(str(args['release'])).tasks
    response = []
    for task in release_tasks:
      response.append(adapter.get_task('task-' + str(task)))

    return to_json(response)


class AirflowDBTesting(Resource):
  """Allows for SQL queries to be sent to App Engine through an HTTP GET request. FOR TESTING ONLY, WILL BE DELETED."""  # pylint: disable=line-too-long

  def get(self):
    parser = reqparse.RequestParser()
    parser.add_argument('cm')
    parser.add_argument('start_date')
    parser.add_argument('end_date')
    parser.add_argument('datetype')
    parser.add_argument('state')
    parser.add_argument('label')
    parser.add_argument('sort_method')
    parser.add_argument('limit')
    parser.add_argument('offset')
    args = parser.parse_args()
    data = airflow_db.query(str(args['cm']))
    print type(data)
    print data[1]


class Resources(object):

  def __init__(self):
    self.releases = Releases
    self.release = Release
    self.branches = Branches
    self.types = Types
    self.tasks = Tasks
    self.airflowdb = AirflowDBTesting  # TODO(dommarques): delete when finished with testing pylint: disable=line-too-long
