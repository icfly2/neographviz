
import setuptools
from distutils.core import setup

with open("README.md", 'r') as f:
    long_description = f.read()
setup(
    name='neographviz',
    version='0.2.6',
    description='Graph display package for py2neo graphs forked from https://github.com/nicolewhite/neo4j-jupyter',
    long_description = long_description,
    long_description_content_type="text/markdown",
    author= 'Ruben Menke',
    author_email='ruben.m.menke@gmail.com',
    url='https://github.com/icfly2/neo4j-jupyter',
    packages=['neographviz'],
    # package_data= ['lib'],
    package_data={'neographviz': ['templates/*.html']},
    install_requires = ['py2neo', 'IPython', 'jinja2', 'pyjokes']
)