"""Data format for Task."""

from datetime import datetime
from state import State


class Task(object):
  """Class for Task Object."""

  def __init__(self, data=None):
    """Initializes a task.

    Args:
      data: dictionary with all the task data (optional).
    """
    self._task = {}
    if data:
      self.task_name = data['task_name']
      self._task['dependent_on'] = []
      self.started = data['started']
      self.status = data['status']
      self.last_modified = data['last_modified']
      self.log_url = data['log_url']
      self.error = data['error']

  def _validate_type(self, check, value, attribute):
    """Helper function to validate setter value types."""
    if isinstance(value, check):
      return True
    else:
      error = 'Invalid input for ' + attribute + ': not a ' + check.__name__
      error += ', instead got a ' + str(type(value))
      raise ValueError(error)

  def _validate_datetime(self, value, attribute):
    """Helper function to validate date types and set attribute."""
    if self._validate_type(int, value, attribute):
      time = datetime.fromtimestamp(value)
      if time >= datetime.fromtimestamp(0) and time <= datetime.now():
        self._task[attribute] = time
      else:
        error = 'Invalid input for ' + attribute + ': not within datetime range'
        raise ValueError(error)

  @property
  def task_name(self):
    return str(self._task['task_name'])

  @task_name.setter
  def task_name(self, value):
    """Sets name as string value."""
    if self._validate_type(basestring, value, 'task_name'):
      self._task['task_name'] = value

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
    """Sets started as a datetime."""
    self._validate_datetime(value, 'started')

  @property
  def status(self):
    return int(self._task['status'])

  @status.setter
  def status(self, value):
    """Sets status as State."""
    if State.is_valid(value):
      status = value
    else:
      raise ValueError('Invalid input for status')
    self._task['status'] = status

  @property
  def last_modified(self):
    return self._task['last_modified']

  @last_modified.setter
  def last_modified(self, value):
    """Sets last_modified as a datetime."""
    self._validate_datetime(value, 'last_modified')

  @property
  def log_url(self):
    return str(self._task['log_url'])

  @log_url.setter
  def log_url(self, value):
    """Sets log_url as string url."""
    if self._validate_type(basestring, value, 'log_url'):
      self._task['log_url'] = value

  @property
  def error(self):
    return str(self._task['error'])

  @error.setter
  def error(self, value):
    """Sets error as string."""
    if self._validate_type(basestring, value, 'error'):
      self._task['error'] = value

  def to_json(self):
    returner = self._task.copy()
    unix = datetime.fromtimestamp(0)
    returner['started'] = (self.started - unix).total_seconds()
    returner['last_modified'] = (self.last_modified - unix).total_seconds()
    return returner
