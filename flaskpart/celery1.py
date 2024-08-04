from celery import Celery

celery = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/1')

def make_celery(app):
    celery.conf.update(app.config)
    return celery