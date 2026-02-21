from airflow.decorators import dag, task
import pendulum
import random
import logging

@dag(
    dag_id="tutorial_2_my_turn",
    description="Одна задача может зависеть от нескольких других и получать несколько результатов через XCom",
    schedule="@daily",
    start_date=pendulum.datetime(2026, 2, 20, tz="Europe/Moscow"),
    catchup=False,
    tags=["tutorial", "my_turn"],
)
def tutorial_2_my_turn_dag():
    @task
    def generate_data():
        logging.info("EXTRACT: получаю список из 7 случайных чисел от 10 до 50.")
        numbers = [random.randint(10, 50) for _ in range(7)]
        return numbers
    
    @task
    def find_max(numbers: list[int]):
        logging.info(f"TRANSFORM: нахожу максимальное число в списке {numbers}")
        return max(numbers)
    
    @task
    def find_min(numbers: list[int]):
        logging.info(f"TRANSFORM: нахожу минимальное число в списке {numbers}")
        return min(numbers)
    
    @task
    def report(max_val, min_val):
        result = f"Max: {max_val}, Min: {min_val}"
        logging.info(result)
        return result
    
    raw = generate_data()
    max_val = find_max(raw)
    min_val = find_min(raw)
    report(max_val, min_val)

tutorial_2_my_turn_dag()
