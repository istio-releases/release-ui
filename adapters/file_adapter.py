"""File Adapter for Fake Data."""

import json
from adapter_abc import Adapter
from data.release import Release
from data.task import Task


class FileAdapter(Adapter):
  """Constructor takes two files: release data and task data"""

  def __init__(self, releases_file, tasks_file):
    with open(releases_file) as f:
      json_releases = f.read()
    releases_dict = json.loads(json_releases)
    self._releases = {}
    for key in releases_dict:
      releases_dict[key]['id'] = releases_dict[key]['name']
      release = Release(releases_dict[key])
      self._releases[key] = release

    with open(tasks_file) as f:
      json_tasks = f.read()
    tasks_dict = json.loads(json_tasks)
    self._tasks = {}
    for key in tasks_dict:
      task = Task(tasks_dict[key])
      self._tasks[key] = task

    branches = set()
    for release in self._releases:
      branches.add(self._releases[release].branch)
    self._branches = list(branches)

    release_types = set()
    for release in self._releases:
      release_types.add(self._releases[release].release_type)
    self._release_types = list(release_types)

  def get_releases(self):
    return self._releases

  def get_release(self, release_id):
    return self._releases[release_id]

  def get_tasks(self):
    return self._tasks

  def get_task(self, task_name):
    return self._tasks[task_name]

  def get_branches(self):
    return self._branches

  def get_release_types(self):
    return self._release_types
