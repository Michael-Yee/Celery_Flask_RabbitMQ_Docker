# coding:utf-8
import time
from celery import Task

from celery_init import app
import celery_init

@app.task(name='affiliation_extract_references_task', queue=celery_init.A_QUEUE, bind=True, ignore_result=False)
def affiliation_extract_references_task(self):
	time.sleep(15)
