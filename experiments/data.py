from google.appengine.ext import ndb

class Release(ndb.Model):
    version = ndb.StringProperty()
    creation = ndb.DateTimeProperty()
    last_change = ndb.DateTimeProperty()
    changes = ndb.StringProperty(repeated=True)
    last_task = ndb.StringProperty()
    status = ndb.BooleanProperty()
    tag = ndb.IntegerProperty()
    build_artifacts = ndb.StringProperty()
    branch = ndb.StringProperty()
    tasks = ndb.IntegerProperty(repeated=True)


class Modification(ndb.Model):
    change_url = ndb.StringProperty()
    timestamp = ndb.DateTimeProperty()


class ReleaseTask(ndb.Model):
    task_name = ndb.StringProperty()
    start = ndb.DateTimeProperty()
    end = ndb.DateTimeProperty()
    status = ndb.BooleanProperty()
    error_message = ndb.StringProperty()
    log_link = ndb.StringProperty()
