from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor

jobstores = {
    'default': DjangoJobStore()
}

executors = {
    'default': ThreadPoolExecutor(),  
}

scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors)