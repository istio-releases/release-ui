"""State Values."""


class State(object):
  """Static State Class."""

  UNUSED_STATUS = 1
  ABANDONED = 2
  FINISHED = 3
  PENDING = 4
  RUNNING = 5
  FAILED = 6

  @classmethod
  def is_valid(cls, value):
    return 1 <= value <= 6


STATE_FROM_STRING = {'none': State.UNUSED_STATUS,
                     'not_started': State.PENDING,
                     'running': State.RUNNING,
                     'success': State.FINISHED,
                     'failed': State.FAILED,
                     'shutdown': State.ABANDONED,
                     'upstream_failed': State.PENDING,
                     'None': State.UNUSED_STATUS,
                     'removed': State.ABANDONED,
                     'queued': State.PENDING,
                     'skipped': State.ABANDONED}

STRING_FROM_STATE = {v: k for k, v in STATE_FROM_STRING.iteritems()}
