FROM python:slim

LABEL Author="Paul Owoicho"

RUN pip3 install --upgrade pip
RUN pip3 install grpcio grpcio_tools

COPY ./ /source

CMD bash /source/build_protos.sh