FROM java:openjdk-8-jre
RUN set -ex \
    && wget http://mirrors.hust.edu.cn/apache/kafka/0.8.2.1/kafka_2.9.1-0.8.2.1.tgz \
    && tar xzvf kafka_2.9.1-0.8.2.1.tgz \
    && mv kafka_2.9.1-0.8.2.1 /app \
    && rm kafka_2.9.1-0.8.2.1.tgz \
    && mkdir /app/data \
    && mkdir /app/logs
 ADD config/consumer.properties /app/config/consumer.properties
 ADD config/log4j.properties /app/config/log4j.properties
 ADD config/producer.properties /app/config/producer.properties
 ADD config/server.properties /app/config/server.properties
 ADD entry.sh /entry.sh

 CMD ["/entry.sh"]
