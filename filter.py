"""Helper Functions to be used for sorting and filtering."""
import datetime


NAME_DECR = 1
NAME_INCR = 2
CREATION_DECR = 3
CREATION_INCR = 4
LAST_MOD_DECR = 5
LAST_MOD_INCR = 6
LAST_ACTIVE_DECR = 7
LAST_ACTIVE_INCR = 8


def filter_releases(releases, state, label, start_date, end_date, datetype):
  """Filters by all of the criteria.

  Args:
    releases: dictionary of release objects
    state: int representation of a state
    label: string label
    start_date: unix datetime of the beginning of a time period
    end_date: unix datetime of the end of a time period
    datetype: string determing which date (creation or last_modified) is
              filtered by the time period

  Returns:
    Array of releases that is filtered by the arguments.
  """

  # convert and validate inputs
  state = int(state)
  if state < 0 or state > 4:
    state = 0

  now = (datetime.datetime.now()-datetime.datetime(1970, 1, 1)).total_seconds()
  start_date = int(start_date)
  if start_date < 0 or start_date > now:
    start_date = 0

  end_date = int(end_date)
  if end_date <= 0:
    end_date = now

  label = str(label)
  if label == 'null':
    label = None

  filtered = []
  for release in releases.values():
    # If invalid datetype will default to started
    if datetype == 'last_modified':
      check_date = release.last_modified
    else:
      check_date = release.started

    if check_date >= start_date and check_date <= end_date:
      if release.state == state or state == 0:
        if label:
          if label in release.labels:
              filtered.append(release)
        else:
          filtered.append(release)

  return filtered


def sort(releases, sort_method):
  """Sorts 'releases' according to 'sort_method'.

  Args:
    releases: array of release objects
    sort_method: int representation of a sort sort_method

  Returns:
    Array 'releases' in a sorted order.
  """

  sort_method = int(sort_method)
  if sort_method == NAME_DECR:
    result = sorted(releases, key=lambda k: k.name, reverse=True)
  elif sort_method == NAME_INCR:
    result = sorted(releases, key=lambda k: k.name)
  elif sort_method == CREATION_DECR:
    result = sorted(releases, key=lambda k: k.started, reverse=True)
  elif sort_method == CREATION_INCR:
    result = sorted(releases, key=lambda k: k.started)
  elif sort_method == LAST_MOD_DECR:
    result = sorted(releases, key=lambda k: k.last_modified, reverse=True)
  elif sort_method == LAST_MOD_INCR:
    result = sorted(releases, key=lambda k: k.last_modified)
  elif sort_method == LAST_ACTIVE_DECR:
    result = sorted(releases, key=lambda k: k.last_active_task, reverse=True)
  elif sort_method == LAST_ACTIVE_INCR:
    result = sorted(releases, key=lambda k: k.last_active_task)
  return result
