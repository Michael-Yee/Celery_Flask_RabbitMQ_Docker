# coding:utf-8
import os
from celery import Celery
from kombu import Queue, Exchange

#Celery queues names
A_QUEUE   = 'affiliation'
B_QUEUE   = 'bibliography'
L_QUEUE   = 'legal'
LTR_QUEUE = 'legal-tr'


#Broker settings
try:
    BROKER_URL = u'amqp://guest:guest@{addr}:{port}//'.format(
        addr=os.environ['RABBITMQ_PORT_5672_TCP_ADDR'],
        port=os.environ['RABBITMQ_PORT_5672_TCP_PORT'],
    )
except:
    #Ensure that the 'guest' account has the correct permissions -> sudo rabbitmqctl set_permissions -p / guest ".*" ".*" ".*"
    BROKER_URL = u'amqp://guest:guest@localhost:5672//'

#Instantiate Celery object 
app = Celery(
    'app', 
    broker=BROKER_URL, 
    backend='amqp', 
    include=['task_legal', 'task_legal_tr', 'task_bibliography', 'task_affiliation']
    )

#Additional configuration, see the application user guide for full details
app.conf.update(
    #Send task-related events so that tasks can be monitored using tools like flower
    #CELERY_SEND_EVENTS = True, 

    #task will NOT report its status as ‘started’ when the task is executed by a worker
    #CELERY_TRACK_STARTED = False, 

    #If the error: expires for queue does not match, try sudo rabbitmqctl reset
    CELERY_TASK_RESULT_EXPIRES = 3600, #60 minutes, time in seconds
    CELERY_IGNORE_RESULT = False, #stores the task return values 
    CELERY_CREATE_MISSING_QUEUES = True, #Catach-all fir any queues specified that are not defined in task_queues will be automatically created
    CELERY_QUEUES = (
        Queue(B_QUEUE,    Exchange(B_QUEUE),  routing_key=B_QUEUE),
        Queue(L_QUEUE,    Exchange(L_QUEUE),  routing_key=L_QUEUE),
        Queue(LTR_QUEUE,  Exchange(LTR_QUEUE),routing_key=LTR_QUEUE),
        Queue(A_QUEUE,    Exchange(A_QUEUE),  routing_key=A_QUEUE)
    ),
    CELERY_ROUTES = {
        'bibliography_extract_references_task': {'queue': B_QUEUE,  'routing_key': B_QUEUE},
        'legal_extract_references_task':        {'queue': L_QUEUE,  'routing_key': L_QUEUE},   
        'legal_tr_extract_references_task':     {'queue': LTR_QUEUE,'routing_key': LTR_QUEUE},   
        'affiliation_extract_references_task':  {'queue': A_QUEUE,  'routing_key': A_QUEUE}
        }
    )