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
    if data is None:
      self._task = {}
    else:
      self._task = data

  @property
  def task_name(self):
    return self._task['task_name']

  @task_name.setter
  def task_name(self, value):
    """Sets name as string value."""
    if isinstance(value, basestring):
      self._task['task_name'] = value
    else:
      raise ValueError('Invalid input for task name: not a string')

  @property
  def dependent_on(self):
    return self._task['dependent_on']

  @dependent_on.setter
  def dependent_on(self, value):
    """Sets dependencies as list of string unique identifiers."""
    if isinstance(value, list):
      for task in value:
        if not isinstance(task, basestring):
          raise ValueError('Invalid input for dependency task: not a string')
      self._release['tasks'] = value
    else:
      raise ValueError('Invalid input for task dependencies: not an list')

  @property
  def started(self):
    return self._task['started']

  @started.setter
  def started(self, value):
    """Sets started as an int unix datetime."""
    if isinstance(value, int):
      self._task['started'] = value
    else:
      raise ValueError('Invalid input for task start datetime: not an int')

  @property
  def status(self):
    return self._task['status']

  @status.setter
  def status(self, value):
    """Sets status as int representation of status."""
    if isinstance(value, int):
      self._task['status'] = value
    else:
      raise ValueError('Invalid input for task status: not an int')

  @property
  def last_modified(self):
    return self._task['last_modified']

  @last_modified.setter
  def last_modified(self, value):
    """Sets last_modified as int unix datetime."""
    if isinstance(value, int):
      self._task['last_modified'] = value
    else:
      raise ValueError('Invalid input for last modified datetime: not an int')

  @property
  def log_url(self):
    return self._task['log_url']

  @log_url.setter
  def log_url(self, value):
    """Sets log_url as string url."""
    if isinstance(value, basestring):
      self._task['log_url'] = value
    else:
      raise ValueError('Invalid input for task log url: not a string')

  @property
  def error(self):
    return self._task['error']

  @error.setter
  def error(self, value):
    """Sets error as string."""
    if isinstance(value, basestring):
      self._task['error'] = value
    else:
      raise ValueError('Invalid input for task error: not a string')

  def to_dict(self):
    return self._task
