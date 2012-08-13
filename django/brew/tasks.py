from celery import task

@task()
def init_mashing():
    return 'finished'
