"""State Values."""


class State(object):
  UNUSED_STATUS = 0
  PENDING = 1
  FINISHED = 2
  FAILED = 3
  ABANDONED = 4
  RUNNING = 5


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

STRING_FROM_STATE =  {v: k for k, v in STATE_FROM_STRING.iteritems()}
