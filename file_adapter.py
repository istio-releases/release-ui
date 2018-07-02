"""File Adapter for Fake Data."""

import json
from release_data_abc import ReleaseData


class FileAdapter(ReleaseData):
  """Constructor takes two files: release data and task data"""

  def load_releases(self, releases_file):
    json_data = open(releases_file).read()
    self.releases = json.loads(json_data)

  def load_tasks(self, tasks_file):
    json_data = open(tasks_file).read()
    self.tasks = json.loads(json_data)

  def get_releases(self):
    return self.releases

  def get_tasks(self):
    return self.tasks

  def get_labels(self):
    labels = []
    for release in self.releases:
      for label in self.releases[release]['labels']:
        if label not in labels:
          labels.append(label)
    return labels
