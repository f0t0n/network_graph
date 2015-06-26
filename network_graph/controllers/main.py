import flask
from flask import request, render_template, redirect, url_for
from network_graph.models.graph import Graph

blueprint = flask.Blueprint('main', __name__)


@blueprint.route('/')
def index():
    from networkx.readwrite import json_graph
    g = Graph()
    return render_template(
        'main/index.html',
        graph=g,
        nodes=g.nodes
    )


@blueprint.route('delete/<node>')
def delete_node(node):
    _delete_node(Graph(), node)
    return redirect(url_for('main.index'))


def _delete_node(g, node):
    if g.graph.has_node(node):
        g.graph.remove_node(node)
        g.save()


def _edit_node(g, node):
    _delete_node(g, node)
    _add_node(g)


def _add_node(g):
    new_node = request.form.get('current_node')
    nodes = request.form.getlist('node')
    weights = request.form.getlist('weight')
    return g.add_node_with_edges(new_node, nodes, weights)


@blueprint.route('edit/<node>', methods=('GET', 'POST'))
def edit_node(node):
    g = Graph()
    if request.method == 'POST':
        _edit_node(g, node)
    return render_template(
        'main/edit.html',
        graph=g,
        nodes=g.nodes,
        node=node,
        paths=g.get_paths_from(node)
    )


@blueprint.route('add/', methods=('GET', 'POST'))
def add_node():
    g = Graph()
    node = ''
    error = ''
    if request.method == 'POST':
        new_node = request.form.get('current_node')
        nodes = request.form.getlist('node')
        weights = request.form.getlist('weight')
        if _add_node(g):
            return redirect(url_for('main.index'))
        error = "Can't create node {}. It already exists.".format(new_node)
    return render_template(
        'main/edit.html',
        graph=g,
        nodes=g.nodes,
        node=node,
        paths=g.get_paths_from(node),
        error=error
    )
