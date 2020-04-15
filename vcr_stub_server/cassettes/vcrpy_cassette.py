from urllib.parse import urlparse, quote

from vcr_stub_server.cassettes.base_vcr_cassette import BaseVcrCassette

from vcr.cassette import Cassette
import vcr as vcrpy

vcr = vcrpy.VCR()


class VcrpyCassette(BaseVcrCassette):
    def __init__(self, cassette_path: str):
        config = vcr.get_merged_config()
        config.pop("path_transformer")
        config.pop("func_path_generator")

        self.vcrpy_cassette = Cassette.load(path=cassette_path, **config)
        self._host = None

        for request in self.vcrpy_cassette.requests:
            parsed_url = urlparse(request.uri)
            current_interaction_request_host = (
                f"{parsed_url.scheme}://{parsed_url.netloc}"
            )

            if current_interaction_request_host != self._host and self._host != None:
                raise Exception("More than one host found in cassette interactions")

            if self._host == None:
                self._host = current_interaction_request_host

    def response_for(self, method: str, path: str, body: str, headers: list):
        headers = vcrpy.request.HeadersDict(headers)
        request = vcrpy.request.Request(method, f"{self._host}{path}", body, headers)

        encoded_response = self.vcrpy_cassette.responses_of(request)[0]
        return vcrpy.filters.decode_response(encoded_response)
