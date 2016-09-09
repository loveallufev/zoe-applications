#!/bin/sh

set -x

cp -a /swift-conf-tmp/* /etc/swift/

supervisord --nodaemon

