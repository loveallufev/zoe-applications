FROM java:8

MAINTAINER Daniele Venzano <venza@brownhat.org>

# Install maven
RUN apt-get update && apt-get install -y maven git

ENV PATH /usr/lib/jvm/java-8-openjdk-amd64/bin:$PATH

ARG SPARK_VERSION
ENV SPARK_VERSION ${SPARK_VERSION:-branch-2.0}

ARG HADOOP_VERSION
ENV HADOOP_VERSION ${HADOOP_VERSION:-hadoop2.6}

ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64

WORKDIR /code

RUN git clone https://github.com/apache/spark.git
WORKDIR /code/spark
RUN git checkout $SPARK_VERSION

RUN build/mvn -Phadoop-2.6 -Dhadoop.version=2.6.1 -DskipTests clean package

ENV SPARK_HOME /code/spark
ENV PATH /code/spark/bin:/code/spark/sbin:${PATH}

RUN apt-get update && apt-get install -y --force-yes --no-install-recommends \
    git \
    vim \
    wget \
    build-essential \
    python-dev \
    ca-certificates \
    bzip2 \
    unzip \
    libsm6 \
    pandoc \
    texlive-latex-base \
    texlive-latex-extra \
    texlive-fonts-extra \
    texlive-fonts-recommended \
    texlive-generic-recommended \
    sudo \
    libxrender1 \
    libopenblas-dev \
    libjpeg-dev \
    && apt-get clean

# Install Tini
RUN wget --quiet https://github.com/krallin/tini/releases/download/v0.6.0/tini && \
    echo "d5ed732199c36a1189320e6c4859f0169e950692f451c03e7854243b95f4234b *tini" | sha256sum -c - && \
    mv tini /usr/local/bin/tini && \
    chmod +x /usr/local/bin/tini

# Configure environment
ENV CONDA_DIR /opt/conda
ENV HADOOP_HOME /opt/hadoop
ENV HADOOP_CONF_DIR $HADOOP_HOME/etc/hadoop
ENV PATH $HADOOP_HOME/bin:$CONDA_DIR/bin:$PATH
ENV PYTHONPATH $SPARK_HOME/python:$SPARK_HOME/python/lib/py4j-0.10.1-src.zip
ENV PYSPARK_PYTHON=/opt/conda/bin/python
ENV HADOOP_VERSION 2.6.1

# Install conda
RUN cd /tmp && \
    mkdir -p $CONDA_DIR && \
    wget http://repo.continuum.io/miniconda/Miniconda3-4.0.5-Linux-x86_64.sh && \
    echo "b1b15a3436bb7de1da3ccc6e08c7a5df *Miniconda3-4.0.5-Linux-x86_64.sh" | md5sum -c - && \
    /bin/bash Miniconda3-4.0.5-Linux-x86_64.sh -f -b -p $CONDA_DIR && \
    rm Miniconda3-4.0.5-Linux-x86_64.sh && \
    $CONDA_DIR/bin/conda install --yes conda

# Install Python 3 packages
RUN conda install --yes \
    'notebook=4.1*' \
    terminado \
    'pandas=0.18*' \
    'matplotlib=1.5*' \
    'scipy=0.17*' \
    'seaborn=0.6*' \
    'scikit-learn=0.17*' \
    'statsmodels=0.6.1' \
    'pillow' \
    'basemap' \
    && conda clean -yt

RUN /opt/conda/bin/pip install thunder-python
ENV PYTHONHASHSEED 0

RUN curl http://apache.mirrors.ovh.net/ftp.apache.org/dist/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz | tar -xz -C /opt/

RUN ln -s /opt/hadoop-${HADOOP_VERSION} /opt/hadoop

RUN mkdir /root/.jupyter && \
    mkdir /root/.local

COPY files/* /opt/

RUN chmod +x /opt/*.sh

# Configure container startup as root
EXPOSE 4040 8888
ENV WS_DIR /mnt/workspace
WORKDIR /mnt/workspace
ENTRYPOINT ["tini", "--"]
CMD ["start-notebook.sh"]

# Add local files as late as possible to avoid cache busting
COPY files/start-notebook.sh /usr/local/bin/
RUN chmod 755 /usr/local/bin/start-notebook.sh
COPY files/jupyter_notebook_config.py /root/.jupyter/
RUN mkdir -p /root/.ipython/profile_default/startup/
COPY files/00-pyspark-setup.py /root/.ipython/profile_default/startup/

COPY files/core-site.xml /opt
COPY files/hdfs-site.xml /opt

