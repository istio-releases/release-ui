"""File Adapter for Fake Data."""

import json
from adapter_abc import Adapter
from release_data import Release, Task


class FileAdapter(Adapter):
  """Constructor takes two files: release data and task data"""

  def __init__(self, releases_file, tasks_file):
    # read releases from file
    with open(releases_file) as f:
      json_releases = f.read()
    releases_dict = json.loads(json_releases)

    # convert file data to dictionary of release objects
    self.releases = {}
    for key in releases_dict:
      release = Release(key)
      release.from_dict(releases_dict[key])
      self.releases[key] = release

    # read tasks from file
    with open(tasks_file) as f:
      json_tasks = f.read()
    tasks_dict = json.loads(json_tasks)

    # convert file data to dictionary of task objects
    self.tasks = {}
    for key in tasks_dict:
      task = Task(key)
      task.from_dict(tasks_dict[key])
      self.tasks[key] = task

    # dynamically create list of labels from release input
    labels = set()
    for release in self.releases:
      for label in self.releases[release].labels:
        labels.add(label)
    self.labels = list(labels)

  def get_releases(self):
    return self.releases

  def get_release(self, release_name):
    return self.releases[release_name]

  def get_tasks(self):
    return self.tasks

  def get_task(self, task_name):
    return self.tasks[task_name]

  def get_labels(self):
    return self.labels
