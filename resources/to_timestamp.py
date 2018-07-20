"""Converts datetime objects to unix time."""
# A module with a couple simple functions I got tired of writing/finding
import datetime
import logging


def to_timestamp(datetime_object):
  logging.debug('datetime: ' + str(datetime_object))
  if datetime_object:
    timestamp = datetime_object - datetime.datetime.fromtimestamp(0)
    logging.debug('Returns: ' + str(int(timestamp.total_seconds())))
    return int(timestamp.total_seconds())
  else:
    logging.debug('Returns: ' + str(int(current_timestamp())))
    return int(current_timestamp())


def current_timestamp():
  timestamp = datetime.datetime.now() - datetime.datetime.fromtimestamp(0)
  return int(timestamp.total_seconds())
