FROM ubuntu:14.04

MAINTAINER Daniele Venzano <venza@brownhat.org>

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update \
    && apt-get install \
         --yes \
         --no-install-recommends \
         --no-install-suggests \
         boinc-client \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

CMD ["/usr/bin/boinc", "--attach_project", ${PROJECT_URL}, ${PROJECT_KEY}]
