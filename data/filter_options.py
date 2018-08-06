"""Data format for Release."""
from state import State


class FilterOptions(object):
  """Class for Release Object."""

  def __init__(self, args=None):
    """Initializes a release.

    Args:
      args: dictionary with all the filter data (optional).
    """
    self._filter_options = {}
    if args:
      self.start_date = float(args['start_date'])
      self.end_date = float(args['end_date'])
      self.datetype = str(args['datetype'])
      self.state = int(args['state'])
      self.branch = str(args['branch'])
      self.release_type = str(args['release_type'])
      self.sort_method = int(args['sort_method'])
      self.reverse = int(args['descending'])

  def _validate_type(self, check, value, attribute):
    """Helper function to validate setter values and set attributes."""
    if isinstance(value, check):
      return True
    else:
      error = 'Invalid input for ' + attribute + ': not a ' + check.__name__
      error += ', instead got a ' + str(type(value))
      raise ValueError(error)

  @property
  def start_date(self):
    return self._filter_options['start_date']

  @start_date.setter
  def start_date(self, value):
    if self._validate_type(float, value, 'start_date'):
      self._filter_options['start_date'] = value

  @property
  def end_date(self):
    return self._filter_options['end_date']

  @end_date.setter
  def end_date(self, value):
    if self._validate_type(float, value, 'end_date'):
      self._filter_options['end_date'] = value

  @property
  def datetype(self):
    return self._filter_options['datetype']

  @datetype.setter
  def datetype(self, value):
    if self._validate_type(basestring, value, 'datetype'):
      self._filter_options['datetype'] = value

  @property
  def state(self):
    return self._filter_options['state']

  @state.setter
  def state(self, value):
    # allow a valid state value or the default 0 (no state selected)
    if State.is_valid(value) or value == 0:
      self._filter_options['state'] = value
    else:
      raise ValueError('Invalid input for status: ' + str(value))

  @property
  def branch(self):
    return self._filter_options['branch']

  @branch.setter
  def branch(self, value):
    if self._validate_type(basestring, value, 'branch'):
      self._filter_options['branch'] = value

  @property
  def release_type(self):
    return self._filter_options['release_type']

  @release_type.setter
  def release_type(self, value):
    if self._validate_type(basestring, value, 'release_type'):
      self._filter_options['release_type'] = value

  @property
  def sort_method(self):
    return self._filter_options['sort_method']

  @sort_method.setter
  def sort_method(self, value):
    if self._validate_type(int, value, 'sort_method'):
      self._filter_options['sort_method'] = value

  @property
  def reverse(self):
    return self._filter_options['reverse']

  @reverse.setter
  def reverse(self, value):
    if self._validate_type(int, value, 'reverse'):
      self._filter_options['reverse'] = value
