import sys
import argparse

from flask import Flask, request

from neographviz import Graph, plot

app = Flask(__name__)


@app.route("/")
def index():
    "Main graph page"
    query = request.args.get('query', 'match p= ()--() return p limit 25')
    out = plot(graph, query=query, template_file="vis.html", app=True)
    return out


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Launch a graph visalisation app.')
    parser.add_argument('--debug', type=bool, default='True',
                    help='Flag for debugging')
    parser.add_argument('--host', default='', type=str,
                    help='Path to the graph DB, defaults to localhost')
    parser.add_argument('--port', default=5000, type=int,
                help='POrt on which to serve the app')
    options = parser.parse_args()
    graph = Graph(options.host)
    if options.debug:
        app.run(debug=True, port=5000)
    else:
        import waitress
        waitress.serve(app, host="0.0.0.0", port=5000)
