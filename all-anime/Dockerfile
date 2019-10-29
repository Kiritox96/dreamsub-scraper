FROM python:3

RUN pip install requests

RUN pip install dnspython

RUN pip install pymongo

COPY ./pi.py /

ENTRYPOINT python pi.py >> /tmp/output.log 2>&1

