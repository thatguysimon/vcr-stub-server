import vcr
from vcr.cassette import Cassette
from urllib.parse import urlparse

routes = {}

cassette = Cassette.load(path='test.yaml')

for request in cassette.requests:
	parsed_url = urlparse(request.uri)
	routes[parsed_url.path] = cassette.responses_of(request)[0]