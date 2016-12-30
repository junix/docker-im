FROM java:openjdk-8-jre
RUN set -ex \
    && wget http://mirrors.hust.edu.cn/apache/kafka/0.8.2.1/kafka_2.9.1-0.8.2.1.tgz \
    && tar xzvf kafka_2.9.1-0.8.2.1.tgz \
    && mv kafka_2.9.1-0.8.2.1 /app \
    && rm kafka_2.9.1-0.8.2.1.tgz \
    && mkdir /app/data \
    && mkdir /app/logs
