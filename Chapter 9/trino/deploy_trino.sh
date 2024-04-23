helm repo add trino https://trinodb.github.io/charts

helm install trino trino/trino -f custom_values.yaml -n trino --create-namespace --version 0.19.0