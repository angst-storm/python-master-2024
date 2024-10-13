from apscheduler.jobstores.base import JobLookupError
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.interval import IntervalTrigger

from .models import Parser
from .tasks import send_run_actor


def schedule(scheduler: BackgroundScheduler, instance: Parser):
    job_id = instance.job_id

    try:
        scheduler.pause_job(job_id)
    except JobLookupError:
        pass

    if instance.scheduled is not None:
        try:
            scheduler.modify_job(
                job_id,
                func=send_run_actor,
                args=(instance.id, instance.name, instance.script.path),
            )
        except JobLookupError:
            scheduler.add_job(
                id=job_id,
                func=send_run_actor,
                args=(instance.id, instance.name, instance.script.path),
            )

        if instance.repeat_after is None:
            scheduler.reschedule_job(job_id, trigger=DateTrigger(instance.scheduled))
        else:
            scheduler.reschedule_job(
                job_id,
                trigger=IntervalTrigger(
                    seconds=instance.repeat_after.seconds, start_date=instance.scheduled
                ),
            )

        scheduler.resume_job(job_id)

    print(f"Parser {instance.id} {instance.name} scheduled")
