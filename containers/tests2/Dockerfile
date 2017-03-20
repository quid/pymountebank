FROM quid-dock.jfrog.io/python:2.7
MAINTAINER <infrastructure@quid.com>

COPY ./requirements-dev.txt .
RUN pip install -r requirements-dev.txt

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./mountebank /apps/mountebank

# Sleep indefinitely
CMD ["sh", "-c", "tail -f /dev/null"]
