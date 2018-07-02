"""Data format for Release and Task objects."""

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
