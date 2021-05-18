import logging
from time import sleep

from celery import Celery

from models.single_time_report import run_single_time_report
dev_broker = 'redis://redis:6379/0'
prod_broker = 'redis://nydc1-data2u-redis-dev-default.data2u-redis.service.nydc1.consul:6379/0'
celery = Celery('tasks', broker=prod_broker, backend=prod_broker)
# celery = Celery('tasks', broker='redis://redis:6379/0', backend='redis://redis:6379/0')
# nydc1-data2u-redis-dev-default.data2u-redis.service.nydc1.consul
# celery = Celery('tasks', broker='redis://localhost/0')


# setting logging variable -----------------------------------------------
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


# tasks for the queue -----------------------------------------------
@celery.task
def test(x, y):
    sleep(5)
    return x + y


@celery.task
def single_time_report_task(report_id, timestamp):
    log.info(f'run single time report: {report_id} time_stamp: {timestamp}')
    run_single_time_report(report_id, timestamp)
# tasks for the queue -----------------------------------------------
