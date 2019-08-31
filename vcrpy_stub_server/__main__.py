#!/usr/bin/env python3

import time
import argparse

from http.server import HTTPServer

from loaded_cassette import LoadedCassette
from stub_server_handler import StubServerHandler


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

    host = args.bind
    port = args.port
    cassette_path = args.path

    LoadedCassette(cassette_path)

    print(time.asctime(), f"Starting VCR stub server for cassette: {cassette_path} on {host}:{port}")
    http_server = HTTPServer((host, port), StubServerHandler)

    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        pass
    
    http_server.server_close()
    print(time.asctime(), "Stopped HTTP server - %s:%s" % (host, port))