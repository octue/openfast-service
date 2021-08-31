FROM gcc:9.4.0-buster

ENV PROJECT_ROOT=/app
WORKDIR $PROJECT_ROOT
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update -y && apt install -y git cmake libblas-dev liblapack-dev gfortran-8 g++

RUN git clone https://github.com/OpenFAST/OpenFAST.git

WORKDIR OpenFAST

RUN mkdir build

WORKDIR build

RUN cmake ..
RUN make -j openfast
RUN make install
