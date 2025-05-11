from airflow import DAG
from airflow.decorators import dag, task
from datetime import datetime
import pendulum
import sqlalchemy 
import requests
import logging
from sqlalchemy import (create_engine, MetaData, Table)
from sqlalchemy.dialects.postgresql import insert as pg_insert
from utils.clear_xcoms_operator import ClearXComsOperator
from airflow.utils.trigger_rule import TriggerRule
from utils.db import get_postgres_sqlalchemy_engine

@dag(
    dag_id= 'get_price_btc_price_by_day',
    schedule = '@daily',
    description= 'Получение цен на биткоин по api каждый день',
    start_date = pendulum.datetime(2025, 5, 9, tz='Europe/Moscow'),
    tags = ['BTC', 'day'],
    catchup=False
)

def btc_price_day_dag():
    @task
    def get_data(**kwargs):
        """
        Получает данные о цене BTC с API Bybit.
        """
        data_interval_start = kwargs['data_interval_start']
        data_interval_end = kwargs['data_interval_end']
        print(f'Данные за период с {data_interval_start} по {data_interval_end}')
        
        url = "https://api.bybit.com/v5/market/tickers?category=linear&symbol=BTCUSDT"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()['result']['list'][0]
        print(data)
        return {
            'data_interval_start': data_interval_start,
            'data_interval_end': data_interval_end,
            'last_price': float(data['lastPrice']),
            'volume_24h': float(data['volume24h']),
            'high_price_24h': float(data['highPrice24h']),
            'low_price_24h': float(data['lowPrice24h']),
            'bid_price': float(data['bid1Price']),
            'ask_price': float(data['ask1Price']),
            'open_interest': float(data['openInterest']),
        }

    @task
    def save_to_db(data):
        """
        Сохраняет данные в PostgreSQL.
        """
        # Подключение к БД
        target_engine = get_postgres_sqlalchemy_engine("etl_db")
        metadata = MetaData()
        get_price_btc_price_by_day = Table(
            'get_price_btc_price_by_day',
            metadata,
            schema='etl',
            autoload_with=target_engine
        )  
        with target_engine.connect() as connection:
            # Циклом вставлем данные и проверяем если есть service_id, то обновляем все данные on_conflict_do_update(index_elements=['service_id'], set_= {key: value for key, value in record.items() if key != 'service_id'})
                stmt=pg_insert(get_price_btc_price_by_day).values(data).on_conflict_do_nothing(index_elements=['data_interval_start'])
                connection.execute(stmt)
        logging.info("Данные записались успешно!")
        

    # Определяем последовательность задач
    raw_data = get_data()
    db_task = save_to_db(raw_data)
    clear = ClearXComsOperator(
        task_id='clear_xcoms',
        trigger_rule=TriggerRule.ALL_DONE
    )
    
    db_task >> clear

btc_price_dag_instance = btc_price_day_dag()

        