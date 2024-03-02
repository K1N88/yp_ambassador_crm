from celery import shared_task
from dbbackup import utils
import subprocess
from datetime import datetime


@shared_task
def backup_database():
    utils.run_command('dbbackup --clean')


@shared_task
def backup_db():
    today = datetime.now().strftime('%Y-%m-%d')
    backup_filename = f'backup_{today}.tar'
    command = f'docker run --rm --volumes-from infra_backend_1 -v $(pwd):/backup ubuntu tar cvf /backup/{backup_filename} /db_data'  # nowa
    subprocess.run(command, shell=True)
