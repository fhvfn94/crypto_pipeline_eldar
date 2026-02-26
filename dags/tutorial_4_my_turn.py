from airflow.decorators import dag, task
import pendulum
import logging
from utils.db import get_postgres_sqlalchemy_engine
from sqlalchemy import text

@dag(
    dag_id='tutorial_4_my_turn',
    description='одна задача готовит данные, вторая пишет их в таблицу в PostgreSQL (как в твоём основном DAG с BTC).',
    schedule=None,
    start_date=pendulum.datetime(2026, 2, 21, tz='Europe/Moscow'),
    catchup=False,
    tags=['tutsorial', 'db']
)
def tutorial_4_my_turn():
  
    @task
    def prepare_data():
        result = [
            {"name": "Alice", "score": 85}, 
            {"name": "Bob", "score": 92}, 
            {"name": "Charlie", "score": 78}
        ]
        logging.info(f'Result: {result}')
        return result
    
    @task
    def save_to_db(data):
        target_engine = get_postgres_sqlalchemy_engine("etl_db")
        with target_engine.begin() as conn:
            for row in data:
                conn.execute(
                    text(
                        "INSERT INTO etl.tutorial_4_scores (name, score) "
                        "VALUES (:name, :score)"
                    ),
                    row,
                )
    
    prepare_data_task = prepare_data()
    save_to_db(prepare_data_task)

tutorial_4_my_turn()