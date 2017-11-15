import requests

from mountebank import Imposter


def test_example():
    imposter = Imposter()
    imposter.add_stub("/test", "GET", "What I'm expecting")
    with imposter.mockhttp() as url:
        response = requests.get(url + "/test")
        response.raise_for_status()
        assert response.text == "What I'm expecting"

        response = requests.get(url + "/test")
        response.raise_for_status()
        assert response.text == "What I'm expecting"


def test_status_codes():

    imposter = Imposter()
    imposter.add_stub("/test", "GET", "Normal response")
    imposter.add_stub(
        "/test",
        "GET",
        "Response with a status code",
        status_code=418
    )

    with imposter.mockhttp() as url:
        response = requests.get(url + "/test")
        assert response.text == "Normal response"
        assert response.status_code == 200

        response = requests.get(url + "/test")
        assert response.text == "Response with a status code"
        assert response.status_code == 418


def test_repeat():
    imposter = Imposter()
    imposter.add_stub("/test", "GET", "Not what I'm expecting", repeat=2)
    imposter.add_stub("/test", "GET", "What I'm expecting")

    with imposter.mockhttp() as url:
        response = requests.get(url + "/test")
        assert response.text == "Not what I'm expecting"
        response = requests.get(url + "/test")
        assert response.text == "Not what I'm expecting"
        response = requests.get(url + "/test")
        assert response.text == "What I'm expecting"

        # Requests loop around when there's repetition
        response = requests.get(url + "/test")
        assert response.text == "Not what I'm expecting"


def test_implied_repeat():
    imposter = Imposter()
    imposter.add_stub("/test", "GET", "Not what I'm expecting")
    imposter.add_stub("/test", "GET", "What I'm expecting")

    with imposter.mockhttp() as url:
        response = requests.get(url + "/test")
        assert response.text == "Not what I'm expecting"

        response = requests.get(url + "/test")
        assert response.text == "What I'm expecting"

        response = requests.get(url + "/test")
        assert response.text == "Not what I'm expecting"


def test_get_requests():
    imposter = Imposter()
    with imposter.mockhttp() as url:
        requests.get(url + "/test")
        requests.get(url + "/anothertest")
        requests.get(url + "/why/not/another")

        mocked_requests = imposter.get_requests()
        assert len(mocked_requests) == 3
        assert mocked_requests[0]["path"] == "/test"
        assert mocked_requests[1]["path"] == "/anothertest"
        assert mocked_requests[2]["path"] == "/why/not/another"


def test_get_no_requests():
    imposter = Imposter()
    with imposter.mockhttp() as url:
        assert imposter.get_requests() == []


def test_static_port():
    imposter = Imposter()
    imposter.add_stub("/test", "GET", "What I'm expecting")
    with imposter.mockhttp(8080) as url:
        assert url == "http://mountebank:8080"
        assert imposter.port == 8080
        response = requests.get(url + "/test")
        response.raise_for_status()
        assert response.text == "What I'm expecting"
