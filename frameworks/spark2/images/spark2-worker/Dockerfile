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

# Configure environment
ENV CONDA_DIR /opt/conda
ENV PATH $CONDA_DIR/bin:$PATH
ENV PYTHONPATH $SPARK_HOME/python:$SPARK_HOME/python/lib/py4j-0.8.2.1-src.zip
ENV PYSPARK_PYTHON=/opt/conda/bin/python

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
    'pandas=0.18*' \
    'matplotlib=1.5*' \
    'scipy=0.17*' \
    'seaborn=0.6*' \
    'scikit-learn=0.17*' \
    'statsmodels=0.6.1' \
    'pillow' \
    && conda clean -yt

RUN /opt/conda/bin/pip install thunder-python
ENV PYTHONHASHSEED 0

COPY files/* /opt/
RUN chmod +x /opt/*.sh
EXPOSE 8888 8081

ENV SPARK_WORKER_PORT 8888
ENV SPARK_WORKER_WEBUI_PORT 8081

CMD /opt/start-worker.sh
