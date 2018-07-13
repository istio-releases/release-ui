"""Creates the fake data to be used by the fake backend."""
import json
import random

blank_release = json.loads(open('fake_data_template.json').read())
blank_template = blank_release['release2_id']
new_data = {}

# ---Set the number of releases you want in the JSON file here--- #
number_of_releases = 500

"""Creates the data to put into the JSON."""
# pylint: disable=line-too-long
for i in range(number_of_releases):
  random.seed()
  release_id = 'release-' + str(random.randint(0, 1023))
  while release_id in new_data:
    release_id = 'release-' + str(random.randint(0, 1023))
  number_of_tasks = random.randint(2, 5)
  number_of_repos = random.randint(1, 3)
  new_data[release_id] = {}
  new_data[release_id]['name'] = release_id
  new_data[release_id]['ref'] = 'reference number ' + str(random.randint(0, 1023))
  new_data[release_id]['state'] = random.randint(1, 4)
  new_data[release_id]['stage'] = random.randint(1, 7)
  new_data[release_id]['started'] = random.randint(0, 1531437000)
  new_data[release_id]['last_modified'] = random.randint(0, 1531437000)
  new_data[release_id]['tasks'] = []
  for task_num in range(number_of_tasks):
    new_data[release_id]['tasks'].append(random.randint(0, 9))
  new_data[release_id]['links'] = []
  new_data[release_id]['links'].append('https://youtu.be/dQw4w9WgXcQ')
  new_data[release_id]['links'].append('https://youtu.be/dQw4w9WgXcQ')
  if number_of_repos >= 1:
    new_data[release_id]['links'].append('https://youtu.be/dQw4w9WgXcQ')
  if number_of_repos >= 2:
    new_data[release_id]['links'].append('https://youtu.be/dQw4w9WgXcQ')
  if number_of_repos >= 3:
    new_data[release_id]['links'].append('https://youtu.be/dQw4w9WgXcQ')
  new_data[release_id]['last_active_task'] = 'task' + str(random.randint(1, 5)) + '_ID'
  branch = random.randint(0,2)
  if branch == 0:
    new_data[release_id]['branch'] = 'master'
  if branch == 1:
    new_data[release_id]['branch'] = '0.8'
  if branch == 2:
    new_data[release_id]['branch'] = '1.0'
  type = random.randint(0,2)
  if type == 0:
    new_data[release_id]['type'] = 'daily'
  if type == 1:
    new_data[release_id]['type'] = 'weekly'
  if type == 2:
    new_data[release_id]['type'] = 'monthly'
  print  release_id + ' created'

# ---Puts the JSON into a file called fake_data.json--- #
fake_data = open('fake_release_data.json', 'w+')
json.dump(new_data, fake_data, indent=2)

print 'Created a file called fake_release_data.json'

new_data = {}
for i in range(10):
  task_id = 'task-' + str(i)
  new_data[task_id] = {}
  new_data[task_id]['task_name'] = task_id
  new_data[task_id]['started'] = random.randint(0, 1531437000)
  new_data[task_id]['last_modified'] = random.randint(0, 1531437000)
  new_data[task_id]['status'] = random.randint(1, 4)
  new_data[task_id]['error'] = 'error number ' + str(random.randint(0, 1023))
  new_data[task_id]['log_url'] = 'https://youtu.be/dQw4w9WgXcQ'
  new_data[task_id]['dependent_on'] = []
  print  task_id + ' created'

# ---Puts the JSON into a file called fake_data.json--- #
fake_data = open('fake_task_data.json', 'w+')
json.dump(new_data, fake_data, indent=2)
