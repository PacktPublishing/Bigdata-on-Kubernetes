# Dploy elastic on kafka namespace
kubectl apply -f elastic_cluster.yaml -n kafka
kubectl apply -f kibana.yaml -n kafka

# Check elastic password
kubectl get secret elastic-es-elastic-user -n kafka -o go-template='{{.data.elastic | base64decode}}'

# Get certificates for elastic saved locally
kubectl get secret elastic-es-http-certs-public -n kafka --output=go-template='{{index .data "ca.crt" | base64decode}}' > ca.crt
kubectl get secret elastic-es-http-certs-public -n kafka --output=go-template='{{index .data "tls.crt" | base64decode}}' > tls.crt
kubectl get secret elastic-es-http-certs-internal -n kafka --output=go-template='{{index .data "tls.key" | base64decode}}' > tls.key

# locally create the keystore.jks file
openssl pkcs12 -export -in tls.crt -inkey tls.key -CAfile ca.crt -caname root -out keystore.p12 -password pass:BCoqZy82BhIhHv3C -name es-keystore
keytool -importkeystore -srckeystore keystore.p12 -srcstoretype PKCS12 -srcstorepass BCoqZy82BhIhHv3C -deststorepass OfwxynZ8KATfZSZe -destkeypass OfwxynZ8KATfZSZe -destkeystore keystore.jks -alias es-keystore

# Create a secret in kafka namespace with keystore.jks
kubectl create secret generic es-keystore --from-file=keystore.jks -n kafka

# Deploy Kafka Connect cluster
kubectl apply -f connect_cluster.yaml -n kafka

# Deploy Kafka JDBC Connector
kubectl  apply -f connectors/jdbc_source.yaml -n kafka

# Check messages in the topic
kubectl exec kafka-cluster-kafka-0 -n kafka -c kafka -it -- bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --from-beginning --topic src-customers

# Creating a service account for spark
kubectl create serviceaccount spark -n kafka
kubectl create clusterrolebinding spark-role-kafka --clusterrole=edit --serviceaccount=kafka:spark -n kafka

# Deploy spark streaming job
kubectl apply -f spark_streaming_job.yaml -n kafka
kubectl describe sparkapplication spark-streaming-job -n kafka
kubectl get pods -n kafka

# Check messages in the transformed topic
kubectl exec kafka-cluster-kafka-0 -n kafka -c kafka -it -- bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --from-beginning --topic customers-transformed

# Deploy elasticsearch sink connector
kubectl apply -f connectors/es_sink.yaml -n kafka

# Check the es sink connector
kubectl describe kafkaconnector es-sink -n kafka
