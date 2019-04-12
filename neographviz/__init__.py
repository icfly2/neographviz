import py2neo

version = py2neo.__version__[0]
if int(version) == 4:
    from .vis import *  # as graphviz
elif int(version) == 3:
    from .vis_old import *  # vis_old as graphviz
elif int(version) < 3:
    raise NotImplementedError(f"Not defined for py2neo version {version} ")
