FROM quay.io/strimzi/kafka:0.40.0-kafka-3.7.0

# using root user
USER root:root

# create default directory jdbc plugins
RUN mkdir -p /opt/kafka/plugins/kafka-connect-jdbc
RUN mkdir -p /opt/kafka/plugins/kafka-connect-s3
RUN mkdir -p /opt/kafka/plugins/kafka-connect-es

# copy local jars files to image
COPY kafka-connect-jdbc/ /opt/kafka/plugins/kafka-connect-jdbc/
COPY kafka-connect-s3/ /opt/kafka/plugins/kafka-connect-s3/
COPY kafka-connect-es/ /opt/kafka/plugins/kafka-connect-es/
