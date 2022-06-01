from py2neo import Graph
from pytest import fixture
from neographviz import Plot

@fixture
def graph():
    # Public test graph
    user= "recommendations"
    pw="recommendations"
    host="demo.neo4jlabs.com"
    port = 7687
    dbname = "recommendations"
    credentials=(user,pw)
    graph = Graph(auth=credentials, host=host, port=port, name=dbname, scheme="bolt+ssc")# Create the connection, as you would normally with py2neo if you have it on localhost (>=2020.0)
    return graph


def test_nodes_and_edges(graph):
    p = Plot(graph)
    query = "match p= (a)--() where id(a)=0  return p limit 5"
    sg = graph.run(query).to_subgraph()
    nodes = p._get_nodes(sg)
    for n in nodes:
        for key in ['id', 'group', 'label', 'title']:
            assert key in n

    edges = p._get_edges(sg)
    for e in edges:
        for key in ['from', 'to', 'label', 'arrows', 'title']:
            assert key in e

