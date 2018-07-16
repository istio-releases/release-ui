"""Unit Tests for Rest API."""

import sys
import unittest
sys.path.append('../')   # allows for importing of files not in the same directory | pylint: disable=line-too-long
import rest_api   # pylint: disable=g-import-not-at-top


class TestRestApi(unittest.TestCase):

  def test_in_cache(self):
    """test for in_cache helper function."""
    self.assertEqual(len(rest_api.release_requests), 0)


suite = unittest.TestLoader().loadTestsFromTestCase(TestRestApi)
unittest.TextTestRunner(verbosity=2).run(suite)
