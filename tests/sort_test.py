import datetime
import json
import sys
import unittest
sys.path.append('../')  # pylint diable=g-import-not-at-top
from filter import sort  # pylint diable=g-import-not-at-top


class TestSort(unittest.TestCase):
  """Tests the sorting function from filter.py"""

  def setUp(self):
    self.unsorted = json.loads(open('../fake_release_data.json').read())

  def test_sort_method_1(self):
    self.unsorted = self.unsorted.values()
    sorted_releases = sort(self.unsorted, 1)
    previous_name = None
    for item in sorted_releases:
      if previous_name is None:
        previous_name = item['name']
      for i, char in enumerate(item['name']):
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
      previous_name = item['name']

  def test_sort_method_2(self):
    self.unsorted = self.unsorted.values()
    sorted_releases = sort(self.unsorted, 2)
    previous_name = None
    for item in sorted_releases:
      if previous_name is None:
        previous_name = item['name']
      for i, char in enumerate(item['name']):
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
      previous_name = item['name']

  def test_sort_method_3(self):
    self.unsorted = self.unsorted.values()
    sorted_releases = sort(self.unsorted, 3)
    previous = datetime.datetime.now()-datetime.datetime(1970, 1, 1)
    previous = previous.total_seconds()
    for item in sorted_releases:
      self.assertLessEqual(item['started'], previous)

  def test_sort_method_4(self):
    self.unsorted = self.unsorted.values()
    sorted_releases = sort(self.unsorted, 4)
    previous = 0
    for item in sorted_releases:
      self.assertGreaterEqual(item['started'], previous)

  def test_sort_method_5(self):
    self.unsorted = self.unsorted.values()
    sorted_releases = sort(self.unsorted, 5)
    previous = datetime.datetime.now()-datetime.datetime(1970, 1, 1)
    previous = previous.total_seconds()
    for item in sorted_releases:
      self.assertLessEqual(item['last_modified'], previous)

  def test_sort_method_6(self):
    self.unsorted = self.unsorted.values()
    sorted_releases = sort(self.unsorted, 6)
    previous = 0
    for item in sorted_releases:
      self.assertGreaterEqual(item['last_modified'], previous)

  def test_sort_method_7(self):
    self.unsorted = self.unsorted.values()
    sorted_releases = sort(self.unsorted, 7)
    previous_name = None
    for item in sorted_releases:
      if previous_name is None:
        previous_name = item['last_active_task']
      for i, char in enumerate(item['last_active_task']):
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
      previous_name = item['last_active_task']

  def test_sort_method_8(self):
    self.unsorted = self.unsorted.values()
    sorted_releases = sort(self.unsorted, 8)
    previous_name = None
    for item in sorted_releases:
      if previous_name is None:
        previous_name = item['last_active_task']
      for i, char in enumerate(item['last_active_task']):
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
      previous_name = item['last_active_task']


if __name__ == '__main__':
  unittest.main()
