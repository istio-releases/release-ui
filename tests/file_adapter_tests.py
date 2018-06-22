#--------Unit Tests for File Adapter-------#

import unittest
from file_adapter import FileAdapter

class TestFileAdapter(unittest.TestCase):

    def __init__(self):
        self.adapter = FileAdapter('fake_release_data.json', 'fake_task_data.json')


    def test_get_releases(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_get_tasks(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_get_labels(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()
