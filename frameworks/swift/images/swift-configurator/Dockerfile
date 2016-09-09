FROM ubuntu:14.04
MAINTAINER Daniele Venzano <venza@brownhat.org>

RUN apt-get update && apt-get install -y supervisor software-properties-common python-requests && apt-get clean
RUN apt-add-repository cloud-archive:mitaka
RUN apt-get update && apt-get install -y swift swift-proxy python-swiftclient

VOLUME /etc/swift

ADD files/list_storage_nodes.py /usr/local/bin/list_storage_nodes.py
ADD files/configure.sh /usr/local/bin/configure.sh
RUN chmod 755 /usr/local/bin/*.sh /usr/local/bin/*.py

CMD /usr/local/bin/configure.sh

