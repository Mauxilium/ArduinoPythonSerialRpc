"""Setup script for ArduinoPythonSerialRpc"""

import os.path
from setuptools import setup

# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

# The text of the README file
with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

# This call to setup() does all the work
setup(
    name="arduinopythonserialrpc",
    version="1.0.0",
    description="Python side of a serial communication library with Arduino Card",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Mauxilium/ArduinoPythonSerialRpc",
    author="Gabriele Maris",
    author_email="gabriele.maris@mauxilium.it",
    license="Apache2",
    classifiers=[
        "License :: OSI Approved :: Apache2",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["arduinopythonserialrpc"],
    include_package_data=True,
    install_requires=[
        "pyserial", "pytest"
    ]
)