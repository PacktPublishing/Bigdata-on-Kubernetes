helm repo add elastic https://helm.elastic.co

helm install elastic-operator elastic/eck-operator -n elastic --create-namespace --version 2.12.1
