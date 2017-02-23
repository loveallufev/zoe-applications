FROM ubuntu:14.04

MAINTAINER Daniele Venzano <venza@brownhat.org>

RUN apt-get update && apt-get install -y --force-yes software-properties-common python-software-properties
RUN apt-add-repository -y ppa:webupd8team/java
RUN /bin/echo debconf shared/accepted-oracle-license-v1-1 select true | /usr/bin/debconf-set-selections
RUN apt-get update && apt-get -y install oracle-java7-installer oracle-java7-set-default curl

WORKDIR /opt

ENV HADOOP_VERSION 2.6.5
RUN curl -s http://apache.mirrors.ovh.net/ftp.apache.org/dist/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz | tar -xz -C /opt/

RUN ln -s hadoop-${HADOOP_VERSION} hadoop

ENV JAVA_HOME /usr/lib/jvm/java-7-oracle/
ENV HADOOP_HOME /opt/hadoop

#RUN hadoop/bin/hdfs namenode -format hdfscluster
#ENV SPARK_HOME /opt/spark
#ENV PATH /opt/spark/bin:/opt/spark/sbin:${PATH}

COPY files/* /opt/
RUN chmod +x /opt/*.sh
RUN mkdir /mnt/datanode
EXPOSE 50010 50075 50020

CMD /opt/start-datanode.sh

#ENV SPARK_MASTER_PORT 7077
#ENV SPARK_MASTER_WEBUI_PORT 8080
