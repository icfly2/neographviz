from IPython.display import IFrame
import json
import uuid
import os


def vis_network(
    nodes,
    edges,
    physics=False,
    height=400,
    node_size=25,
    font_size=14,
    filename=None,
    config=False,
    jsoptions=None,
):
    html = """
    <html>
    <head>
      <script type="text/javascript" src="http://visjs.org/dist/vis.js"></script>
      <link href="https://visjs.org/dist/vis.css" rel="stylesheet" type="text/css">

      <!-- <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.min.js"></script> -->
      <!-- <link href="https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.min.css" rel="stylesheet" type="text/css"> -->
    </head>
    <body>

    <div id="{id}"></div>

    <script type="text/javascript">
      var nodes = {nodes};
      var edges = {edges};

      var container = document.getElementById("{id}");

      var data = {{
        nodes: nodes,
        edges: edges
      }};

    {options}

    var network = new vis.Network(container, data, options);


    // assuming that nodes is a vis.DataSet containing the nodes

    network.on('dragEnd', function(params) {{
        if (params.nodeIds.length){{
       //for (var i = 0; i < params.nodeIds.length; i++) {{
           var nodeId = params.nodeIds[0];
           nodes.update( {{ id: nodeId, allowedToMoveX: false, allowedToMoveY: false }});
       }}
    }});
    network.on('dragStart', function(params) {{
       if (params.nodeIds.length){{
       // for (var i = 0; i < params.nodeIds.length; i++) {{
          var nodeId = params.nodeIds[0];
          nodes.update( {{ id: nodeId, allowedToMoveX: true, allowedToMoveY: true }} );
       }}
    }});


    </script>
    </body>
    </html>
    """

    unique_id = str(uuid.uuid4())
    if not jsoptions:
        jsoptions = """
        var options = {{
            nodes: {{
                shape: 'dot',
                size: {node_size},
                font: {{
                    size: {font_size}
                }}
            }},
            edges: {{
                font: {{
                    size: {font_size},
                    align: 'middle'
                }},
                color: 'gray',
                arrows: {{
                    to: {{enabled: true, scaleFactor: 0.5}}
                }},

            }},
            physics: {{
                enabled: {physics},
                "barnesHut": {{
                    "gravitationalConstant": -18400,
                    "damping": 0.36,
                    "avoidOverlap": 0.68
                }},
                "minVelocity": 0.75
            }},
            configure: {{
                    enabled: {config},
                    showButton: true
            }}

        }};
        """.format(
            node_size=node_size,
            font_size=font_size,
            physics=json.dumps(physics),
            config=json.dumps(config),
        )
    # breakpoint()
    html = html.format(
        id=unique_id,
        options=jsoptions,
        nodes=json.dumps(nodes),
        edges=json.dumps(edges),
    )
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


def roundness(from_node, to_node, cache) -> float:
    already = cache.get((from_node, to_node), None)
    if already:
        precomputed = [
            0.6,
            -0.6,
            0.4,
            -0.4,
            0.6,
            -0.6,
            0.8,
            -0.8,
            1,
            -1,
            0.1,
            -0.1,
            0.3,
            -0.3,
            0.5,
            -0.5,
            0.7,
            -0.7,
            0.9,
            -0.9,
        ]
        if len(already) < len(precomputed):
            curve = precomputed[len(already)]
        else:
            curve = 0.15
    else:
        curve = 0
        cache[(from_node, to_node)] = []

    cache[(from_node, to_node)].append(curve)

    return curve, cache


def get_vis_info(node, id, options):
    node_label = list(node.labels)[0]
    title = "".join([f"{k}:{v} " for k, v in node.items()]).strip()
    if node_label in options:
        vis_label = node.get(options.get(node_label, ""), "")
    else:
        vis_label = title

    return {"id": id, "label": vis_label, "group": node_label, "title": title}


def draw(
    graph,
    query="",
    options={},
    physics=False,
    limit=100,
    height=400,
    node_size=25,
    font_size=14,
    filename=None,
    jsoptions=None,
    config=False,
):
    """[summary]
    
    Arguments:
        graph {[type]} -- [description]
    
    Keyword Arguments:
        query {str[CYPHER]} -- query to run on graph to plot, default is just as many random items as defined by limit.
        options {dict} -- Display configuration options (default: {{}})
        physics {bool} -- Weather to have animated physics (default: {False})
        limit {int} -- Number of items to display (default: {100})
        height {int} -- [description] (default: {400})
        node_size {int} -- [description] (default: {25})
        font_size {int} -- [description] (default: {14})
        filename {[type]} -- [description] (default: {None})
        jsoptions {[type]} -- [description] (default: {None})
        config {bool} -- [description] (default: {False})
    
    Returns:
        [type] -- [description]
    """

    # The options argument should be a dictionary of node labels and property keys; it determines which property
    # is displayed for the node label. For example, in the movie graph, options = {"Movie": "title", "Person": "name"}.
    # Omitting a node label from the options dict will leave the node unlabeled in the visualization.
    # Setting physics = True makes the nodes bounce around when you touch them!
    if not query:
        query = f"""
        MATCH (n)
        WITH n, rand() AS random
        ORDER BY random
        LIMIT {limit}
        OPTIONAL MATCH (n)-[r]->(m)
        RETURN n AS source_node,
                id(n) AS source_id,
                r,
                m AS target_node,
                id(m) AS target_id
        """

    data = graph.run(query)
    cache = {}
    nodes = []
    edges = []

    for row in data:
        source_node = row[0]
        source_id = row[1]
        rel = row[2]
        target_node = row[3]
        target_id = row[4]
        source_info = get_vis_info(source_node, source_id, options)

        if source_info not in nodes:
            nodes.append(source_info)

        #  smooth: {type: 'curvedCW', roundness: 0.2}
        if rel is not None:
            target_info = get_vis_info(target_node, target_id, options)

            if target_info not in nodes:
                nodes.append(target_info)

            label = "".join([f"{name} " for name in rel.types()]).strip()
            if len(rel.keys()):
                # we have keys get the details
                try:
                    title = "".join(
                        [f"{key}:{str(rel[key])} " for key in list(rel.keys())]
                    ).strip()
                except:
                    breakpoint()
            else:
                # there is nothing more to it
                title = "".join([f"{name} " for name in rel.types()]).strip()
            # try:
            #     title = "".join([f"{name}:{value} " for name, value in rel.items()]).strip()
            # except:
            rdns, cache = roundness(source_info["id"], target_info["id"], cache)
            edges.append(
                {
                    "from": source_info["id"],
                    "to": target_info["id"],
                    "label": label,
                    "title": title,
                    "smooth": f"{{type: 'curvedCW', roundness: {rdns} }}",
                }
            )

    return vis_network(
        nodes,
        edges,
        physics=physics,
        height=height,
        node_size=node_size,
        font_size=font_size,
        filename=filename,
        jsoptions=jsoptions,
        config=config,
    )
