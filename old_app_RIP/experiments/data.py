from google.appengine.ext import ndb

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
    release_key = ndb.KeyProperty()

class Release(ndb.Model):
    version = ndb.StringProperty()
    creation = ndb.DateTimeProperty(auto_now_add=True)
    last_change = ndb.DateTimeProperty(auto_now=True)
    changes = ndb.StringProperty(repeated=True)
    last_task = ndb.KeyProperty()
    status = ndb.BooleanProperty()
    tags = ndb.IntegerProperty(repeated=True)
    build_artifacts = ndb.StringProperty()
    branch = ndb.StringProperty()
    tasks = ndb.KeyProperty(repeated=True)

class Test_Post(ndb.Model):
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    site = ndb.StringProperty()
    comments = ndb.StringProperty()
