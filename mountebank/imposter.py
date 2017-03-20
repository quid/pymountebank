import json
import logging
from contextlib import contextmanager

import requests
import requests.exceptions


logger = logging.getLogger(__name__)


class Imposter(object):
    """Represents a mountebank imposter.

    This is used to mock services.

    Usage:
        imposter = Imposter()
        imposter.add_stub("/test", "GET", "What I'm expecting")
        with imposter.mockhttp() as url:
            assert requests.get(url + "/test").text == "What I'm expecting"
    """

    def __init__(self):
        """Instantiates a new Imposter instance.
        """
        self._imposter = {
            "protocol": "http",
            "stubs": [{
                "responses": [
                    {"is": {"statusCode": 404}}
                ]
            }]
        }

    def add_stub(self, path, method, body):
        """Adds a stub to mock.

        Args:
            path (str): The path being mocked.
            path (str): The method being mocked.
            body (str): The text the mock should return.
        """
        index = len(self._imposter["stubs"]) - 1

        self._imposter["stubs"].insert(index, {
            "predicates": [{
                "equals": {
                    "method": method,
                    "path": path
                }
            }],
            "responses": [{
                "is": {
                    "statusCode": 200,
                    "body": body
                }
            }]
        })

    @contextmanager
    def mockhttp(self, mountebank_scheme="http", mountebank_host="mountebank",
        mountebank_port=2525):
        """A contextmanager that uses mountebank to mock out a service.

        Args:
            imposter (dict): The mountebank imposter definition.
            mountebank_url (str): Optional URL to communicate with mountebank.

        Yields:
            str: The URL to the mocked service.
        """
        mountebank_url = "%s://%s:%s" % (
            mountebank_scheme, mountebank_host, mountebank_port)
        response = requests.post(mountebank_url + "/imposters",
            data=json.dumps(self._imposter))

        try:
            response.raise_for_status()

        except requests.exceptions.HTTPError:
            logger.exception("Mountebank returned: %s", response.text)
            raise

        port = response.json()["port"]
        url = "%s://%s:%s" % (mountebank_scheme, mountebank_host, port)

        try:
            yield url

        finally:
            response = requests.delete("%s/imposters/%s" % (
                mountebank_url, port))

            try:
                response.raise_for_status()

            except requests.exceptions.HTTPError:
                logger.exception(
                    "Unable to delete mountebank mock: %s", response.text)
                raise
