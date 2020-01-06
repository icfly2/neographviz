import py2neo

__version__ = 0.3

if py2neo.__version__[0] >= 4:
    from .vis import plot_query, get_edges, get_nodes, draw  # as graphviz
else:
    raise NotImplementedError("Requires py2neo v4 or (possibly) newer")
