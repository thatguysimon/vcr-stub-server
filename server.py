from http.server import BaseHTTPRequestHandler
import vcr
from vcr.request import Request, HeadersDict
from urllib.parse import urlparse


class Server(BaseHTTPRequestHandler):
    def do_HEAD(self):
        return
      
    def do_GET(self):
        self.respond("GET")

    def do_DELETE(self):
        self.respond("DELETE")

    def do_POST(self):
        return

    def do_PATCH(self):
        return

    def do_PUT(self):
        return
      
    def respond(self, method, request):
        headers = HeadersDict(self.headers)
        request = Request(method, f"{cassette_host}{self.path}", None, headers)

        response = cassette.responses_of(request)[0]
        response = vcr.filters.decode_response(response)
        
        self.send_response(response["status"]["code"])
        
        for header_name, header_value in response["headers"].items():
            self.send_header(header_name, header_value[0])

        self.end_headers()
        self.wfile.write(response["body"]["string"])

