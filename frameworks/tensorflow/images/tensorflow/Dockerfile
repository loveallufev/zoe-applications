FROM ubuntu:14.04

MAINTAINER Pietro Michiardi <Pietro.Michiardi@eurecom.fr>

ENV DEBIAN_FRONTEND noninteractive

##################################################
# BASELINE
##################################################
RUN apt-get update && apt-get install -y --force-yes --no-install-recommends \
    python-pip \
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
    python-numpy \
    swig \
    python-dev \
    python-wheel \
    && apt-get clean

RUN python -m pip install --upgrade pip

##################################################
# JAVA
##################################################
RUN add-apt-repository ppa:webupd8team/java -y
RUN /bin/echo debconf shared/accepted-oracle-license-v1-1 select true | /usr/bin/debconf-set-selections
RUN apt-get update && apt-get install -y oracle-java8-installer

##################################################
# TENSORFLOW
##################################################
# From binaries
ENV TF_BINARY_URL=export TF_BINARY_URL=https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-0.12.1-cp27-none-linux_x86_64.whl
RUN pip install --upgrade $TF_BINARY_URL
RUN apt-get install -y python-matplotlib


##################################################
# GPy
##################################################
RUN pip install --upgrade GPy paramz

##################################################
# GPFlow
##################################################
WORKDIR /opt
RUN git clone https://github.com/GPflow/GPflow.git
WORKDIR /opt/GPflow
RUN python setup.py install

##################################################
# SETUP ZOE APP
##################################################
# Configure environment
ENV JAVA_HOME /usr/lib/jvm/java-8-oracle/
ENV SHELL /bin/bash
ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8

# Configure container startup as root
EXPOSE 6006
WORKDIR /mnt/workspace
ENV WS_DIR /mnt/workspace
COPY files/start-tf.sh /usr/local/bin/
CMD ["/usr/local/bin/start-tf.sh"]
RUN chmod 755 /usr/local/bin/start-tf.sh
