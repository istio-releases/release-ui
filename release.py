"""Data format for Release."""


class State(object):
  UNUSED_STATUS = 0
  PENDING = 1
  FINISHED = 2
  FAILED = 3
  ABANDONED = 4


class Release(object):
  """Class for Release Object."""

  def __init__(self, data=None):
    """Initializes a release.

    Args:
      data: dictionary with all the release data (optional).
    """
    self._release = data or {}

  def _validate(self, check, value, attribute):
    """Helper function to validate setter values and set attributes."""
    if isinstance(value, check):
      self._release[attribute] = value
    else:
      error = 'Invalid input for ' + attribute + ': not a ' + check.__name__
      raise ValueError(error)

  def _validate_array(self, check, value, attribute):
    """Helper function to validate setter list values and set attributes."""
    if isinstance(value, list):
      for item in value:
        if not isinstance(item, check):
          error = 'Invalid input for ' + attribute + ': not a ' + check.__name__
          raise ValueError(error)
      self._release[attribute] = value
    else:
      error = 'Invalid input for ' + attribute + ': not a list'
      raise ValueError(error)

  @property
  def name(self):
    return self._release['name']

  @name.setter
  def name(self, value):
    """Sets name as string value."""
    self._validate(basestring, value, 'name')

  @property
  def tasks(self):
    return self._release['tasks']

  @tasks.setter
  def tasks(self, value):
    """Sets tasks as list of int unique identifiers."""
    self._validate_array(int, value, 'tasks')

  @property
  def links(self):
    return self._release['links']

  @links.setter
  def links(self, value):
    """Sets links as list of string urls."""
    self._validate_array(basestring, value, 'links')

  @property
  def started(self):
    return self._release['started']

  @started.setter
  def started(self, value):
    """Sets started as an int unix datetime."""
    self._validate(int, value, 'started')

  @property
  def labels(self):
    return self._release['labels']

  @labels.setter
  def labels(self, value):
    """Sets labels as list of string labels."""
    self._validate_array(basestring, value, 'labels')

  @property
  def state(self):
    return self._release['state']

  @state.setter
  def state(self, value):
    """Sets state as int representation of state."""
    self._validate(int, value, 'state')

  @property
  def last_modified(self):
    return self._release['last_modified']

  @last_modified.setter
  def last_modified(self, value):
    """Sets last_modified as int unix datetime."""
    self._validate(int, value, 'last_modified')

  @property
  def last_active_task(self):
    return self._release['last_active_task']

  @last_active_task.setter
  def last_active_task(self, value):
    """Sets last_active_task as a string unique identifier for a task."""
    self._validate(basestring, value, 'last_active_task')

  def to_dict(self):
    return self._release.copy()
