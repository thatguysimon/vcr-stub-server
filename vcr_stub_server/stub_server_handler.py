from urllib.parse import urlparse

from http.server import BaseHTTPRequestHandler
from vcr.cassette import Cassette
import vcr


def BuildHandlerClassWithCassette(cassette_path=None):
    class StubServerHandler(BaseHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            self.vcrpy_cassette, self.vcr_cassette_host = _load_cassette(cassette_path)

            super().__init__(*args, **kwargs)

        def do_HEAD(self):
            return
          
        def do_GET(self):
            self.respond("GET")

        def do_DELETE(self):
            self.respond("DELETE")

        def do_POST(self):
            self.respond("POST")

        def do_PATCH(self):
            self.respond("PATCH")

        def do_PUT(self):
            self.respond("PUT")
          
        def respond(self, method):
            request_headers = vcr.request.HeadersDict(self.headers)
            request_body = None

            if 'Content-Length' in request_headers:
                request_content_length = int(request_headers['Content-Length'])
                request_body = self.rfile.read(request_content_length)
            
            request = vcr.request.Request(method, f"{self.vcr_cassette_host}{self.path}", request_body, request_headers)

            encoded_response = self.vcrpy_cassette.responses_of(request)[0]
            response = vcr.filters.decode_response(encoded_response)
            
            self.send_response(response["status"]["code"], response["status"]["message"])
            
            for header_name, header_value in response["headers"].items():
                # Ignore Transfer-Encoding and Content-Endcoding for now
                if header_name.lower() in ['content-encoding', 'transfer-encoding']:
                    continue

                self.send_header(header_name, header_value[0])

            self.end_headers()

            self.wfile.write(response["body"]["string"])

    return StubServerHandler

def _load_cassette(cassette_path):
    vcrpy_cassette = Cassette.load(path=cassette_path)
    vcr_cassette_host = None

    for request in vcrpy_cassette.requests:
        parsed_url = urlparse(request.uri)
        current_interaction_request_host = f"{parsed_url.scheme}://{parsed_url.netloc}"

        if current_interaction_request_host != vcr_cassette_host and vcr_cassette_host != None:
            raise Exception("More than one host found in cassette interactions")
        
        if vcr_cassette_host == None:
            vcr_cassette_host = current_interaction_request_host

    return vcrpy_cassette, vcr_cassette_host
