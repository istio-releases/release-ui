from flask import Flask, render_template, request


app = Flask(__name__)

@app.route('/', methods =["GET", "POST"])
def index():
    """Opening page will be dashboard"""

    fake ={"version" : "xxx-xxx-xxx", "status" : True, "creation" : "mm/dd/yy at hh:mm:ss", "last_mod" : "mm/dd/yy at hh:mm:ss", "last_active" : "task123", "tag" : 1}
    fakeData = [fake]

    task = {"status": False, "name": "test123", "start" : "mm/dd/yy at hh:mm:ss", "duration" : "xxx units", "log" : "https://github.com/cabreraem/mock_release_UI"}
    fakeTasks = [task]

    if request.method == "POST":
        return render_template('details.html', release=fake, tasks=fakeTasks)

    return render_template('index.html', releases=fakeData)


@app.route('/details')
def details():
    """Opens details of a single release """

    fake ={"version" : "xxx-xxx-xxx", "status" : True, "creation" : "mm/dd/yy at hh:mm:ss", "last_mod" : "mm/dd/yy at hh:mm:ss", "last_active" : "task123", "tag" : 1, "github" : "https://github.com/cabreraem/mock_release_UI"}
    task = {"status": False, "name": "test123", "start" : "mm/dd/yy at hh:mm:ss", "duration" : "xxx units", "log" : "https://github.com/cabreraem/mock_release_UI"}
    fakeTasks = [task]

    return render_template('details.html', release=fake, tasks=fakeTasks)


if __name__ == '__main__':
    app.run()
