"""Converts datetime objects to unix time."""
# A module with a couple simple functions I got tired of writing/finding
from datetime import datetime


def to_timestamp(datetime_object):
  timestamp = datetime_object - datetime.fromtimestamp(0)
  timestamp = timestamp.total_seconds()
  return int(timestamp)

def current_timestamp():
  timestamp = datetime.now() - datetime.fromtimestamp(0)
  timestamp.total_seconds()
  return int(timestamp)
