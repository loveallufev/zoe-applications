FROM ubuntu:16.04
#FROM debian:testing

MAINTAINER Daniele Venzano <venza@brownhat.org>

ENV DEBIAN_FRONTEND noninteractive

######################################################
# This image is configured to support running:
#    - python scripts (version 2 & 3)
#    - java applications (JDK8)
#    - bash scripts
#    - R scripts
######################################################


######################################################
#                    PYTHON 2 + 3
######################################################

# Dependencies for installing Python
RUN apt-get update

RUN apt-get install -y --force-yes --no-install-recommends build-essential
RUN apt-get install -y --force-yes --no-install-recommends \
    libreadline-gplv2-dev \
    libncursesw5-dev \
    libssl-dev \
    libsqlite3-dev \
    tk-dev \
    libgdbm-dev \
    libc6-dev \
    libbz2-dev \
    python-dev \
    software-properties-common \
    curl \
    pkg-config \
    zip \
    g++ \
    zlib1g-dev \
    unzip \
    swig \
    git \
    wget \
    python-pip \
    python-numpy \
    swig \
    python-wheel \
    && apt-get clean


RUN apt-get install python
RUN python -m pip install --upgrade pip
RUN apt-get install -y python-matplotlib

##################################################
#                 JAVA 8
##################################################

RUN apt update
RUN rm -f /etc/apt/sources.list.d/webupd8team-java.list
RUN add-apt-repository ppa:webupd8team/java
RUN echo debconf shared/accepted-oracle-license-v1-1 select true | debconf-set-selections
RUN echo debconf shared/accepted-oracle-license-v1-1 seen true | debconf-set-selections


RUN apt update; apt install -y --force-yes --no-install-recommends --allow-unauthenticated oracle-java8-installer
RUN apt install -y --allow-unauthenticated oracle-java8-set-default

#################################################
#        R
#################################################

## Emacs, make this -*- mode: sh; -*-


#RUN /bin/bash -c "gpg --keyserver pgpkeys.mit.edu --recv-key  010908312D230C5F"
#RUN /bin/bash -c "gpg -a --export 010908312D230C5F | sudo apt-key add -"
RUN apt-get update

## This handle reaches Carl and Dirk
# MAINTAINER "Carl Boettiger and Dirk Eddelbuettel" rocker-maintainers@eddelbuettel.com
# from  https://github.com/rocker-org/rocker
## Set a default user. Available via runtime flag `--user docker` 
## Add user to 'staff' group, granting them write privileges to /usr/local/lib/R/site.library
## User should also have & own a home directory (for rstudio or linked volumes to work properly). 
RUN useradd docker \
	&& mkdir /home/docker \
	&& chown docker:docker /home/docker \
	&& addgroup docker staff

RUN apt-get update \ 
	&& apt-get install -y --no-install-recommends \
		ed \
		less \
		locales \
		vim-tiny \
		wget \
		ca-certificates \
		fonts-texgyre \
	&& rm -rf /var/lib/apt/lists/*

## Configure default locale, see https://github.com/rocker-org/rocker/issues/19
RUN echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen \
	&& locale-gen en_US.utf8 \
	&& /usr/sbin/update-locale LANG=en_US.UTF-8

## Use Debian unstable via pinning -- new style via APT::Default-Release
RUN echo "deb http://http.debian.net/debian sid main" > /etc/apt/sources.list.d/debian-unstable.list \
	&& echo 'APT::Default-Release "testing";' > /etc/apt/apt.conf.d/default

ENV R_BASE_VERSION 3.3.2

## Now install R and littler, and create a link for littler in /usr/local/bin
## Also set a default CRAN repo, and make sure littler knows about it too
RUN apt-get update \
	&& apt-get install -t unstable -y --allow-unauthenticated --no-install-recommends \
		littler \
                r-cran-littler \
		r-base=${R_BASE_VERSION}* \
		r-base-dev=${R_BASE_VERSION}* \
		r-recommended=${R_BASE_VERSION}* \
        && echo 'options(repos = c(CRAN = "https://cran.rstudio.com/"), download.file.method = "libcurl")' >> /etc/R/Rprofile.site \
        && echo 'source("/etc/R/Rprofile.site")' >> /etc/littler.r \
	&& ln -s /usr/share/doc/littler/examples/install.r /usr/local/bin/install.r \
	&& ln -s /usr/share/doc/littler/examples/install2.r /usr/local/bin/install2.r \
	&& ln -s /usr/share/doc/littler/examples/installGithub.r /usr/local/bin/installGithub.r \
	&& ln -s /usr/share/doc/littler/examples/testInstalled.r /usr/local/bin/testInstalled.r \
	&& install.r docopt \
	&& rm -rf /tmp/downloaded_packages/ /tmp/*.rds \
	&& rm -rf /var/lib/apt/lists/*




##################################################
#            ENVIRONMENT VARIABLES
##################################################
# Configure environment
ENV JAVA_HOME /usr/lib/jvm/java-8-oracle/
ENV SHELL /bin/bash
ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8



# Configure container startup as root
EXPOSE 6006

VOLUME /mnt/workspace
WORKDIR /mnt/workspace

ENV WS_DIR /mnt/workspace
#COPY files/start-tf.sh /usr/local/bin/
#CMD ["/usr/local/bin/start-tf.sh"]
#RUN chmod 755 /usr/local/bin/start-tf.sh

ENTRYPOINT ["/bin/bash"]

