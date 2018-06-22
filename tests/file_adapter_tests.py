"""Unit Tests for File Adapter."""

import unittest
from file_adapter import FileAdapter


class TestFileAdapter(unittest.TestCase):

  def test_get_releases(self):
    self.adapter = FileAdapter('mini_release_data.json', 'mini_task_data.json')
    releases = self.adapter.get_releases()
    length = 0
    for _, value in releases.iteritems():
      self.assertEqual(len(value), 10)
      length += 1
    self.assertEqual(length, 5)

  def test_get_tasks(self):
    self.adapter = FileAdapter('mini_release_data.json', 'mini_task_data.json')
    tasks = self.adapter.get_tasks()
    length = 0
    for _, value in tasks.iteritems():
      self.assertEqual(len(value), 7)
      length += 1
    self.assertEqual(length, 3)

  def test_get_labels(self):
    self.adapter = FileAdapter('mini_release_data.json', 'mini_task_data.json')
    labels = self.adapter.get_labels()
    check_labels = ['label0', 'label1', 'label2', 'label3']
    self.assertEqual(labels, check_labels)

suite = unittest.TestLoader().loadTestsFromTestCase(TestFileAdapter)
unittest.TextTestRunner(verbosity=2).run(suite)
