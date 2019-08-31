import threading
import time
import unittest
from urllib.request import urlopen

import requests

from vcrpy_stub_server.stub_server_handler import StubServerHandler
from http.server import HTTPServer
from vcrpy_stub_server.loaded_cassette import LoadedCassette


class TestRequests(unittest.TestCase):

    def setUp(self):
        host = "localhost"
        port = 8181
        self.http_server = HTTPServer((host, port), StubServerHandler)

        self.server_thread = threading.Thread(target=self.http_server.serve_forever)
        self.server_thread.start()

    def tearDown(self):
        self.http_server.shutdown()
        self.server_thread.join()

    def test_get_request(self):
        LoadedCassette("tests/fixtures/get_posts.yaml")
        response = requests.get("http://localhost:8181/posts")
        
        assert response.status_code == 200

    def test_post_request(self):
        LoadedCassette("tests/fixtures/post_post.yaml")
        response = requests.post("http://localhost:8181/posts", json={
            "title": "foo",
            "body": "bar",
            "userId": 1
        })
        
        assert response.status_code == 201

if __name__ == '__main__':
    unittest.main()