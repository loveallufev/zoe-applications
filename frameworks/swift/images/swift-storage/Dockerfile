FROM ubuntu:14.04
MAINTAINER Daniele Venzano <venza@brownhat.org>

RUN apt-get update && apt-get install -y supervisor software-properties-common python-requests && apt-get clean
RUN apt-add-repository cloud-archive:mitaka
RUN apt-get update && apt-get install -y swift swift-account swift-container swift-object rsync && apt-get clean

RUN mkdir -p /var/log/supervisor
ADD files/supervisord.conf /etc/supervisor/conf.d/swift-storage.conf

ADD files/rsyncd.conf /etc/rsyncd.conf 

RUN mkdir -p /swift-conf-tmp

ADD files/swift.conf /swift-conf-tmp/swift.conf
ADD files/account-server.conf /swift-conf-tmp/account-server.conf
ADD files/object-server.conf /swift-conf-tmp/object-server.conf
ADD files/container-server.conf /swift-conf-tmp/container-server.conf

ADD files/start.sh /usr/local/bin/start.sh
RUN chmod 755 /usr/local/bin/*.sh

RUN mkdir -p /var/cache/swift

RUN perl -pi -e 's/RSYNC_ENABLE=false/RSYNC_ENABLE=true/' /etc/default/rsync

CMD /usr/local/bin/start.sh

