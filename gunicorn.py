from multiprocessing import cpu_count
import os

def max_proccess():
    return cpu_count()

bind='0.0.0.0:' + os.getenv('PORT', '8000')
max_requests=1000
worker_class='gevent'
workers=max_proccess()

env={
    'DJANGO_SETTINGS_MODULE':'bookcamp.settings'
}

reload=True
name='bookcamp'