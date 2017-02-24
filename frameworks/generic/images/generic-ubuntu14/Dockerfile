FROM ubuntu:14.04

MAINTAINER Daniele Venzano <venza@brownhat.org>

######################################################
# This image is configured to support running:
#    - python scripts (version 2 & 3)
#    - tensorflow applications
#    - java applications (JDK8)
#    - bash scripts
#    - R scripts
######################################################


######################################################
#                    PYTHON 2 + 3
######################################################

# Dependencies for installing Python
sudo apt-get install -y --force-yes --no-install-recommends build-essential
sudo apt-get install -y --force-yes --no-install-recommends \
    libreadline-gplv2-dev \
    libncursesw5-dev \
    libssl-dev \
    libsqlite3-dev \
    tk-dev \
    libgdbm-dev \
    libc6-dev \
    libbz2-dev \
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
    python-wheel \
    && apt-get clean


# Download Python 2.7.9 and extract
mkdir $HOME/Downloads
cd $HOME/Downloads
wget https://www.python.org/ftp/python/2.7.9/Python-2.7.9.tgz
tar -xvf Python-2.7.9.tgz

# Install Python 2.7.9
cd $HOME/Downloads/Python-2.7.9
./configure
make
sudo make install

# Download python 3.4.3 and extract
cd $HOME/Downloads
wget https://www.python.org/ftp/python/3.4.3/Python-3.4.3.tgz
tar -xvf Python-3.4.3.tgz

# Install Python 3.4.3
cd $HOME/Downloads/Python-3.4.3
./configure
make
sudo make altinstall

#RUN python -m pip install --upgrade pip
wget https://bootstrap.pypa.io/ez_setup.py -O - | sudo python2.7
sudo easy_install-2.7 pip

wget https://bootstrap.pypa.io/ez_setup.py -O - | sudo python3.4
sudo easy_install-3.4 pip


##################################################
#                 JAVA 8
##################################################
RUN add-apt-repository ppa:webupd8team/java -y
RUN /bin/echo debconf shared/accepted-oracle-license-v1-1 select true | /usr/bin/debconf-set-selections
RUN apt-get update && apt-get install -y oracle-java8-installer

##################################################
#               TENSORFLOW
##################################################
# From binaries
ENV TF_BINARY_URL=export TF_BINARY_URL=https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-0.12.1-cp27-none-linux_x86_64.whl
RUN pip install --upgrade $TF_BINARY_URL
RUN apt-get install -y python-matplotlib

##################################################
#                  GPy
##################################################
RUN pip install --upgrade GPy paramz

##################################################
#                 GPFlow
##################################################
WORKDIR /opt
RUN git clone https://github.com/GPflow/GPflow.git
WORKDIR /opt/GPflow
RUN python setup.py install

#################################################
#        R
#################################################

## Emacs, make this -*- mode: sh; -*-

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
	&& apt-get install -t unstable -y --no-install-recommends \
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
COPY files/start-tf.sh /usr/local/bin/
CMD ["/usr/local/bin/start-tf.sh"]
RUN chmod 755 /usr/local/bin/start-tf.sh

ENTRYPOINT ["/bin/bash"]

