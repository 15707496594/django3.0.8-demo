from july.celery import app
import time

@app.task
def hello_world():
    time.sleep(2)
    return 'Hello World!'