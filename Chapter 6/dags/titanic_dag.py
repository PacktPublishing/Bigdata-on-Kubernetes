from airflow.decorators import task, dag
from airflow.operators.dummy import DummyOperator
from airflow.models import Variable
from datetime import datetime

default_args = {
    'owner': 'Ney',
    'start_date': datetime(2022, 4, 2)
}

@dag(
        default_args=default_args, 
        schedule_interval="@once", 
        description="Simple Pipeline with Titanic", 
        catchup=False, 
        tags=['Titanic']
)
def titanic_processing():

    start = DummyOperator(task_id='start')

    @task
    def first_task():
        print("And so, it begins!")

    ### Some more tasks here...

execution = titanic_processing()