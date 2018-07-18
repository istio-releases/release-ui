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
    self.assertEqual(length, 5)

  def test_tasks(self):
    tasks = self.adapter.get_tasks()
    length = 0
    for key, value in tasks.iteritems():
      self.assertEqual(value, self.adapter.get_task(key))
      length += 1
    self.assertEqual(length, 3)

  def test_get_labels(self):
    labels = self.adapter.get_labels()
    check_labels = ['label0', 'label1', 'label2', 'label3']
    self.assertEqual(labels, check_labels)

suite = unittest.TestLoader().loadTestsFromTestCase(TestFileAdapter)
unittest.TextTestRunner(verbosity=2).run(suite)
