from airflow.decorators import task, dag
from airflow.models import Variable
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime
import requests
import pandas as pd
from sqlalchemy import create_engine
import boto3

engine = create_engine('postgresql://postgres:postgres@postgres:5432/postgres')

aws_access_key_id = Variable.get('aws_access_key_id')
aws_secret_access_key = Variable.get('aws_secret_access_key')

s3_client = boto3.client(
    's3',
    aws_access_key_id=aws_access_key_id, 
    aws_secret_access_key=aws_secret_access_key
)

default_args = {
    'owner': 'Ney',
    'start_date': datetime(2024, 2, 12)
}

@dag(
        default_args=default_args, 
        schedule_interval="@once", 
        description="Insert Data into PostgreSQL and AWS", 
        catchup=False, 
        tags=['postgres', 'aws']
)
def postgres_aws_dag():
    
    # Tasks definition
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
    def write_to_postgres(source):
        df = pd.read_csv(source, sep=";")
        df.to_sql('titanic', engine, if_exists="replace", chunksize=1000, method='multi')

    create_view = PostgresOperator(
        task_id="create_view",
        postgres_conn_id="postgres",
        sql="""
            CREATE OR REPLACE VIEW titanic_count_survivors AS
            SELECT 
                "Sex",
                SUM("Survived") as survivors_count
            FROM titanic
            GROUP BY "Sex"
          """,
    )

    @task
    def upload_to_s3(source):
        s3_client.upload_file(source, 'bdok-539445819060', 'titanic.csv')

    # Orchestration
    download = download_data()
    write = write_to_postgres(download)
    write >> create_view
    upload = upload_to_s3(download)

execution = postgres_aws_dag()