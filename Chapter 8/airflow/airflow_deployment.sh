helm repo add apache-airflow https://airflow.apache.org

helm install airflow apache-airflow/airflow --namespace airflow --create-namespace -f custom_values.yaml