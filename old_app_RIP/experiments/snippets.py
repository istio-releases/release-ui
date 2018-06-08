def index():
    """Opening page will be dashboard"""

    task = ReleaseTask(
        task_name='task123', start=datetime.now(), end = datetime.now(), status=False)
    task_key = task.put()

    release = Release(
        version='xxx-xxx-xxx', creation=datetime.now(), last_change=datetime.now(), status=True, tag=1, tasks=[task_key.id()], build_artifacts='https://github.com/cabreraem/mock_release_UI'
    )
    release_key = release.put()

    releases= Release.query().fetch(1)
    template_values = {
        'releases' : releases
    }

    return render_template('index.html', template_values=template_values)
