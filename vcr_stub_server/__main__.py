#!/usr/bin/env python3

import argparse
import time
import os.path

from http.server import HTTPServer

from vcr_stub_server.stub_server_handler import BuildHandlerClassWithCassette
from vcr_stub_server.cassettes.vcrpy_cassette import VcrpyCassette


CASSETTE_FORMAT_TO_CLASS = {"vcrpy": VcrpyCassette}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--bind",
        "-b",
        default="localhost",
        metavar="ADDRESS",
        help="Specify alternate bind address " "[default: all interfaces]",
    )
    parser.add_argument(
        "--port",
        "-p",
        action="store",
        default=8181,
        type=int,
        nargs="?",
        help="Specify alternate port [default: 8000]",
    )
    parser.add_argument(
        "--cassette-format",
        "-cf",
        action="store",
        choices=CASSETTE_FORMAT_TO_CLASS.keys(),
        default="vcrpy",
        type=str,
        help="Specify VCR implementation [default: vcrpy]",
    )
    parser.add_argument(
        "path",
        action="store",
        default=8181,
        type=str,
        metavar="FILE",
        help="Specify the VCR Casette file path",
    )
    args = parser.parse_args()

    host = args.bind
    port = args.port
    cassette_path = args.path

    if not os.path.isfile(cassette_path):
        raise ValueError("Invalid cassette file path")

    vcr_cassette = CASSETTE_FORMAT_TO_CLASS[args.cassette_format](
        cassette_path=cassette_path
    )
    handler_class = BuildHandlerClassWithCassette(vcr_cassette=vcr_cassette)

    print(time.asctime(), f"Starting VCR stub server for cassette: {cassette_path}")
    http_server = HTTPServer((host, port), handler_class)

    try:
        print(time.asctime(), f"Server started, serving on {host}:{port}")
        http_server.serve_forever()
    except KeyboardInterrupt:
        pass

    http_server.server_close()
    print(time.asctime(), "Stopped server - %s:%s" % (host, port))


if __name__ == "__main__":
    main()
