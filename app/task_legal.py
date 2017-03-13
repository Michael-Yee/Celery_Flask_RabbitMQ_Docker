# coding:utf-8
import time
from celery import Task

from celery_init import app
import celery_init

@app.task(name='legal_extract_references_task', queue=celery_init.L_QUEUE, bind=True, ignore_result=False)
def legal_extract_references_task(self):  
    time.sleep(10)
    