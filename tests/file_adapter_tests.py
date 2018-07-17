"""Unit Tests for File Adapter."""

import unittest
from adapters.file_adapter import FileAdapter


class TestFileAdapter(unittest.TestCase):

  def setUp(self):
    self.adapter = FileAdapter('tests/mini_release_data.json', 'tests/mini_task_data.json')

  def test_releases(self):
    releases = self.adapter.get_releases()
    length = 0
    for key, value in releases.iteritems():
      self.assertEqual(value, self.adapter.get_release(key))
      length += 1
    self.assertEqual(length, 10)

  def test_tasks(self):
    tasks = self.adapter.get_tasks()
    length = 0
    for key, value in tasks.iteritems():
      self.assertEqual(value, self.adapter.get_task(key))
      length += 1
    self.assertEqual(length, 4)

  def test_get_branches(self):
    branches = self.adapter.get_branches()
    check_branches = ['0.8', '1.0', 'master']
    self.assertEqual(branches, check_branches)

  def test_get_types(self):
    release_types = self.adapter.get_types()
    check_types = ['monthly', 'daily', 'weekly']
    self.assertEqual(release_types, check_types)

suite = unittest.TestLoader().loadTestsFromTestCase(TestFileAdapter)
unittest.TextTestRunner(verbosity=2).run(suite)
