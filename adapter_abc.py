"""Astract Base Class for Release Data."""

import abc


class Adapter(object):
  """ABC to retrieve data from File Adapter and Airflow Adapter."""

  __metaclass__ = abc.ABCMeta

  @abc.abstractmethod
  def get_releases(self, start_date, end_date, datetype, state,
                   label, sort_method, descending):
    """Retrieves filtered release information.

    Args:
      start_date: unix timestamp format
      end_date: unix timestamp format
      datetype: what to filter by - created or last last_modified
      state: state enumeration
      label: filtering labels
      sort_method: sort method enumeration
      descending: boolean

    Returns:
      Dictionary of Release objects.
    """
    pass

  @abc.abstractmethod
  def get_release(self, release_name):
    """Retrieve individual release information.

    Returns:
      Single Release object.
    """
    pass

  @abc.abstractmethod
  def get_tasks(self):
    """Retrieve all task information.

    Returns:
      Dictionary of Task objects.
    """
    pass

  @abc.abstractmethod
  def get_task(self, task_name):
    """Retrieve individual task information.

    Returns:
      Single Task object.
    """
    pass

  @abc.abstractmethod
  def get_labels(self):
    """Retrieve all possible labels for UI.

    Returns:
      Array of labels as strings.
    """
    pass
