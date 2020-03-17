import threading
import time
import unittest
from urllib.request import urlopen

import requests
import pytest

from vcrpy_stub_server.stub_server_handler import StubServerHandler
from http.server import HTTPServer
from vcrpy_stub_server.loaded_cassette import LoadedCassette


@pytest.fixture(scope="module")
def stub_server():
    host = "localhost"
    port = 8181
    http_server = HTTPServer((host, port), StubServerHandler)

    server_thread = threading.Thread(target=http_server.serve_forever)
    server_thread.start()

    yield stub_server
    
    http_server.shutdown()
    server_thread.join()


def test_get_request(stub_server):
    LoadedCassette("tests/fixtures/get_posts.yaml")
    response = requests.get("http://localhost:8181/posts")
    
    assert response.status_code == 200


def test_post_request(stub_server):
    LoadedCassette("tests/fixtures/post_post.yaml")
    response = requests.post("http://localhost:8181/posts", json={
        "title": "foo",
        "body": "bar",
        "userId": 1
    })
    
    assert response.status_code == 201


if __name__ == '__main__':
    unittest.main()