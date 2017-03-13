# coding:utf-8
import celery
import json
from flask import Flask, Response

import celery_init, task_legal, task_legal_tr, task_bibliography, task_affiliation

DOMAINS = {
    "legal" : {
        "task": task_legal.legal_extract_references_task,
        "queue": celery_init.L_QUEUE
    },
    "legal-tr" : {
        "task": task_legal_tr.legal_tr_extract_references_task,
        "queue": celery_init.LTR_QUEUE
    },
    "bibliography" : {
        "task": task_bibliography.bibliography_extract_references_task,
        "queue": celery_init.B_QUEUE
    },
    "affiliation" : {
        "task": task_affiliation.affiliation_extract_references_task,
        "queue": celery_init.A_QUEUE
    }
}

# Web application main context
app = Flask(__name__)

@app.route('/')
def index():
    return "HELLO WORLD"

@app.route('/ping')
def ping():
    out = dict()
    out["ping"] = "pong"
    return json.dumps(out), 200

@app.route('/reference/<string:domain>/<string:filename>', methods=['GET'])
def domain_references(domain, filename):

    if domain not in DOMAINS:  
        return Response("Invalid domain: " + domain, status=400)

    task = DOMAINS[domain]["task"].apply_async(queue=DOMAINS[domain]["queue"])

    return Response('Celery task ID: ' + task.id, status=202)

@app.route('/reference/status/<string:task_id>', methods=['GET'])
def get_status(task_id):
    task = celery.result.AsyncResult(task_id)

    #Most likely states = PENDING, SUCCESS and FAILURE - for all states, refer to http://docs.celeryproject.org/en/latest/reference/celery.states.html
    #Does not account for the state while it is being processing, additional code would be required
    if task.state == 'SUCCESS':
        return json.dumps({'progress': -1, 'completed': True,'steps': 0}), 200
    elif task.state == 'FAILURE':
        return json.dumps({'progress': -1, 'completed': False, 'steps': 0, 'exception': 'Task failure'}), 200
    elif task.state == 'PENDING':
        return json.dumps({'progress': -1, 'completed': False, 'steps': 0}), 200

    return "Invalid task ID: {}".format(task_id), 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
    