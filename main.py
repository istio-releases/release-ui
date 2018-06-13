from flask import Flask, jsonify, request, json, render_template, send_file, make_response, abort
from flask_restful import Api, Resource, reqparse
import json
from google.appengine.api import memcache


# creating the Flask application
app = Flask(__name__)
api = Api(app)

#--------"File Adapter"(temporary)-------#
json_data = open("fake_data.json").read()
parsed_json = json.loads(json_data)
memcache.add(key="releases", value=parsed_json)


#--------Functions to be used for sorting/filtering-------#
# Filters by all of the criteria shown below, returns an array of filtered releases
def filter(state, label, start_date, end_date, datetype):
    # convert variables from unix type to something usableself
    state = int(state)
    start_date = int(start_date)
    end_date = int(end_date)
    datetype = int(datetype) # designates whether to sort by creation date(0) or date modified(1)
    data = memcache.get('releases')
    filtered = []
    for item in data.items():
        if end_date > 0: # see if there is a valid end date - if not, don't consider it
            if datetype == 1: # filter by date modified
                if item[1]['last_modified'] >= start_date and item[1]['last_modified'] <= end_date:
                    if item[1]['state'] == state:
                        if label != 'None':
                            for l in item[1]['labels']:
                                if l == label:
                                    filtered.append(item[1])
                        else:
                            filtered.append(item[1])
            else: #filter by date created
                if item[1]['started'] >= start_date and item[1]['started'] <= end_date:
                    if item[1]['state'] == state:
                        if label != 'None':
                            for l in item[1]['labels']:
                                if l == label:
                                    filtered.append(item[1])
                        else:
                            filtered.append(item[1])
        else:
            if datetype == 1: # filter by date modified
                if item[1]['last_modified'] >= start_date:
                    if item[1]['state'] == state:
                        if label != 'None':
                            for l in item[1]['labels']:
                                if l == label:
                                    filtered.append(item[1])
                        else:
                            filtered.append(item[1])
            else: #filter by date created
                if item[1]['started'] >= start_date:
                    if item[1]['state'] == state:
                        if label != 'None':
                            for l in item[1]['labels']:
                                if l == label:
                                    filtered.append(item[1])
                        else:
                            filtered.append(item[1])
    return filtered

# sorts unsorted according to sort_method. See https://docs.google.com/document/d/1JDD_NX2XVL7yqYcfFOqkef1FKv98nrlRFJ0OpSZprMU/ for enumerations
def sort(unsorted, sort_method):
    sort_method = int(sort_method)
    if sort_method == 1:
        result = sorted(unsorted, key=lambda k: k['name'], reverse=True)
    elif sort_method == 2:
        result = sorted(unsorted, key=lambda k: k['name'])
    elif sort_method == 3:
        result = sorted(unsorted, key=lambda k: k['started'], reverse=True)
    elif sort_method == 4:
        result = sorted(unsorted, key=lambda k: k['started'])
    elif sort_method == 5:
        result = sorted(unsorted, key=lambda k: k['last_modified'], reverse=True)
    elif sort_method == 6:
        result = sorted(unsorted, key=lambda k: k['last_modified'])
    elif sort_method == 7:
        result = sorted(unsorted, key=lambda k: k['last_active_task'], reverse=True)
    elif sort_method == 8:
        result = sorted(unsorted, key=lambda k: k['last_active_task'])
    return result

def in_memcache(args):
    start_date = hex(int(args['start_date']))
    end_date = hex(int(args['end_date']))
    datetype = str(int(args['datetype']))
    state = str(int(args['state']))
    label = str(args['label'])
    sort_method = str(int(args['sort_method']))
    key = start_date + end_date + datetype + state + label + sort_method

    if memcache.get(key):
        return key, memcache.get(key)
    else:
        return False, key

#--------REST API--------#
class Releases(Resource):
    def get(self):
        result = memcache.get('releases')
        result = json.dumps(result)
        return result, 200


class Sort(Resource):
    def get(self):
        releases = getData()
        return releases
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('start_date')
        parser.add_argument('end_date')
        parser.add_argument('datetype')
        parser.add_argument('state')
        parser.add_argument('label')
        parser.add_argument('sort_method')
        parser.add_argument('limit')
        parser.add_argument('offset')
        args = parser.parse_args()

        response = filter(args['state'], args['label'], args['start_date'], args['end_date'], args['datetype'])
        response = sort(response, args['sort_method'])
        return json.dumps(response), 200


class Pagination(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('start_date')
        parser.add_argument('end_date')
        parser.add_argument('datetype')
        parser.add_argument('state')
        parser.add_argument('label')
        parser.add_argument('sort_method')
        parser.add_argument('limit')
        parser.add_argument('offset')
        args = parser.parse_args()

        memcache_exists, memcache_results = in_memcache(args)
        if memcache_exists:
            return memcache_results[args['offset']:args['limit']]
        else:
            response = filter(args['state'], args['label'], args['start_date'], args['end_date'], args['datetype'])
            response = sort(response, args['sort_method'])
            memcache.add(key=memcache_results, value=response)
            return response[args['offset']:args['limit']]



api.add_resource(Releases, '/releases')
api.add_resource(Sort, '/sort')
api.add_resource(Pagination, '/page')

if __name__ == '__main__':
     app.run(port='8080', debug=True)



#-----------Handlers------------#
@app.route('/')
@app.route('/details')
def basic_pages():
    return make_response(open('templates/index.html').read())


@app.route('/getReleases')
def getReleases():
    # return render_template('details.html')
    result = memcache.get('releases')
    result = json.dumps(result)
    return result, 200

# TODO(dommarques):
#     - implement server-side pagination
#     - implement caching of sorted, filtered releases
