"""File Adapter for Fake Data."""

import json
from release_data_abc import Release, Task, ReleaseData


class FileAdapter(ReleaseData):
  """Constructor takes two files: release data and task data"""

  def __init__(self, releases_file, tasks_file):
    with open(releases_file) as f:
      json_releases = f.read()

    releases_dict = json.loads(json_releases)
    self.releases = {}
    for key in releases_dict:
      release = Release(key)
      for k in releases_dict[key]:
        setattr(release, k, releases_dict[key][k])
      self.releases[key] = release

    with open(tasks_file) as f:
      json_tasks = f.read()

    tasks_dict = json.loads(json_tasks)
    self.tasks = {}
    for key in tasks_dict:
      task = Task(key)
      for k in tasks_dict[key]:
        setattr(task, k, tasks_dict[key][k])
      self.tasks[key] = task

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
