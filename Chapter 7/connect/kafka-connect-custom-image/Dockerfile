FROM confluentinc/cp-kafka-connect-base:7.6.0

RUN confluent-hub install --no-prompt confluentinc/kafka-connect-jdbc:10.7.5 \
    && confluent-hub install --no-prompt confluentinc/kafka-connect-s3:10.5.8