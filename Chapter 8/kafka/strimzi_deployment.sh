helm repo add strimzi https://strimzi.io/charts/

helm install kafka strimzi/strimzi-kafka-operator --namespace kafka --create-namespace --version 0.40.0