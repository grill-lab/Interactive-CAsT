FROM python:slim

RUN pip3 install --upgrade pip

COPY requirements.txt /requirements.txt

RUN pip3 install -r /requirements.txt

WORKDIR /source

CMD python3 -u main.py