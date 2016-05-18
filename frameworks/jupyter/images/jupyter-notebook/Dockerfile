FROM ubuntu:14.04

MAINTAINER Daniele Venzano <venza@brownhat.org>

RUN apt-get update && apt-get install -y --force-yes software-properties-common python-software-properties
RUN apt-add-repository -y ppa:webupd8team/java
RUN /bin/echo debconf shared/accepted-oracle-license-v1-1 select true | /usr/bin/debconf-set-selections

RUN apt-get update && apt-get -y install oracle-java7-installer oracle-java7-set-default curl

ENV JAVA_HOME /usr/lib/jvm/java-7-oracle/

RUN sudo sh -c 'echo "deb http://cran.rstudio.com/bin/linux/ubuntu trusty/" >> /etc/apt/sources.list'

RUN apt-key adv --recv-keys --keyserver keyserver.ubuntu.com E084DAB9

WORKDIR /opt

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
    locales \
    libxrender1 \
    libopenblas-dev \
    r-base \
    libcurl4-openssl-dev \
    libssl-dev \
    && apt-get clean

RUN locale-gen en_US.UTF-8

# Install Tini
RUN wget --quiet https://github.com/krallin/tini/releases/download/v0.6.0/tini && \
    echo "d5ed732199c36a1189320e6c4859f0169e950692f451c03e7854243b95f4234b *tini" | sha256sum -c - && \
    mv tini /usr/local/bin/tini && \
    chmod +x /usr/local/bin/tini

# Configure environment
ENV CONDA_DIR /opt/conda
ENV PATH $CONDA_DIR/bin:$PATH
ENV SHELL /bin/bash
ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8

RUN mkdir /root/work && \
    mkdir /root/.jupyter && \
    mkdir /root/.local

RUN cd /tmp && \
    mkdir -p $CONDA_DIR && \
    wget http://repo.continuum.io/miniconda/Miniconda3-3.9.1-Linux-x86_64.sh && \
    echo "6c6b44acdd0bc4229377ee10d52c8ac6160c336d9cdd669db7371aa9344e1ac3 *Miniconda3-3.9.1-Linux-x86_64.sh" | sha256sum -c - && \
    /bin/bash Miniconda3-3.9.1-Linux-x86_64.sh -f -b -p $CONDA_DIR && \
    rm Miniconda3-3.9.1-Linux-x86_64.sh && \
    $CONDA_DIR/bin/conda install --yes conda==3.14.1

RUN conda install --yes \
    'notebook=4.1*' \
    terminado \
    'ipywidgets=4.0*' \
    'pandas=0.17*' \
    'matplotlib=1.4*' \
    'scipy=0.16*' \
    'seaborn=0.6*' \
    'scikit-learn=0.16*' \
    'statsmodels=0.6.1' \
    'ipyparallel' \
    'basemap' \
    'pillow' \
    && conda clean -yt

RUN /opt/conda/bin/pip install thunder-python showit

RUN wget https://oss.sonatype.org/content/repositories/snapshots/com/github/alexarchambault/jupyter/jupyter-scala-cli_2.11.6/0.2.0-SNAPSHOT/jupyter-scala_2.11.6-0.2.0-SNAPSHOT.tar.xz
RUN tar xvfJ jupyter-scala_2.11.6-0.2.0-SNAPSHOT.tar.xz && rm jupyter-scala_2.11.6-0.2.0-SNAPSHOT.tar.xz

RUN jupyter-scala_2.11.6-0.2.0-SNAPSHOT/bin/jupyter-scala

RUN R -e "install.packages(c('pbdZMQ', 'repr', 'devtools'), repos = 'http://cran.rstudio.com/')"
RUN R -e "devtools::install_github('irkernel/IRdisplay')"
RUN R -e "devtools::install_github('irkernel/IRkernel')"
RUN R -e "IRkernel::installspec(user = FALSE)"

# Configure container startup as root
EXPOSE 8888
RUN ln -s /mnt/workspace /root/work
WORKDIR /root/work
ENTRYPOINT ["tini", "--"]
CMD ["start-notebook.sh"]

# Add local files as late as possible to avoid cache busting
COPY files/start-notebook.sh /usr/local/bin/
RUN chmod 755 /usr/local/bin/start-notebook.sh
COPY files/jupyter_notebook_config.py /root/.jupyter/
RUN mkdir -p /root/.ipython/profile_default/startup/
