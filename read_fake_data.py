import json
from google.appengine.api import memcache

json_data = open("fake_data.json").read()
parsed_json = json.loads(json_data)
memcache.add(key="releases", value=parsed_json)
