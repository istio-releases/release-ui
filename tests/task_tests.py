"""Unit Tests for Task."""

import unittest
from task import Task


class TestTask(unittest.TestCase):

  def test_getters(self):
    task = Task({
        'status': 3,
        'log_url': 'https://youtu.be/dQw4w9WgXcQ',
        'started': 47752289,
        'dependent_on': [],
        'last_modified': 637147117,
        'task_name': 'task-2',
        'error': 'error number 990'
    })

    self.assertEqual(task.task_name, 'task-2')
    self.assertEqual(task.status, 3)
    self.assertEqual(task.log_url, 'https://youtu.be/dQw4w9WgXcQ')
    self.assertEqual(task.started, 47752289)
    self.assertEqual(task.dependent_on, [])
    self.assertEqual(task.last_modified, 637147117)
    self.assertEqual(task.error, 'error number 990')

  def test_setters(self):
    task = Task()

    task.task_name = 'new task'
    self.assertEqual(task.task_name, 'new task')
    with self.assertRaises(ValueError):
      task.task_name = 0

    task.status = 0
    self.assertEqual(task.status, 0)
    with self.assertRaises(ValueError):
      task.status = ['task1', 'task2']

    task.log_url = 'url'
    self.assertEqual(task.log_url, 'url')
    with self.assertRaises(ValueError):
      task.log_url = 0

    task.started = 0
    self.assertEqual(task.started, 0)
    with self.assertRaises(ValueError):
      task.started = 'started'

    task.add_dependency('task1')
    self.assertEqual(task.dependent_on, ['task1'])
    with self.assertRaises(ValueError):
      task.add_dependency(0)

    task.last_modified = 0
    self.assertEqual(task.last_modified, 0)
    with self.assertRaises(ValueError):
      task.last_modified = 'last_modified'

    task.error = 'error'
    self.assertEqual(task.error, 'error')
    with self.assertRaises(ValueError):
      task.error = 0

suite = unittest.TestLoader().loadTestsFromTestCase(TestTask)
unittest.TextTestRunner(verbosity=2).run(suite)
