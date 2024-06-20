kubectl create serviceaccount spark -n airflow 

kubectl create clusterrolebinding spark-role --clusterrole=edit --serviceaccount=airflow:spark --namespace=airflow
