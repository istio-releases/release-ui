"""Astract Base Class for Release Data."""

import abc

UNUSED_STATUS = 0
PENDING = 1
FINISHED = 2
FAILED = 3
ABANDONED = 4


class Release(object):
  """Class for Release Object."""

  def __init__(self, release_name):
    """Initializes a release with a specified name."""

    self.name = release_name
    self.tasks = []
    self.links = []
    self.started = 0
    self.labels = []
    self.state = UNUSED_STATUS
    self.last_modified = 0
    self.last_active_task = ""

  def from_dict(self, dict):
    for k, v in dict.iteritems():
      setattr(self, k, v)

  def to_dict(self):
    return self.__dict__


class Task(object):
  """Class for Task Instance Object."""

  def __init__(self, task_name):
    """Initializes a task instance with a specified name."""
    self.task_name = task_name
    self.status = UNUSED_STATUS
    self.log_url = ""
    self.started = 0
    self.dependent_on = []
    self.last_modified = 0
    self.error = ""

  def from_dict(self, dict):
    for k, v in dict.iteritems():
      self.k = v

  def to_dict(self):
    return self.__dict__


class ReleaseData(object):
  """ABC to retrieve data from File Adapter and Airflow Adapter."""

  __metaclass__ = abc.ABCMeta

  @abc.abstractmethod
  def get_releases(self):
    """Retrieve all release information."""
    pass

  @abc.abstractmethod
  def get_release(self, release_name):
    """Retrieve individual release information."""
    pass

  @abc.abstractmethod
  def get_tasks(self):
    """Retrieve all task information."""
    pass

  @abc.abstractmethod
  def get_task(self, task_name):
    """Retrieve individual task information."""
    pass

  @abc.abstractmethod
  def get_labels(self):
    """Retrieve all possible labels for UI."""
    pass
