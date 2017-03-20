# Mountebank

This is a simple wrapper library around mountebank. It's useful for mocking
HTTP API services.

## Usage

    from mountebank import Imposter

    imposter = Imposter()
    imposter.add_stub("/text", "GET", "What I'm expecting")
    with imposter.mockhttp() as url:
        assert requests.get(url + "/test").text == "What I'm expecting"
