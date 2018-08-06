"""REST API."""
import json
import logging
from data.filter_options import FilterOptions
from flask_restful import reqparse
from flask_restful import Resource
from flask import render_template

release_requests = {}


def to_json(objects):
  """Turns list of objects (tasks or releases) to json."""
  output = []
  for item in objects:
    output.append(item.to_json())
  return json.dumps(output)


class Releases(Resource):
  """"Resource for all releases GET request."""

  def __init__(self, adapter):
    self._adapter = adapter

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

    # check if limit and offset exist, if not provide defaults
    if not args['limit']:
      args['limit'] = 100
    if not args['offset']:
      args['offset'] = 0

    # define start and end of desired array section
    array_from = int(args['offset'])
    array_to = int(args['limit'])+int(args['offset'])

    filter_options = FilterOptions(args)

    response = self._adapter.get_releases(filter_options)

    # returns a jsonified array with the determined start and end indices
    response = to_json(response[array_from:array_to])
    return response


class Release(Resource):
  """"Resource for single release GET request."""

  def __init__(self, adapter):
    self._adapter = adapter

  def get(self):
    parser = reqparse.RequestParser()
    parser.add_argument('release')
    args = parser.parse_args()

    response = self._adapter.get_release(str(args['release']))
    response = response[str(args['release'])].to_json()
    return response


class Branches(Resource):
  """"Resource for Branches GET request."""

  def __init__(self, adapter):
    self._adapter = adapter

  def get(self):
    return json.dumps(self._adapter.get_branches())


class Types(Resource):
  """"Resource for types GET request."""

  def __init__(self, adapter):
    self._adapter = adapter

  def get(self):
    return json.dumps(self._adapter.get_release_types())


class Tasks(Resource):
  """"Resource for tasks GET request."""

  def __init__(self, adapter):
    self._adapter = adapter

  def get(self):
    parser = reqparse.RequestParser()
    parser.add_argument('release')
    args = parser.parse_args()

    release = self._adapter.get_release(str(args['release']))
    release_tasks = release[str(args['release'])].tasks
    task_objects = []
    for task_id in release_tasks:
      task_object = self._adapter.get_task(task_id, str(args['release']))
      task_object = task_object[0]
      task_objects.append(task_object)
    response = to_json(task_objects)
    return response


class Logs(Resource):
  def __init__(self, adapter, bucket_name):
    self._adapter = adapter
    self._bucket_name = bucket_name

  def get(self):
    parser = reqparse.RequestParser()
    parser.add_argument('release_id')
    parser.add_argument('task_name')
    args = parser.parse_args()
    logging.debug('Release id: ' + str(args['release_id']))
    logging.debug('Task name: ' + str(args['task_name']))

    response = self._adapter.get_logs(str(args['release_id']), str(args['task_name']))
    return json.dumps(response)


class OverallStatus(Resource):
  def __init__(self, adapter):
    self._adapter = adapter

  def get(self):
    response = self._adapter.get_overall_status()
    return json.dumps(response)
