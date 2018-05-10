import json
import logging
from contextlib import contextmanager

import requests
import requests.exceptions
from tenacity import retry, wait_fixed, stop_after_attempt


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

    def __init__(self, mountebank_scheme="http", mountebank_host="mountebank",
        mountebank_port=2525):
        """Instantiates a new Imposter instance.

        Args:
            mountebank_scheme (str): Optional scheme to use to connect with
            mountebank.
            mountebank_host (str): Optional host to use to connect with
            mountebank.
            mountebank_port (int): Optional port to use to connect with
            mountebank.
        """
        self.port = None
        self.mountebank_scheme = mountebank_scheme
        self.mountebank_host = mountebank_host
        self.mountebank_port = mountebank_port
        self.mountebank_url = "%s://%s:%s" % (
            mountebank_scheme, mountebank_host, mountebank_port)

        self._imposter = {
            "protocol": "http",
            "stubs": [{
                "responses": [
                    {"is": {"statusCode": 404}}
                ]
            }]
        }

    def add_stub(self, path, method, body, repeat=0, status_code=200):
        """Adds a stub to mock.

        Args:
            path (str): The path being mocked.
            path (str): The method being mocked.
            body (str): The text the mock should return.
            repeat (int): The total number of times to repeat a response. If
            not set then the response will repeat indefinitely.
            status_code (int): The status code to return.
        """
        predicates = [{
            "equals": {
                "method": method,
                "path": path
            }
        }]
        responses = [{
            "is": {
                "statusCode": status_code,
                "body": body
            }
        }]

        if repeat > 0:
            responses = responses * repeat

        # Check to see if a stub already exists for the predicates. If so,
        # update the existing stub.
        predicates_exists = False
        for stub in self._imposter["stubs"]:
            if "predicates" in stub and stub["predicates"] == predicates:
                predicates_exists = True
                stub["responses"] += responses
                break

        # Add the new stub near the bottom before our catch-all
        if not predicates_exists:
            self._imposter["stubs"].insert(len(self._imposter["stubs"]) - 1, {
                "predicates": predicates,
                "responses": responses
            })

    @contextmanager
    def mockhttp(self, port=None, wait_for_mountebank=True):
        """A contextmanager that uses mountebank to mock out a service.

        Args:
            port (int): Optional static port to open for the new mock service.
            If not provided a port will be randomly generated.
            wait_for_mountebank (bool): Whether or not to wait for mountebank
            to become available. This is useful in containers where mountebank
            might still be loading while tests are running. By default this
            function will wait a few seconds for mountebank to become
            available. Set to False to not wait at all.

        Yields:
            str: The URL to the mocked service.
        """
        if wait_for_mountebank:
            self.wait()

        if port:
            self._imposter["port"] = port

        response = requests.post(self.mountebank_url + "/imposters",
            data=json.dumps(self._imposter))

        try:
            response.raise_for_status()

        except requests.exceptions.HTTPError:
            logger.exception("Mountebank returned: %s", response.text)
            raise

        self.port = response.json()["port"]
        url = "%s://%s:%s" % (
            self.mountebank_scheme, self.mountebank_host, self.port)

        try:
            yield url

        finally:
            response = requests.delete("%s/imposters/%s" % (
                self.mountebank_url, self.port))

            try:
                response.raise_for_status()

            except requests.exceptions.HTTPError:
                logger.exception(
                    "Unable to delete mountebank mock: %s", response.text)
                raise

    def get_requests(self):
        """Retrieves the requests received by the mock service.

        Returns:
            dict: The requests received by the mock service.
        """
        response = requests.get("%s/imposters/%s" % (
            self.mountebank_url, self.port))
        response_data = response.json()
        return response_data["requests"]

    def wait(self):
        """Blocks until mountebank is accessible (or waiting times out).
        """
        def wait():
            requests.get(self.mountebank_url).raise_for_status()

        retry(wait=wait_fixed(1000), stop=stop_after_attempt(10))(wait)()
