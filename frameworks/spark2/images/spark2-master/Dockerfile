FROM java:8

MAINTAINER Daniele Venzano <venza@brownhat.org>

# Install maven
RUN apt-get update && apt-get install -y maven git

ENV PATH /usr/lib/jvm/java-8-openjdk-amd64/bin:$PATH

ARG SPARK_VERSION
ENV SPARK_VERSION ${SPARK_VERSION:-branch-2.0}

ARG HADOOP_VERSION
ENV HADOOP_VERSION ${HADOOP_VERSION:-hadoop2.6}

ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64

WORKDIR /code

RUN git clone https://github.com/apache/spark.git
WORKDIR /code/spark
RUN git checkout $SPARK_VERSION

RUN build/mvn -Phadoop-2.6 -Dhadoop.version=2.6.1 -DskipTests clean package

ENV SPARK_HOME /code/spark
ENV PATH /code/spark/bin:/code/spark/sbin:${PATH}

COPY files/* /opt/
RUN chmod +x /opt/*.sh
EXPOSE 8080 7077

ENV SPARK_MASTER_PORT 7077
ENV SPARK_MASTER_WEBUI_PORT 8080

CMD /opt/start-master.sh

