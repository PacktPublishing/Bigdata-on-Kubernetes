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
    def read_data():
        df = pd.read_csv("https://raw.githubusercontent.com/neylsoncrepalde/titanic_data_with_semicolon/main/titanic.csv", sep=";")
        survivors = df.loc[df.Survived == 1, "Survived"].sum()
        survivors_sex = df.loc[df.Survived == 1, ["Survived", "Sex"]].groupby("Sex").count()
        return {
            'survivors_count': survivors,
            'survivors_sex': survivors_sex
        }

    @task
    def print_survivors(source):
        print(source['survivors_count'])

    @task
    def survivors_sex(source):
        print(source['survivors_sex'])

    last = BashOperator(
        task_id="last_task",
        bash_command='echo "This is the last task performed with Bash."',
    )

    end = DummyOperator(task_id='end')

    # Orchestration
    first = first_task()
    downloaded = read_data()
    start >> first >> downloaded
    surv_count = print_survivors(downloaded)
    surv_sex = survivors_sex(downloaded)

    [surv_count, surv_sex] >> last >> end

execution = titanic_processing()