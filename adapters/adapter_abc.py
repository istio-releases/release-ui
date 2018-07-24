"""Astract Base Class for Release Data."""

import abc


class Adapter(object):
  """ABC to retrieve data from File Adapter and Airflow Adapter."""

  __metaclass__ = abc.ABCMeta

  @abc.abstractmethod
  def get_releases(self, filter_options):
    """Retrieves filtered release information.

    Args:
      filter_options: An object containing filter/sort parameters

    Returns:
      Dictionary of Release objects.
    """
    pass

  @abc.abstractmethod
  def get_release(self, release_id):
    """Retrieve individual release information.

    Args:
      release_id: unique release identifier (str)

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
  def get_task(self, task_name, execution_date):
    """Retrieve individual task information.

    Args:
      task_name: str name of the task
      execution_date: int

    Returns:
      Single Task object.
    """
    pass

  @abc.abstractmethod
  def get_branches(self):
    """Retrieve all possible branches for UI.

    Returns:
      Array of branches as strings.
    """
    pass

  @abc.abstractmethod
  def get_release_types(self):
    """Retrieve all possible release_types for UI.

    Returns:
      Array of release_types as strings.
    """
    pass
