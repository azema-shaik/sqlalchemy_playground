import subprocess
from celery import Celery,chain 
from config import config




app = Celery(
    broker = config.celery_broker, backend = config.celery_backend
)

tasks_id = {}

@app.task 
def generate_logs():
    subprocess.run(f'py log_genrator/log_genrator.py -t 1000 -p 100 -c'.split())

@app.task
def write_logs_to_db(status):
    print(f'Logs generated sucessfully. Sql Generation. Start:STATUS = {status = }')
    subprocess.run(r'py creating_tables.py'.split())


chain(
    generate_logs.s()|write_logs_to_db.s()
).delay()
