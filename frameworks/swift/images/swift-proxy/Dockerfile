FROM ubuntu:14.04
MAINTAINER Daniele Venzano <venza@brownhat.org>

RUN apt-get update && apt-get install -y supervisor software-properties-common python-requests && apt-get clean
RUN apt-add-repository cloud-archive:mitaka
RUN apt-get update && apt-get install -y swift swift-proxy python-swiftclient python-keystoneclient python-keystonemiddleware

RUN mkdir -p /var/log/supervisor
ADD files/supervisord.conf /etc/supervisor/conf.d/swift-proxy.conf

RUN mkdir -p /swift-conf-tmp

ADD files/swift.conf /swift-conf-tmp/swift.conf
ADD files/proxy-server.conf /swift-conf-tmp/proxy-server.conf

ADD files/start.sh /usr/local/bin/start.sh
RUN chmod 755 /usr/local/bin/*.sh

EXPOSE 8080

CMD /usr/local/bin/start.sh

