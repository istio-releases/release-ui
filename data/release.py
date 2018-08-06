"""Data format for Release."""

from datetime import datetime
from state import State


class Release(object):
  """Class for Release Object."""

  def __init__(self, data=None):
    """Initializes a release.

    Args:
      data: dictionary with all the release data (optional).
    """
    self._release = {}
    if data:
      self.release_id = data['release_id']
      self.name = data['name']
      self.tasks = data['tasks']
      self.links = data['links']
      self.started = data['started']
      self.state = data['state']
      self.last_active_task = data['last_active_task']
      self.last_modified = data['last_modified']
      self.branch = data['branch']
      self.release_type = data['release_type']
      self.download_link = data['download_link']

  def _validate_type(self, check, value, attribute):
    """Helper function to validate setter values and set attributes."""
    if isinstance(value, check):
      return True
    else:
      error = 'Invalid input for ' + attribute + ': not a ' + check.__name__
      error += ', instead got a ' + str(type(value))
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

  def _validate_datetime(self, value, attribute):
    """Helper function to validate date types and set attribute."""
    if self._validate_type(int, value, attribute):
      time = datetime.fromtimestamp(value)
      if time >= datetime.fromtimestamp(0) and time <= datetime.now():
        self._release[attribute] = time
      else:
        error = 'Invalid input for ' + attribute + ': not within datetime range'
        raise ValueError(error)

  @property
  def release_id(self):
    return str(self._release['release_id'])

  @release_id.setter
  def release_id(self, value):
    """Sets name as string value."""
    if self._validate_type(basestring, value, 'release_id'):
      self._release['release_id'] = value

  @property
  def name(self):
    return str(self._release['name'])

  @name.setter
  def name(self, value):
    """Sets name as string value."""
    if self._validate_type(basestring, value, 'name'):
      self._release['name'] = value

  @property
  def tasks(self):
    return self._release['tasks']

  @tasks.setter
  def tasks(self, value):
    """Sets tasks as string unique ids list, if combined with execution_date."""
    self._validate_array(basestring, value, 'tasks')

  @property
  def links(self):
    return self._release['links']

  @links.setter
  def links(self, value):
    """Sets links as list of string urls."""
    self._validate_array(dict, value, 'links')

  @property
  def started(self):
    return self._release['started']

  @started.setter
  def started(self, value):
    """Sets started as an int unix datetime."""
    self._validate_datetime(value, 'started')

  @property
  def labels(self):
    return self._release['labels']

  @labels.setter
  def labels(self, value):
    """Sets labels as list of string labels."""
    self._validate_array(basestring, value, 'labels')

  @property
  def state(self):
    return int(self._release['state'])

  @state.setter
  def state(self, value):
    """Sets state as State."""
    if State.is_valid(value):
      state = value
    else:
      raise ValueError('Invalid input for status')
    self._release['state'] = state

  @property
  def last_modified(self):
    return self._release['last_modified']

  @last_modified.setter
  def last_modified(self, value):
    """Sets last_modified as int unix datetime."""
    self._validate_datetime(value, 'last_modified')

  @property
  def last_active_task(self):
    return str(self._release['last_active_task'])

  @last_active_task.setter
  def last_active_task(self, value):
    """Sets last_active_task as a string unique identifier for a task."""
    if self._validate_type(basestring, value, 'last_active_task'):
      self._release['last_active_task'] = value

  @property
  def branch(self):
    return str(self._release['branch'])

  @branch.setter
  def branch(self, value):
    """Sets branch as a string branch name."""
    if self._validate_type(basestring, value, 'branch'):
      self._release['branch'] = value

  @property
  def release_type(self):
    return str(self._release['release_type'])

  @release_type.setter
  def release_type(self, value):
    """Sets release_type as a string release_type name."""
    if self._validate_type(basestring, value, 'release_type'):
      self._release['release_type'] = value.lower()

  @property
  def download_link(self):
    return str(self._release['download_link'])

  @download_link.setter
  def download_link(self, value):
    """Sets release_type as a string release_type name."""
    if self._validate_type(basestring, value, 'download_link'):
      self._release['download_link'] = value.lower()

  def to_json(self):
    returner = self._release.copy()
    unix = datetime.fromtimestamp(0)
    returner['started'] = (self.started - unix).total_seconds()
    returner['last_modified'] = (self.last_modified - unix).total_seconds()
    return returner
