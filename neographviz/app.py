import sys

from flask import Flask

from neographviz import Graph, plot

app = Flask(__name__)


@app.route("/")
def index():
    "Main graph page"
    out = plot(graph, template_file="vis.html", app=True)
    return out


if __name__ == "__main__":
    options = sys.argv
    if len(options)==1:
        graph_host, debug = '', True
    elif len(options)==2:
        graph_host, debug = options[1], True
    elif len(options)==3:
        _, graph_host, debug = options
    graph = Graph(graph_host)
    if bool(debug):
        app.run(debug=True, port=5000)
    else:
        import waitress
        waitress.serve(app, host="0.0.0.0", port=5000)
