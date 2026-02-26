from airflow.decorators import dag, task
import pendulum
from datetime import timedelta
import random

@dag(
    dag_id='tutorial_5_my_turn',
    description='Если задача упала (сеть, API недоступен, таймаут), Airflow может автоматически перезапустить её несколько раз с паузой — без ручного Run',
    schedule=None,
    start_date=pendulum.datetime(2026, 2, 25, tz='Europe/Moscow'),
    catchup=False,
    tags=['tutorial', 'retries']
)

def tutorial_5_my_turn():

    @task(retries=3, retry_delay=timedelta(minutes=1))
    def unstable_task():
        if random.random() < 0.5: 
            raise Exception("Симуляция сбоя")
    
    unstable_task()
tutorial_5_my_turn()