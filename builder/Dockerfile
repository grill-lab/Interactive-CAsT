FROM python:slim

LABEL Author="Paul Owoicho"

RUN pip3 install --upgrade pip
RUN pip3 install grpcio grpcio_tools

COPY builder/ /source

WORKDIR /source

CMD bash build_protos.sh