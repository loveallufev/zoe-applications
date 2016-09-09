#!/bin/sh

set -x

cp -a /swift-conf-tmp/* /etc/swift/

sed -i "s/SED_MEMCACHED_SERVER/$MEMCACHED_SERVER/" /etc/swift/proxy-server.conf
# sed -i "s/SED_USERNAME/$OS_USERNAME/" /etc/swift/proxy-server.conf
# sed -i "s/SED_PASSWORD/$OS_PASSWORD/" /etc/swift/proxy-server.conf
# sed -i "s/SED_PROJECT_NAME/$PROJECT_NAME/" /etc/swift/proxy-server.conf
# sed -i "s/SED_AUTH_HOST/$AUTH_HOST/" /etc/swift/proxy-server.conf
# sed -i "s+SED_AUTH_URI+$AUTH_URI+" /etc/swift/proxy-server.conf
# sed -i "s+SED_AUTH_URL+$AUTH_URL+" /etc/swift/proxy-server.conf

supervisord --nodaemon

