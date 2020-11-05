import json
import os
import uuid
from tempfile import NamedTemporaryFile
from typing import List

import pkg_resources
import py2neo
from IPython.display import HTML, IFrame, Image, display_html
from jinja2 import Environment, FileSystemLoader


def plot(
    graph: py2neo.Graph, query: str = "match p=()--()--() return p limit 25", **kwargs
) -> IFrame:
    """Plot a graph, using a query.

    Heavy lifting is done via py2neo `to_subgraph` and `neographviz.vis_network`

    Example:
        >>> from neographviz import plot, Graph
        >>> graph = Graph() # You need a graph at localhos, or pass the uri here.
        >>> plot(graph)

    Args:
        graph (py2neo.Graph): Graph object from py2neo
        query (str, optional): Any valid cypher query, must return a path p, should use a limit. Defaults to "match p=()--()--() return p limit 25".

    Returns:
        IFrame: IFrame to show in jupyter notebook or website.
    """
    sg = graph.run(query).to_subgraph()
    return vis_network(_get_nodes(sg), _get_edges(sg), **kwargs)


def _get_nodes(sg: py2neo.Subgraph) -> List[dict]:
    """Get nodes from a subgraph
    
    Get the nodes in a subgraph and add the data so that
    visjs can consume it. 

    Arguments:
        sg {py2neo.Subgraph} -- 
    
    Returns:
        List -- List of dictionaries with keys: id, group, label, title
    """
    nodes = []
    if sg:
        for n in sg.nodes:
            nodes.append(
                {
                    "id": n.identity,
                    "group": n.labels.__str__()[1:],
                    "label": " ".join([f"{v}" for v in n.values()]),
                    "title": "<br> ".join([f"{k}:{v}" for k, v in n.items()]),
                }
            )
    return nodes


def _get_edges(sg: py2neo.Subgraph) -> List:
    edges = []
    if sg:
        for r in sg.relationships:
            d = {
                "from": r.start_node.identity,
                "to": r.end_node.identity,
                "label": next(iter(r.types())),
                "arrows": "to",
            }
            try:
                d["title"] = " <br>".join([str(k) + ":" + str(v) for k, v in r.items()])
            except:
                pass
            edges.append(d)
    return edges


def vis_network(
    nodes,
    edges,
    physics="",
    height=400,
    node_size=25,
    font_size=14,
    filename="",
    config={},
    template_file="vis.html",
    app=False,
):
    """Render a network with vis.js in an IFrame for use in a jupyter notebook or website. 

    This function will render a template whihc uses vis.js to display the graph. 
    The options configured can be passed directly to the template, but as it is vis.js underneith,
    any valid options for it can be passed as js in string form to jsoptions.

    Args:
        nodes (List): List of nodes
        edges (List): List of edges
        physics (str, optional): Defintion of physics in vis.js. Defaults to basic barnesHut.
        height (int, optional): Height of the plot in pixels. Defaults to 400.
        node_size (int, optional): Defaults to 25.
        font_size (int, optional): [description]. Defaults to 14.
        filename (str, optional): Optional filenmae for storing the page. Defaults to a `''` and uses a uuid.
        config (dict, optional): Custom kwargs to pass to template. Defaults to `{}`.
        template_file (str, optional): Defaults to `vis.html` the provided template, provide your own.

    Returns:
        IFrame: Iframe to show in jupyter notebook
    """
    template = pkg_resources.resource_filename("neographviz", "templates/")
    env = Environment(loader=FileSystemLoader(template))
    template = env.get_template(template_file)
    if not physics:
        physics = """{
            "barnesHut": {
            "centralGravity": 0,
            "springLength": 240
            }
        }"""

    if not app:
        html = template.render(
            nodes=nodes,
            edges=edges,
            physics=physics,
            node_size=node_size,
            font_size=font_size,
        )
        unique_id = str(uuid.uuid4())
        if not filename:
            filename = "figure/graph-{}.html".format(unique_id)
        try:
            with open(filename, "w") as file:
                file.write(html)
        except FileNotFoundError:
            os.mkdir("figure")
            with open(filename, "w") as file:
                file.write(html)

        return IFrame(filename, width="100%", height=str(height))
    else:
        return template.render(
            nodes=nodes,
            edges=edges,
            physics=physics,
            node_size=node_size,
            font_size=font_size,
            app=app
        )


def get_vis_info(node, id, options):
    node_label = list(node.labels)[0]
    title = "".join([f"{k}:{v} " for k, v in node.items()]).strip()
    if node_label in options:
        vis_label = node.get(options.get(node_label, ""), "")
    else:
        vis_label = title

    return {"id": id, "label": vis_label, "group": node_label, "title": title}
