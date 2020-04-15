# -*- coding: utf-8 -*-

# DO NOT EDIT THIS FILE!
# This file has been autogenerated by dephell <3
# https://github.com/dephell/dephell

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

readme = ''

setup(
    long_description=readme,
    name='vcr-stub-server',
    version='0.1.0',
    description='Standalone stub server for replaying VCR cassettes',
    python_requires='==3.*,>=3.6.0',
    author='Simon Nizov',
    author_email='simon.nizov@gmail.com',
    packages=['vcr_stub_server', 'vcr_stub_server.cassettes'],
    package_dir={"": "."},
    package_data={},
    install_requires=['vcrpy==4.*,>=4.0.2'],
    extras_require={
        "dev": [
            "black==19.*,>=19.10.0", "ipdb==0.*,>=0.13.2", "pytest==pytest-cov",
            "pytest-cov==2.*,>=2.8.1", "requests==2.*,>=2.23.0"
        ]
    },
    scripts=["vcr_stub_server/__main__.py"],
    entry_points = {
        'console_scripts': ['vcr-stub-server=vcr_stub_server.__main__:main'],
    }
)