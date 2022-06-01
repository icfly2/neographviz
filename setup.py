import setuptools
from distutils.core import setup
from neographviz.__init__ import __version__

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="neographviz",
    version=__version__,
    description="Graph display package for py2neo graphs forked from https://github.com/nicolewhite/neo4j-jupyter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Ruben Menke",
    author_email="ruben.m.menke@gmail.com",
    url="https://github.com/icfly2/neographviz",
    packages=["neographviz"],
    package_data={"neographviz": ["templates/*.html"]},
    extras_require={"app": ["waitress==2.1.1", "flask>=1.1.1"]},
)
