from airflow.decorators import dag, task
import pendulum
import random

@dag(
    dag_id="tutorial_1_my_turn",
    description="Учебный DAG: 4 задачи с зависимостями",
    schedule="@daily",
    start_date=pendulum.datetime(2026, 2, 20, tz="Europe/Moscow"),
    catchup=False,
    tags=["tutorial", "my_turn"],
)
def tutorial_1_my_turn_dag():
    @task
    def generate_numbers():
        print("EXTRACT: получаю список из 10 случайных чисел от 1 до 100.")
        numbers = [random.randint(1, 100) for _ in range(10)]
        return numbers
    
    @task
    def find_max(numbers: list[int]):
        print(f"TRANSFORM: нахожу максимальное число в списке {numbers}")
        max_number = max(numbers)
        return max_number
    
    @task
    def find_min(numbers: list[int]):
        print(f"TRANSFORM: нахожу минимальное число в списке {numbers}")
        return min(numbers)
    
    @task
    def calculate_sum(numbers: list[int]):
        print(f"TRANSFORM: нахожу сумму чисел в списке {numbers}")
        return sum(numbers)

    raw = generate_numbers()
    find_max(raw)
    find_min(raw)
    calculate_sum(raw)

tutorial_1_my_turn_dag()
