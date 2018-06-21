import json
import random
import time

blank_release = json.loads(open("fake_data_template.json").read())
blank_template = blank_release['release2_id']
new_data = {}

#---Set the number of releases you want in the JSON file here---#
number_of_releases = 5

#-----Creates the data to put into the JSON-----#
for i in range(number_of_releases):
    random.seed()
    release_id = "release-" + str(random.randint(0,1023))
    while release_id in new_data:
        release_id = "release-" + str(random.randint(0,1023))
    number_of_labels = random.randint(1,5)
    number_of_tasks = random.randint(1,5)
    number_of_repos = random.randint(1,3)
    new_data[release_id] = {}
    new_data[release_id]['name'] = release_id
    new_data[release_id]['labels'] = []
    for label_num in range(number_of_labels):
        new_data[release_id]['labels'].append('label' + str(label_num))
    new_data[release_id]['ref'] = 'reference number ' + str(random.randint(0,1023))
    new_data[release_id]['state'] = random.randint(1,4)
    new_data[release_id]['stage'] = random.randint(1,7)
    new_data[release_id]['started'] = random.randint(0, 1528996059)
    new_data[release_id]['last_modified'] = random.randint(0, 1528996059)
    new_data[release_id]['tasks'] = []
    for task_num in range(number_of_tasks):
        new_data[release_id]['tasks'].append(random.randint(0,2))
    new_data[release_id]['links'] = []
    new_data[release_id]['links'].append({'name': 'Release', 'url': 'https://youtu.be/dQw4w9WgXcQ'})
    new_data[release_id]['links'].append({'name': 'Artifacts', 'url': 'https://youtu.be/dQw4w9WgXcQ'})
    if number_of_repos >= 1:
        new_data[release_id]['links'].append({'name': 'Istio Repo', 'url': 'https://youtu.be/dQw4w9WgXcQ'})
    if number_of_repos >= 2:
        new_data[release_id]['links'].append({'name': 'API Repo', 'url': 'https://youtu.be/dQw4w9WgXcQ'})
    if number_of_repos >= 3:
        new_data[release_id]['links'].append({'name': 'Proxy Repo', 'url': 'https://youtu.be/dQw4w9WgXcQ'})
    new_data[release_id]['last_active_task'] = 'task' + str(random.randint(1,5)) + '_ID'
    print  release_id + ' created'

#---Puts the JSON into a file called fake_data.json---#
fake_data = open("mini_fake_release_data.json", "w+")
json.dump(new_data, fake_data, indent=2 )

print 'Created a file called fake_release_data.json'

new_data = {}
for i in range(3):
    task_id = "task-" + str(i)
    new_data[task_id] = {}
    new_data[task_id]['task_name'] = task_id
    new_data[task_id]['started'] = random.randint(0, 2147483647)
    new_data[task_id]['last_modified'] = random.randint(0, 2147483647)
    new_data[task_id]['status'] = random.randint(1,4)
    new_data[task_id]['error'] = 'error number ' + str(random.randint(0,1023))
    new_data[task_id]['log_url'] = 'https://youtu.be/dQw4w9WgXcQ'
    new_data[task_id]['dependent_on'] = []
    print  task_id + ' created'

#---Puts the JSON into a file called fake_data.json---#
fake_data = open("mini_fake_task_data.json", "w+")
json.dump(new_data, fake_data, indent=2 )
