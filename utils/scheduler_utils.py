import pytz
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.jobstores.memory import MemoryJobStore



def configure_scheduler(scheduler, config):
    jobstores = {
        'default': MemoryJobStore()
    }
    executors = {
        'default': ThreadPoolExecutor(50),  # max threads: 1
    }
    job_defaults = {
        'coalesce': True,
        'max_instances': 1
    }

    scheduler.configure(
        jobstores=jobstores,
        executors=executors,
        job_defaults=job_defaults,
        timezone=pytz.timezone(config.get('local_timezone'))
    )
