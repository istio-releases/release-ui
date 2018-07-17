import datetime
import sys
import unittest
from adapters.file_adapter import FileAdapter
from resources.filter_releases import sort  # pylint: disable=g-import-not-at-top


class TestSort(unittest.TestCase):
  """Tests the sorting function from filter.py"""

  def setUp(self):
    self.unsorted = FileAdapter('fake_data/fake_release_data.json', 'fake_data/fake_task_data.json')
    self.unsorted = self.unsorted.get_releases().values()

  def test_sort_method_created_descending(self):
    sorted_releases = sort(self.unsorted, 2, 1)
    previous = datetime.datetime.now()-datetime.datetime(1970, 1, 1)
    previous = previous.total_seconds()
    for item in sorted_releases:
      time = item.started-datetime.datetime(1970, 1, 1)
      time = time.total_seconds()
      self.assertLessEqual(time, previous)
      previous = time

  def test_sort_method_created_ascending(self):
    sorted_releases = sort(self.unsorted, 2, 0)
    previous = datetime.datetime.fromtimestamp(0)
    for item in sorted_releases:
      time = item.started
      self.assertGreaterEqual(time, previous)
      previous = time

  def test_sort_method_modified_descending(self):
    sorted_releases = sort(self.unsorted, 3, 1)
    previous = datetime.datetime.now()-datetime.datetime(1970, 1, 1)
    previous = previous.total_seconds()
    for item in sorted_releases:
      time = item.last_modified-datetime.datetime(1970, 1, 1)
      time = time.total_seconds()
      self.assertLessEqual(time, previous)
      previous = time

  def test_sort_method_modified_ascending(self):
    sorted_releases = sort(self.unsorted, 3, 0)
    previous = datetime.datetime.fromtimestamp(0)
    for item in sorted_releases:
      time = item.last_modified
      self.assertGreaterEqual(time, previous)
      previous = time

  def test_sort_method_active_descending(self):
    sorted_releases = sort(self.unsorted, 4, 1)
    previous_name = None
    for item in sorted_releases:
      if previous_name is None:
        previous_name = item.last_active_task
      for i, char in enumerate(item.last_active_task):
        if char.isalpha():
          if previous_name:
            if len(previous_name) > i:
              self.assertGreaterEqual(char, previous_name[i])
            else:
              break
            if char > previous_name[i]:
              break
        if char.isdigit():
          if len(previous_name) > i:
            self.assertLessEqual(char, previous_name[i])
          else:
            break
          if char < previous_name[i]:
            break
      previous_name = item.last_active_task

  def test_sort_method_active_ascending(self):
    sorted_releases = sort(self.unsorted, 4, 0)
    previous_name = None
    for item in sorted_releases:
      if previous_name is None:
        previous_name = item.last_active_task
      for i, char in enumerate(item.last_active_task):
        if char.isalpha():
          if previous_name:
            if len(previous_name) > i:
              self.assertLessEqual(char, previous_name[i])
            else:
              break
            if char < previous_name[i]:
              break
        if char.isdigit():
          if len(previous_name) > i:
            self.assertGreaterEqual(char, previous_name[i])
          else:
            break
          if char > previous_name[i]:
            break
      previous_name = item.last_active_task


if __name__ == '__main__':
  unittest.main()
