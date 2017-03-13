# coding:utf-8
import time
from celery import Task

from celery_init import app
import celery_init

@app.task(name='bibliography_extract_references_task', queue=celery_init.B_QUEUE, bind=True, ignore_result=False)
def bibliography_extract_references_task(self):
	time.sleep(20)

   