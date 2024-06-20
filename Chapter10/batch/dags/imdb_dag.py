from airflow.decorators import task, dag
from airflow.utils.task_group import TaskGroup
from airflow.providers.cncf.kubernetes.operators.spark_kubernetes import SparkKubernetesOperator
from airflow.providers.cncf.kubernetes.sensors.spark_kubernetes import SparkKubernetesSensor
from airflow.providers.amazon.aws.operators.glue_crawler import GlueCrawlerOperator
from airflow.models import Variable
from datetime import datetime
import requests
import boto3

aws_access_key_id = Variable.get("aws_access_key_id")
aws_secret_access_key = Variable.get("aws_secret_access_key")

s3 = boto3.client('s3', 
    aws_access_key_id=aws_access_key_id, 
    aws_secret_access_key=aws_secret_access_key
)

default_args = {
    'owner': 'Ney',
    'start_date': datetime(2024, 5, 10)
}

@dag(
        default_args=default_args, 
        schedule_interval="@once", 
        description="IMDB Dag", 
        catchup=False, 
        tags=['IMDB']
)
def IMDB_batch():

    @task
    def data_acquisition():
        urls_dict = {
            "names.tsv.gz": "https://datasets.imdbws.com/name.basics.tsv.gz",
            "basics.tsv.gz": "https://datasets.imdbws.com/title.basics.tsv.gz",
            "crew.tsv.gz": "https://datasets.imdbws.com/title.crew.tsv.gz",
            "principals.tsv.gz": "https://datasets.imdbws.com/title.principals.tsv.gz",
            "ratings.tsv.gz": "https://datasets.imdbws.com/title.ratings.tsv.gz"
        }

        for title, url in urls_dict.items():
            response = requests.get(url, stream=True)
            with open(f"/tmp/{title}", mode="wb") as file:
                file.write(response.content)
            s3.upload_file(f"/tmp/{title}", "bdok-539445819060", f"landing/imdb/{title}")
        
        return True
    

    with TaskGroup("tsvs_to_parquet") as tsv_parquet:
        tsvs_to_parquet = SparkKubernetesOperator(
            task_id="tsvs_to_parquet",
            namespace="airflow",
            #application_file=open(f"{APP_FILES_PATH}/spark_imdb_tsv_parquet.yaml").read(),
            application_file="spark_imdb_tsv_parquet.yaml",
            kubernetes_conn_id="kubernetes_default",
            do_xcom_push=True
        )
        tsvs_to_parquet_sensor = SparkKubernetesSensor(
            task_id="tsvs_to_parquet_sensor",
            namespace="airflow",
            application_name="{{ task_instance.xcom_pull(task_ids='tsvs_to_parquet.tsvs_to_parquet')['metadata']['name'] }}",
            kubernetes_conn_id="kubernetes_default"
        )
        tsvs_to_parquet >> tsvs_to_parquet_sensor
    

    with TaskGroup('Transformations') as transformations:
        consolidated_table = SparkKubernetesOperator(
            task_id='consolidated_table',
            namespace="airflow",
            application_file="spark_imdb_consolidated_table.yaml",
            kubernetes_conn_id="kubernetes_default",
            do_xcom_push=True
        )
        consolidated_table_sensor = SparkKubernetesSensor(
            task_id='consolidated_table_sensor',
            namespace="airflow",
            application_name="{{ task_instance.xcom_pull(task_ids='Transformations.consolidated_table')['metadata']['name'] }}",
            kubernetes_conn_id="kubernetes_default"
        )
        consolidated_table >> consolidated_table_sensor


    glue_crawler_consolidated = GlueCrawlerOperator(
        task_id='glue_crawler_consolidated',
        region_name='us-east-1',
        aws_conn_id='aws_conn',
        wait_for_completion=True,
        config = {'Name': 'imdb_consolidated_crawler'}
    )

    
    # Orchestration
    da = data_acquisition() 
    da >> tsv_parquet >> transformations >> glue_crawler_consolidated

execution = IMDB_batch()
