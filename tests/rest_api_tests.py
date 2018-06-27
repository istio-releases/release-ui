"""Unit Tests for Rest API."""

import unittest
import rest_api


class TestRestApi(unittest.TestCase):

  def test_in_cache(self):
    """test for in_cache helper function."""
    self.assertEqual(len(rest_api.release_requests), 0)


suite = unittest.TestLoader().loadTestsFromTestCase(TestRestApi)
unittest.TextTestRunner(verbosity=2).run(suite)
