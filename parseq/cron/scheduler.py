from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler(
    {
        "apscheduler.jobstores.default": {
            "class": "django_apscheduler.jobstores:DjangoJobStore"
        },
        'apscheduler.executors.processpool': {
            "type": "threadpool"
        },
    }
)