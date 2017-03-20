import requests

from mountebank import Imposter


def test_example():
    imposter = Imposter()
    imposter.add_stub("/test", "GET", "What I'm expecting")
    with imposter.mockhttp() as url:
        response = requests.get(url + "/test")
        response.raise_for_status()
        assert response.text == "What I'm expecting"
