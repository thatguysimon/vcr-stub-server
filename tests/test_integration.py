import threading
import time
import unittest
from urllib.request import urlopen

import requests
import pytest

from vcr_stub_server.stub_server_handler import BuildHandlerClassWithCassette
from vcr_stub_server.cassettes.vcrpy_cassette import VcrpyCassette
from http.server import HTTPServer


@pytest.fixture(scope="module")
def stub_server():
    host = "localhost"
    port = 8282

    vcr_cassette = VcrpyCassette(
        cassette_path="tests/fixtures/json_placeholder_crud.yaml"
    )

    handler_class = BuildHandlerClassWithCassette(vcr_cassette=vcr_cassette)

    http_server = HTTPServer((host, port), handler_class)

    server_thread = threading.Thread(target=http_server.serve_forever)
    server_thread.start()

    yield stub_server

    http_server.shutdown()
    server_thread.join()


def test_get_request(stub_server):
    response = requests.get("http://localhost:8282/posts")

    assert response.status_code == 200


def test_post_request(stub_server):
    response = requests.post(
        "http://localhost:8282/posts", json={"title": "foo", "body": "bar", "userId": 1}
    )

    assert response.status_code == 201


def test_patch_request(stub_server):
    response = requests.patch("http://localhost:8282/posts/1", json={"body": "baz"})

    assert response.status_code == 200


def test_put_request(stub_server):
    response = requests.put(
        "http://localhost:8282/posts/1",
        json={"title": "foo", "body": "baz", "userId": 1},
    )

    assert response.status_code == 200


def test_delete_request(stub_server):
    response = requests.delete("http://localhost:8282/posts/1")

    assert response.status_code == 200


def test_response_not_found(stub_server):
    response = requests.get("http://localhost:8282/unrecorded_request")

    assert response.status_code == 500
