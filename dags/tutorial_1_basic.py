from airflow.decorators import dag, task
import pendulum

@dag(
    dag_id="tutorial_1_basic",
    description="Простой учебный DAG: три задачи с зависимостями",
    schedule="@daily",
    start_date=pendulum.datetime(2026, 2, 20, tz="Europe/Moscow"),
    catchup=False,
    tags=["tutorial", "basic"],
)
def tutorial_1_basic_dag():
    @task
    def extract():
        print("EXTRACT: получаю сырые данные (пока просто список чисел)")
        data = [1, 2, 3, 4, 5]
        return data

    @task
    def transform(numbers: list[int]):
        print(f"TRANSFORM: входные данные = {numbers}")
        squared = [n ** 2 for n in numbers]
        print(f"TRANSFORM: возведение в квадрат = {squared}")
        return squared

    @task
    def load(transformed: list[int]):
        avg = sum(transformed) / len(transformed)
        print(f"LOAD: среднее значение = {avg}")
        return avg

    raw = extract()
    processed = transform(raw)
    load(processed)

tutorial_1_basic_dag()