import vcr

from http.server import BaseHTTPRequestHandler
from loaded_cassette import LoadedCassette

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
        headers = vcr.request.HeadersDict(self.headers)
        body = None

        if 'Content-Length' in headers:
            content_length = int(headers['Content-Length'])
            body = self.rfile.read(content_length)
        
        request = vcr.request.Request(method, f"{LoadedCassette.cassette_host()}{self.path}", body, headers)

        response = LoadedCassette.vcr_cassette().responses_of(request)[0]
        response = vcr.filters.decode_response(response)
        
        self.send_response(response["status"]["code"])
        
        transfer_encoding_chunked = None
        
        for header_name, header_value in response["headers"].items():
            if header_name == 'Transfer-Encoding' and header_value == ['chunked']:
                transfer_encoding_chunked = True
                continue

            self.send_header(header_name, header_value[0])

        self.end_headers()

        if transfer_encoding_chunked:
            content = response["body"]["string"]
            to_write = f"{len(content)}\r\n{content}\r\n"
            self.wfile.write(to_write.encode("utf-8"))
            self.wfile.write("0\r\n\r\n".encode("utf-8"))
        else:
            self.wfile.write(response["body"]["string"])            


        # self.wfile.write('{"userId": 1}'.encode('utf-8'))