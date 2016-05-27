# Spark submit image

This image contains the Spark submit process. It is used by Zoe, the Container Analytics as a
Service system to create on-demand Spark clusters.

Zoe can be found at: https://github.com/DistributedSystemsGroup/zoe

## Setup

The Dockerfile expects a number of environment variables to configure its behaviour:

* SPARK\_MASTER\_IP: IP address of the Spark master this notebook should use for its kernel
* SPARK\_EXECUTOR\_RAM: How much RAM to use for each executor spawned by the notebook
* APPLICATION\_ID: a string identifing the application to be run, a directory will be created with this name in the container's /tmp
* APPLICATION\_URL: the URL of a .zip file containing all the necessary application files (JARs, libraries, .py files, etc.)
* SPARK\_OPTIONS: additional options to pass to spark-submit

To run, by hand use:
```
docker run -i -t <environment variables> zoerepo/spark-submit <commandline normally passed to spark-submit>
```

