import flask
from flask import render_template
from network_graph.models.graph import Graph

blueprint = flask.Blueprint('network_table', __name__)


@blueprint.route('/')
def index():
    g = Graph()
    return render_template(
        'network_table/index.html',
        graph=g,
        nodes=g.nodes,
    )
