from urllib.parse import urlparse
from vcr.cassette import Cassette

class LoadedCassette:
    __vcr_cassette = None
    __cassette_host = None
   
    def __init__(self, cassette_path):
        LoadedCassette.__vcr_cassette = Cassette.load(path=cassette_path)
        LoadedCassette.__cassette_host = None

        for request in LoadedCassette.__vcr_cassette.requests:
            parsed_url = urlparse(request.uri)
            current_interaction_request_host = f"{parsed_url.scheme}://{parsed_url.netloc}"

            if current_interaction_request_host != LoadedCassette.__cassette_host and LoadedCassette.__cassette_host != None:
                raise Exception("More than one host found in cassette interactions")
            if LoadedCassette.__cassette_host == None:
                LoadedCassette.__cassette_host = current_interaction_request_host

    @staticmethod 
    def vcr_cassette():
        return LoadedCassette.__vcr_cassette

    @staticmethod 
    def cassette_host():
        return LoadedCassette.__cassette_host