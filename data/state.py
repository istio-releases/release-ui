"""State Values."""


class State(object):
  UNUSED_STATUS = 0
  PENDING = 1
  FINISHED = 2
  FAILED = 3
  ABANDONED = 4

# TODO(emiliacabrera): add 'skipped': State.ABANDONED to STATE_FROM_STRING
# TODO(emiliacabrera): add 'up_for_retry': State.PENDING} to STATE_FROM_STRING
