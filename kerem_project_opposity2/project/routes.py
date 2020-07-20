from flask import render_template, request
from project import app, redis_queue

from project.redis_task_controller import run_algorithm


@app.route("/", methods=['GET', 'POST'])
def index():
    context = {}
    if request.method == 'POST':
        search_term = request.form.get('search')
        number = int(request.form.get('number'))
        pick_type = request.form.get('pick_type')
        pick_algorithm = request.form.get('pick_algorithm')
        job_id = request.form.get('job_id')
        job = redis_queue.enqueue_call(
            func=run_algorithm, args=(search_term, number, pick_type, pick_algorithm, job_id), result_ttl=60,
            timeout=7000
        )
        print("job id", job.get_id())
        context['search_posted'] = "yes"
    return render_template('index.html', **context)
