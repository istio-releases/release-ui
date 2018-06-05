from flask import Flask, render_template, request
import datetime


app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def index():
    """Main index is the dashboard with a table of recent releases"""

    fake1 = {"version":"xxx-xxx-123","status":True,"creation":"mm/dd/yy at hh:mm:ss","last_mod":"mm/dd/yy at hh:mm:ss","last_active":"task123","tags":[1,3]}
    fake2 = {"version":"xxx-xxx-456","status":False,"creation":"mm/dd/yy at hh:mm:ss","last_mod":"mm/dd/yy at hh:mm:ss","last_active":"task456","tags":[2]}
    fakeData = [fake1, fake2]

    return render_template('index.html', releases= fakeData)


@app.route('/details')
def details():
    """Opens details of a single release """

    fake ={"version" : "xxx-xxx-xxx", "status" : True, "creation" : "mm/dd/yy at hh:mm:ss", "last_mod" : "mm/dd/yy at hh:mm:ss", "last_active" : "task123", "tag" : 1, "github" : "https://github.com/cabreraem/mock_release_UI"}
    task = {"status": False, "name": "test123", "start" : "mm/dd/yy at hh:mm:ss", "duration" : "xxx units", "log" : "https://github.com/cabreraem/mock_release_UI"}
    fakeTasks = [task]

    return render_template('details.html', release=fake, tasks=fakeTasks)

# @app.route('/form')
# def form():
#     return render_template('test_form.html')
#
# @app.route('/submitted', methods=['POST'])
# def submitted_form():
#     # gets the neccessary info from the form
#     name = request.form['name']
#     email = request.form['email']
#     site = request.form['site_url']
#     comments = request.form['comments']
#
#     #puts the form info into a variable called "post", which uses the Test_Post ndb model(aka "a kind") defined above
#     post = Test_Post(
#         name=name,
#         email=email,
#         site=site,
#         comments=comments
#     )
#     # put this entry into the datastore
#     post.put()
#
#     return render_template(
#     'test_form_submitted.html',
#     name=name,
#     email=email,
#     site=site,
#     comments=comments,
#     )
