import vcr

from http.server import BaseHTTPRequestHandler
from vcr_stub_server.loaded_cassette import LoadedCassette

class StubServerHandler(BaseHTTPRequestHandler):
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
        
        request = vcr.request.Request(method, f"{LoadedCassette.cassette_host()}{self.path}", request_body, request_headers)

        response = LoadedCassette.vcr_cassette().responses_of(request)[0]
        response = vcr.filters.decode_response(response)
        
        self.send_response(response["status"]["code"], response["status"]["message"])
        
        for header_name, header_value in response["headers"].items():
            # Ignore Transfer-Encoding and Content-Endcoding for now
            if header_name.lower() in ['content-encoding', 'transfer-encoding']:
                continue

            self.send_header(header_name, header_value[0])

        self.end_headers()

        self.wfile.write(response["body"]["string"])
