import json
import random
import time

blank_release = json.loads(open("fake_data_template.json").read())
blank_template = blank_release['release2_id']
new_data = {}

#---Set the number of releases you want in the JSON file here---#
number_of_releases = 25

#-----Creates the data to put into the JSON-----#
for i in range(number_of_releases):
    random.seed()
    release_id = "release-" + str(random.randint(0,1023))
    while release_id in new_data:
        release_id = "release-" + str(random.randint(0,1023))
    number_of_labels = random.randint(1,5)
    number_of_tasks = random.randint(1,5)
    new_data[release_id] = {}
    new_data[release_id]['name'] = release_id
    new_data[release_id]['repo_url'] = 'https://youtu.be/dQw4w9WgXcQ'
    new_data[release_id]['labels'] = []
    for label_num in range(number_of_labels):
        new_data[release_id]['labels'].append('label' + str(label_num))
    new_data[release_id]['ref'] = 'reference number ' + str(random.randint(0,1023))
    new_data[release_id]['state'] = random.randint(1,4)
    new_data[release_id]['stage'] = random.randint(1,7)
    new_data[release_id]['started'] = random.randint(0, 2147483647)
    new_data[release_id]['last_modified'] = random.randint(0, 2147483647)
    new_data[release_id]['artifacts_link'] = 'https://youtu.be/dQw4w9WgXcQ'
    new_data[release_id]['release_url'] = 'https://youtu.be/dQw4w9WgXcQ'
    new_data[release_id]['tasks'] = {}
    for task_num in range(number_of_tasks):
        new_data[release_id]['tasks']['task'+str(task_num)+'_ID'] = {}
        new_data[release_id]['tasks']['task'+str(task_num)+'_ID']['task_name'] = 'task-' + str(task_num)
        new_data[release_id]['tasks']['task'+str(task_num)+'_ID']['started'] = random.randint(0, 2147483647)
        new_data[release_id]['tasks']['task'+str(task_num)+'_ID']['last_modified'] = random.randint(0, 2147483647)
        new_data[release_id]['tasks']['task'+str(task_num)+'_ID']['status'] = random.randint(1,4)
        new_data[release_id]['tasks']['task'+str(task_num)+'_ID']['error'] = 'error number ' + str(random.randint(0,1023))
        new_data[release_id]['tasks']['task'+str(task_num)+'_ID']['log_url'] = 'https://youtu.be/dQw4w9WgXcQ'
        new_data[release_id]['tasks']['task'+str(task_num)+'_ID']['dependent_on'] = []
        for prev_task in range(0,task_num):
            new_data[release_id]['tasks']['task'+str(task_num)+'_ID']['dependent_on'].append('task' + str(prev_task) + '_ID')
    new_data[release_id]['last_active_task'] = 'task' + str(random.randint(1,5)) + '_ID'
    print  release_id + ' created'

#---Puts the JSON into a file called fake_data.json---#
fake_data = open("fake_data.json", "w+")
json.dump(new_data, fake_data, indent=2 )

print 'Created a file called fake_data.json'
