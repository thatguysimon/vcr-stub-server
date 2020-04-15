from http.server import BaseHTTPRequestHandler


def BuildHandlerClassWithCassette(vcr_cassette):
    class StubServerHandler(BaseHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            self.vcr_cassette = vcr_cassette

            super().__init__(*args, **kwargs)

        def do_HEAD(self):
            return

        def do_GET(self):
            self._respond(method="GET")

        def do_DELETE(self):
            self._respond(method="DELETE")

        def do_POST(self):
            self._respond(method="POST")

        def do_PATCH(self):
            self._respond(method="PATCH")

        def do_PUT(self):
            self._respond(method="PUT")

        def _respond(self, method: str):
            request_body = None

            if "Content-Length" in self.headers:
                request_content_length = int(self.headers["Content-Length"])
                request_body = self.rfile.read(request_content_length)

            response = self.vcr_cassette.response_for(
                method=method, path=self.path, body=request_body, headers=self.headers,
            )

            self.send_response(
                response["status"]["code"], response["status"]["message"]
            )

            for header_name, header_value in response["headers"].items():
                # Ignore Transfer-Encoding and Content-Endcoding for now
                if header_name.lower() in ["content-encoding", "transfer-encoding"]:
                    continue

                self.send_header(header_name, header_value[0])

            self.end_headers()

            self.wfile.write(response["body"]["string"])

    return StubServerHandler
