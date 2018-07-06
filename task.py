"""Data format for Task."""


class State(object):
  UNUSED_STATUS = 0
  PENDING = 1
  FINISHED = 2
  FAILED = 3
  ABANDONED = 4


class Task(object):
  """Class for Task Object."""

  def __init__(self, data=None):
    """Initializes a task.

    Args:
      data: dictionary with all the task data (optional).
    """
    self._task = data or {}

  def _validate(self, check, value, attribute):
    """Helper function to validate setter values and set attributes."""
    if isinstance(value, check):
      self._task[attribute] = value
    else:
      error = 'Invalid input for ' + attribute + ': not a ' + check.__name__
      raise ValueError(error)

  @property
  def task_name(self):
    return self._task['task_name']

  @task_name.setter
  def task_name(self, value):
    """Sets name as string value."""
    self._validate(basestring, value, 'task_name')

  @property
  def dependent_on(self):
    return self._task['dependent_on']

  def add_dependency(self, value):
    """Adds dependency to list of string unique identifiers."""
    if isinstance(value, basestring):
      if not hasattr(self, 'dependent_on'):
        self._task['dependent_on'] = []
      self._task['dependent_on'].append(value)
    else:
      raise ValueError('Invalid input for a dependency: not a string')

  @property
  def started(self):
    return self._task['started']

  @started.setter
  def started(self, value):
    """Sets started as an int unix datetime."""
    self._validate(int, value, 'started')

  @property
  def status(self):
    return self._task['status']

  @status.setter
  def status(self, value):
    """Sets status as int representation of status."""
    self._validate(int, value, 'status')

  @property
  def last_modified(self):
    return self._task['last_modified']

  @last_modified.setter
  def last_modified(self, value):
    """Sets last_modified as int unix datetime."""
    self._validate(int, value, 'last_modified')

  @property
  def log_url(self):
    return self._task['log_url']

  @log_url.setter
  def log_url(self, value):
    """Sets log_url as string url."""
    self._validate(basestring, value, 'log_url')

  @property
  def error(self):
    return self._task['error']

  @error.setter
  def error(self, value):
    """Sets error as string."""
    self._validate(basestring, value, 'error')

  def to_dict(self):
    return self._task.copy()
