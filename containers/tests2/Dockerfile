FROM python:2.7-alpine
MAINTAINER <infrastructure@quid.com>

RUN apk add --update bash

COPY ./requirements-dev.txt .
RUN pip install -r requirements-dev.txt

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./mountebank /apps/mountebank

# Sleep indefinitely
CMD ["sh", "-c", "tail -f /dev/null"]
