FROM            python:3.9-slim as base

WORKDIR         /opt/code/

RUN             pip install -U pip

COPY            requirements.txt requirements.txt

FROM            base as app

COPY            searchapp/ searchapp/
COPY            app.py app.py

ENTRYPOINT      ["python", "app.py"]

FROM            base as test

COPY            requirements-dev.txt requirements-dev.txt
RUN             pip install -r requirements-dev.txt
