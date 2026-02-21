from airflow.decorators import dag, task
from datetime import datetime
import pendulum
import logging
import requests

@dag(
    dag_id='tutorial_3_my_turn',
    description='Одна задача делает HTTP-запрос к публичному API, вторая обрабатывает ответ и логирует результат.',
    schedule=None,
    start_date=pendulum.datetime(2026, 2, 21, tz='Europe/Moscow'),
    catchup=False,
    tags=['tutorial', 'api']
)
def tutorial_3_my_turn():
    @task
    def fetch_data():
        url = 'https://jsonplaceholder.typicode.com/posts/1'
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            logging.info('Запрос успешен')
            return response.json()
        except requests.RequestException as e:
            logging.error(f'Ошибка при запросе к API: {e}')
            raise
    

    @task
    def process_data(data):
        logging.info(f'Processing data: {data}')
        id = data['id']
        title = data['title']
        result = f'Post ID: {id}, Title: {title}'
        logging.info(f'Result: {result}')
        return result
    
    fetch_data_task = fetch_data()
    process_data(fetch_data_task)

tutorial_3_my_turn()
    