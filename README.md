# vcr-stub-server

[![pypi-version](https://img.shields.io/pypi/v/vcr-stub-server.svg)](https://pypi.org/project/vcr-stub-server/)
[![python-version](https://img.shields.io/pypi/pyversions/vcr-stub-server)](https://pypi.org/project/vcr-stub-server/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


This is a small tool for setting up a lightweight stub server that replays previously recorded VCR cassettes.

Usually VCR is used internally while running the test suite. In that case, the library is responsible for intercepting HTTP requests. 

But in some cases, it can be useful to be able to spin up a live HTTP server which given a preexisting VCR cassette, would respond to each request with its matching recorded response.

One such case might come when implementing usage of [Pact](http://pact.io), where `vcr-stub-server` can be used to prevent the provider service from making requests to external services during pact verification. This project was inspired by Pact's own [Stub Service](https://github.com/pact-foundation/pact-mock_service#stub-service-usage).

#### Caveats

- Unfortunately, there isn't _one_ standard for cassette YAML files, each VCR implementation does it differently. For example, cassette YAML files created by VCR.py won't be compatible with YAML files created by the Ruby implementation of VCR, etc.

  Therfore **this tool currently only supports [VCR.py](https://github.com/kevin1024/vcrpy)**, using the library's own implementation of parsing the YAML files.
  
- The recorded requests in your YAML cassette file must all be made to the same host.

## Installation

```
$ pip install vcr-stub-server
```

## Usage

Once the package is installed, use the `vcr-stub-server` command to spin up your stub server.

```
$ vcr-stub-server path/to/vcr_cassette.yml
```

## Contributing

Bug reports and pull requests are welcome on GitHub at https://github.com/thatguysimon/vcr-stub-server. This project is intended to be a safe, welcoming space for collaboration, and contributors are expected to adhere to the [Contributor Covenant](https://contributor-covenant.org) code of conduct.

## License

The gem is available as open source under the terms of the [MIT License](https://opensource.org/licenses/MIT).
