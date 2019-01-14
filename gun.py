import os
import gevent.monkey
gevent.monkey.patch_all()

debug = False
loglevel = 'debug'
bind = '0.0.0.0:20002'
pidfile = 'gunicorn_log/gunicorn.pid'
logfile = 'gunicorn_log/debug.log'

threads = 2
workers = 3
worker_class = 'gunicorn.workers.ggevent.GeventWorker'

x_forwarded_for_header = 'X-FORWARDED-FOR'