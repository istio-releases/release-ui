"""Unit Tests for Release."""

from datetime import datetime
import unittest
from data.release import Release


class TestRelease(unittest.TestCase):

  def test_getters(self):
    release1 = Release({
        'tasks': [0, 2, 1, 2, 1],
        'name': 'release-260',
        'links': ['https://youtu.be/dQw4w9WgXcQ'],
        'started': 1158781609,
        'branch': 'master',
        'release_type' : 'daily',
        'state': 4,
        'last_modified': 341231047,
        'last_active_task': 'task4_ID'})

    self.assertEqual(release1.name, 'release-260')
    self.assertEqual(release1.tasks, [0, 2, 1, 2, 1])
    self.assertEqual(release1.links, ['https://youtu.be/dQw4w9WgXcQ'])
    self.assertEqual(release1.started, datetime.fromtimestamp(1158781609))
    self.assertEqual(release1.branch, 'master')
    self.assertEqual(release1.release_type, 'daily')
    self.assertEqual(release1.state, 4)
    self.assertEqual(release1.last_modified, datetime.fromtimestamp(341231047))
    self.assertEqual(release1.last_active_task, 'task4_ID')

  def test_setters(self):
    release2 = Release()

    release2.name = 'new release'
    self.assertEqual(release2.name, 'new release')
    with self.assertRaises(ValueError):
      release2.name = 0

    release2.tasks = []
    self.assertEqual(release2.tasks, [])
    with self.assertRaises(ValueError):
      release2.tasks = 0
    with self.assertRaises(ValueError):
      release2.tasks = ['task1', 'task2']

    release2.links = []
    self.assertEqual(release2.links, [])
    with self.assertRaises(ValueError):
      release2.links = 0
    with self.assertRaises(ValueError):
      release2.links = [0, 1]

    release2.started = 0
    self.assertEqual(release2.started, datetime.fromtimestamp(0))
    with self.assertRaises(ValueError):
      release2.started = 'started'

    release2.branch = '0.8'
    self.assertEqual(release2.branch, '0.8')
    with self.assertRaises(ValueError):
      release2.branch = 0

    release2.release_type = 'monthly'
    self.assertEqual(release2.release_type, 'monthly')
    with self.assertRaises(ValueError):
      release2.release_type = []

    release2.state = 0
    self.assertEqual(release2.state, 0)
    with self.assertRaises(ValueError):
      release2.state = 'state'

    release2.last_modified = 0
    self.assertEqual(release2.last_modified, datetime.fromtimestamp(0))
    with self.assertRaises(ValueError):
      release2.last_modified = 'last_modified'

    release2.last_active_task = 'last_active_task'
    self.assertEqual(release2.last_active_task, 'last_active_task')
    with self.assertRaises(ValueError):
      release2.last_active_task = 0

suite = unittest.TestLoader().loadTestsFromTestCase(TestRelease)
unittest.TextTestRunner(verbosity=2).run(suite)
