FROM alpine:edge 
LABEL maintainer="kai@sassie.de"

RUN apk update
RUN apk --no-cache add python3 git gcc libffi-dev python3-dev musl-dev openssl-dev

COPY ./ /opt/Brain

RUN python3 -m ensurepip
RUN pip3 install --upgrade pip
RUN pip3 install -r /opt/Brain/requirements.txt

RUN export FLASK_APP=brain.py && cd /opt/Brain && flask db init && flask db migrate && flask db upgrade

ENTRYPOINT python3 /opt/Brain/brain.py
 


