# NEOGRAPHVIZ 

A draw function for neo4j graphs, usable as app or in jupyter notebooks.

Derived and forked from [Nicole White's work](https://github.com/nicolewhite/neo4j-jupyter).

## What can it do?
- display graph DB data
- allow you to run cypher queries from your jupyter notebook
- enable deployment of apps with custom graph queries to make the DB accessible to more people.
- save the graph as html page that can be shared and interacted with.
- show your graph as a website as easy as `python -m neographviz.app` or `python -m neographviz.app "bolt://path to graph" `

## Get started
### in Jupyter
`pip install neographviz`, launch an jupyter notebook with:

    from neographviz import Graph, plot
    graph = Graph("bolt://path to you graph")
    plot(graph)

### With flask
To run a basic flask app:

    pip install neographviz[app]
    python -m neographviz.app --host bolt://path to graph

## Further development
- customisation with jsons
- basic automated queries from website
  - modifying data in the DB with add and remove queries
- better examples and docs:
 - deployment as app to docker
 - in jupyter notebooks
 