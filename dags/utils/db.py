from airflow.hooks.base import BaseHook
from sqlalchemy import create_engine

def get_postgres_sqlalchemy_engine(conn_id: str, schema: str = None):
    """
    Возвращает SQLAlchemy engine на основе подключения из Airflow.
    
    :param conn_id: ID подключения в Airflow (например, 'postgres_default')
    :param schema: (опционально) имя схемы БД
    :return: SQLAlchemy engine
    """
    connection = BaseHook.get_connection(conn_id)
    user = connection.login
    password = connection.password
    host = connection.host
    port = connection.port or 5432
    db_schema = schema or connection.schema

    conn_str = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_schema}"
    return create_engine(conn_str)