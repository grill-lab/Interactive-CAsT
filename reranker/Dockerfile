FROM  nvidia/cuda:11.4.1-runtime-ubuntu18.04

LABEL Author="Paul Owoicho"

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    build-essential \
    git \
    wget vim \
    software-properties-common \
    locales \
    unzip

RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en

RUN add-apt-repository -y ppa:deadsnakes/ppa

RUN apt-get install -y python3 \
    python3-pip \
    python-setuptools

RUN pip3 install --upgrade pip

RUN apt-get install -y openjdk-11-jdk

# Install Rust for M1 Compatibility
RUN apt-get install -y curl
RUN curl https://sh.rustup.rs -sSf | bash -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

COPY requirements.txt /requirements.txt

COPY rerankers/pygaggle/requirements.txt /pygaggle_requirements.txt

RUN pip3 install -r /requirements.txt -r /pygaggle_requirements.txt

WORKDIR /source

CMD python3 -u main.py