FROM ubuntu:14.04

MAINTAINER Daniele Venzano <venza@brownhat.org>

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install --yes --no-install-recommends --no-install-suggests boinc && apt-get clean && rm -Rf /var/lib/apt/lists/*

RUN mkdir /data
WORKDIR /data

COPY files/cc_config.xml /data

CMD /usr/bin/boinc --abort_jobs_on_exit --exit_when_idle --fetch_minimal_work --attach_project ${PROJECT_URL} ${PROJECT_KEY}
