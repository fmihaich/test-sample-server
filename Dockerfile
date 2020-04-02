FROM python:3.8

COPY . /test_sample_source
WORKDIR /test_sample_source

RUN pip3 install -r requirements.txt
