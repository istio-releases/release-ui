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
def getData(start_date, end_date, datetype): # used to find all releases in the given date range
    start_date = int(start_date)
    end_date = int(end_date)
    datetype = int(datetype) # designates whether to sort by creation date(0) or date modified(1)
    result = memcache.get('releases')
    filtered = {}
    for item in result.items():
        if datetype == 0:
            if item[1]['started'] >= start_date and item[1]['started'] <= end_date:
                item[1]['started']
                filtered[item[1]['name']] = item[1]
        elif datetype == 1:
            if item[1]['last_modified'] >= start_date and item[1]['last_modified'] <= end_date:
                filtered[item[1]['name']] = item[1]
    return filtered

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
        parser.add_argument('filter_by')
        args = parser.parse_args()
        print args['start_date']
        response = getData(args['start_date'], args['end_date'], args['datetype'])
        return json.dumps(response)




api.add_resource(Releases, '/releases')
api.add_resource(Sort, '/sort')

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

# @app.route('/list)
# def list():
#     # Get list of releases from memcache or adapter interface
#     result = memcache.get('releases')
#     request.data = result
#     request.data = json.dumps(request.data)
#     return request.data, 200
