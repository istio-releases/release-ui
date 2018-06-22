"""Astract Base Class for Release Data."""

import abc


class ReleaseData(object):
  """ABC to retrieve data from File Adapter and Airflow Adapter."""

  __metaclass__ = abc.ABCMeta

  @abc.abstractmethod
  def get_releases(self):
    """Retrieve all release information."""
    pass

  @abc.abstractmethod
  def get_tasks(self):
    """Retrieve all task information."""
    pass

  @abc.abstractmethod
  def get_labels(self):
    """Retrieve all possible labels for UI."""
    pass
