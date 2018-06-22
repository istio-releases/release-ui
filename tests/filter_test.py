import datetime
import json
import random
import sys
import unittest
sys.path.append('../')  # pylint: disable=g-import-not-at-top
from filter import filter_releases  # pylint: disable=g-import-not-at-top


class TestSort(unittest.TestCase):

  def setUp(self):
    self.unsorted = json.loads(open('../fake_release_data.json').read())
    current_time = (datetime.datetime.now()-datetime.datetime(1970, 1, 1))
    self.current_time = int(current_time.total_seconds())

  def test_filter_dates_creation(self):
    current_time = self.current_time
    start_date = random.randint(0, current_time)
    end_date = random.randint(0, current_time)
    # while end_date < start_date or end_date != 0:
    #   end_date = random.randint(0, current_time)
    filtered = filter_releases(self.unsorted, 0, 'null', start_date, end_date, 'started')  # pylint: disable=line-too-long
    if end_date == 0:
      end_date = current_time
    for item in filtered:
      self.assertGreaterEqual(item['started'], start_date)
      self.assertLessEqual(item['started'], end_date)

  def test_filter_dates_last_modified(self):
    current_time = self.current_time
    start_date = random.randint(0, current_time)
    end_date = random.randint(0, current_time)
    # while end_date < start_date or end_date != 0:
    #   end_date = random.randint(0, current_time)
    filtered = filter_releases(self.unsorted, 0, 'null', start_date, end_date, 'last_modified')  # pylint: disable=line-too-long
    if end_date == 0:
      end_date = current_time
    for item in filtered:
      self.assertGreaterEqual(item['last_modified'], start_date)
      self.assertLessEqual(item['last_modified'], end_date)

  def test_filter_state(self):
    for state in xrange(0, 5):
      filtered = filter_releases(self.unsorted, state, 'null', 0, self.current_time, 'started')  # pylint: disable=line-too-long
      for item in filtered:
        if state != 0:
          self.assertEqual(item['state'], state)
          
if __name__ == '__main__':
  unittest.main()
