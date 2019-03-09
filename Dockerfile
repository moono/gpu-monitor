FROM nvidia/cuda:9.0-cudnn7-runtime-ubuntu16.04

MAINTAINER mookyung "toilety@gmail.com"

RUN apt-get update && apt-get install -y \
    build-essential \
    software-properties-common \
    docker.io

# install python3.6
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update && apt-get install -y \
    python3.6 \
    python3.6-dev \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# set python shortcut
RUN ln -sfn /usr/bin/python3.6 /usr/bin/python3 && \
    ln -sfn /usr/bin/python3 /usr/bin/python && \
    ln -sfn /usr/bin/pip3 /usr/bin/pip

# copy current sources & install requred packages
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt

# set port
EXPOSE 3033

# set commands
CMD ["python", "simple_rest_api.py"]
