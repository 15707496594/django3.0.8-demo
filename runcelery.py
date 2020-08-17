#!/usr/bin/env python
import os
from july.celery import QUEUES

if __name__ == '__main__':
    queues_str = ','.join([v for k, v in QUEUES.items()])
    os.system('celery -A july worker -Q %s -l info' % queues_str)
