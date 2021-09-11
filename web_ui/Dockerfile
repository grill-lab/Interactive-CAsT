FROM python:slim

RUN pip3 install --upgrade pip

COPY web_ui/ /source

RUN pip3 install -r source/requirements.txt

WORKDIR /source

CMD python3 -u main.py