#!/usr/bin/env python3
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
import vcr
from vcr.cassette import Cassette
from vcr.request import Request, HeadersDict
import argparse
from urllib.parse import urlparse


class Server(BaseHTTPRequestHandler):
    def do_HEAD(self):
        return
      
    def do_GET(self):
        self.respond("GET")

    def do_DELETE(self):
        return

    def do_POST(self):
        return

    def do_PATCH(self):
        return

    def do_PUT(self):
        return
      
    def respond(self, method):
        headers = HeadersDict(self.headers)
        request = Request(method, f"{LoadedCassette.host()}{self.path}", None, headers)

        response = LoadedCassette.instance().responses_of(request)[0]
        response = vcr.filters.decode_response(response)
        
        self.send_response(response["status"]["code"])
        
        for header_name, header_value in response["headers"].items():
            self.send_header(header_name, header_value[0])

        self.end_headers()
        self.wfile.write(response["body"]["string"])


class LoadedCassette:
    __instance = None
    __host = None
   
    def __init__(self, cassette_path):
        if LoadedCassette.__instance != None:
            raise Exception("Cannot instantiate another instance of a singleton")

        LoadedCassette.__instance = Cassette.load(path=cassette_path)

        for request in LoadedCassette.__instance.requests:
            parsed_url = urlparse(request.uri)
            current_interaction_request_host = f"{parsed_url.scheme}://{parsed_url.netloc}"
            
            if current_interaction_request_host != LoadedCassette.__host and LoadedCassette.__host != None:
                raise Exception("More than one host found in cassette interactions")
            if LoadedCassette.__host == None:
                LoadedCassette.__host = current_interaction_request_host

    @staticmethod 
    def instance():
        if LoadedCassette.__instance == None:
            raise
        return LoadedCassette.__instance

    @staticmethod 
    def host():
        if LoadedCassette.__instance == None:
            raise
        return LoadedCassette.__host


if __name__ == "__main__":    
    parser = argparse.ArgumentParser()
    parser.add_argument("--bind", "-b", default="localhost", metavar="ADDRESS",
                        help="Specify alternate bind address "
                             "[default: all interfaces]")
    parser.add_argument("--port", "-p", action="store",
                        default=8181, type=int,
                        nargs="?",
                        help="Specify alternate port [default: 8000]")
    parser.add_argument("path", action="store",
                        default=8181, type=str, metavar="FILE",
                        help="Specify the VCR Casette file path")
    args = parser.parse_args()

    host_name = args.bind
    port_number = args.port
    cassette_path = args.path

    LoadedCassette(cassette_path)

    print(time.asctime(), f"Starting VCR stub server for cassette: {cassette_path}")

    httpd = HTTPServer((host_name, port_number), Server)
    print(time.asctime(), "Started HTTP server - %s:%s" % (host_name, port_number))
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    
    httpd.server_close()
    print(time.asctime(), "Stopped HTTP server - %s:%s" % (host_name, port_number))