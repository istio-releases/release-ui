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
    if data is None:
      self._release = {}
    else:
      self._release = data

  @property
  def name(self):
    return self._release['name']

  @name.setter
  def name(self, value):
    """Sets name as string value."""
    if isinstance(value, basestring):
      self._release['name'] = value
    else:
      raise ValueError('Invalid input for release name: not a string')

  @property
  def tasks(self):
    return self._release['tasks']

  @tasks.setter
  def tasks(self, value):
    """Sets tasks as list of string unique identifiers."""
    if isinstance(value, list):
      for task in value:
        if not isinstance(task, basestring):
          raise ValueError('Invalid input for task key: not a string')
      self._release['tasks'] = value
    else:
      raise ValueError('Invalid input for release tasks: not an list')

  @property
  def links(self):
    return self._release['links']

  @links.setter
  def links(self, value):
    """Sets links as list of string urls."""
    if isinstance(value, list):
      for link in value:
        if not isinstance(link, basestring):
          raise ValueError('Invalid input for link: not a string')
      self._release['links'] = value
    else:
      raise ValueError('Invalid input for release links: not an list')

  @property
  def started(self):
    return self._release['started']

  @started.setter
  def started(self, value):
    """Sets started as an int unix datetime."""
    if isinstance(value, int):
      self._release['started'] = value
    else:
      raise ValueError('Invalid input for release start datetime: not an int')

  @property
  def labels(self):
    return self._release['labels']

  @labels.setter
  def labels(self, value):
    """Sets labels as list of string labels."""
    if isinstance(value, list):
      for label in value:
        if not isinstance(label, basestring):
          raise ValueError('Invalid input for label: not a string')
      self._release['labels'] = value
    else:
      raise ValueError('Invalid input for release labels: not an list')

  @property
  def state(self):
    return self._release['state']

  @state.setter
  def state(self, value):
    """Sets state as int representation of state."""
    if isinstance(value, int):
      self._release['state'] = value
    else:
      raise ValueError('Invalid input for release state: not an int')

  @property
  def last_modified(self):
    return self._release['last_modified']

  @last_modified.setter
  def last_modified(self, value):
    """Sets last_modified as int unix datetime."""
    if isinstance(value, int):
      self._release['last_modified'] = value
    else:
      raise ValueError('Invalid input for last modified datetime: not an int')

  @property
  def last_active_task(self):
    return self._release['last_active_task']

  @last_active_task.setter
  def last_active_task(self, value):
    """Sets last_active_task as a string unique identifier for a task."""
    if isinstance(value, basestring):
      self._release['last_active_task'] = value
    else:
      raise ValueError('Invalid input for last active task: not a string')

  def to_dict(self):
    return self._release
