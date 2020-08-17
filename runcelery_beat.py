#!/usr/bin/env python
import os


if __name__ == '__main__':
    os.system('celery -A july beat -s /var/lib/celery/celerybeat-schedule')
