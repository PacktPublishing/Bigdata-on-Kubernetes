from airflow.decorators import task, dag
from airflow.operators.dummy import DummyOperator
from airflow.operators.bash import BashOperator
from datetime import datetime
import requests
import pandas as pd

default_args = {
    'owner': 'Ney',
    'start_date': datetime(2024, 2, 12)
}

@dag(
        default_args=default_args, 
        schedule_interval="@once", 
        description="Simple Pipeline with Titanic", 
        catchup=False, 
        tags=['Titanic']
)
def titanic_processing():

    # Task Definition
    start = DummyOperator(task_id='start')

    @task
    def first_task():
        print("And so, it begins!")

    @task
    def download_data():
        destination = "/tmp/titanic.csv"
        response = requests.get(
            "https://raw.githubusercontent.com/neylsoncrepalde/titanic_data_with_semicolon/main/titanic.csv", 
            stream=True
        )
        with open(destination, mode="wb") as file:
            file.write(response.content)
        return destination

    @task
    def analyze_survivors(source):
        df = pd.read_csv(source, sep=";")
        res = df.loc[df.Survived == 1, "Survived"].sum()
        print(res)

    @task
    def survivors_sex(source):
        df = pd.read_csv(source, sep=";")
        res = df.loc[df.Survived == 1, ["Survived", "Sex"]].groupby("Sex").count()
        print(res)

    last = BashOperator(
        task_id="last_task",
        bash_command='echo "This is the last task performed with Bash."',
    )

    end = DummyOperator(task_id='end')

    # Orchestration
    first = first_task()
    downloaded = download_data()
    start >> first >> downloaded
    surv_count = analyze_survivors(downloaded)
    surv_sex = survivors_sex(downloaded)

    [surv_count, surv_sex] >> last >> end

execution = titanic_processing()