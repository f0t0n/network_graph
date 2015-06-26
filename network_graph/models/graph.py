import os
import sys
import json
import networkx as nx
from networkx.readwrite import json_graph
from collections import OrderedDict

from network_graph import app


class Graph(object):
    graph_db = app.config.get('GRAPH_DB_PATH')
    JSON_SETTINGS = {
        'pretty': {
            'indent': 4,
            'sort_keys': True
        },
        'compact': {
            'separators': (',', ':')
        }
    }

    def __init__(self,):
        graph_data = self._load_graph_data()
        self.graph = (
            json_graph.node_link_graph(graph_data)
            if graph_data
            else nx.Graph()
        )

    def _load_graph_data(self):
        if not os.path.exists(self.graph_db):
            return None
        with open(self.graph_db, 'r') as fp:
            return json.load(fp)

    def _get_json_serialization_settings(self, pretty=False):
        return self.JSON_SETTINGS['pretty' if pretty else 'compact']

    def _get_path_weight(self, x, y):
        try:
            return nx.dijkstra_path_length(self.graph, x, y)
        except nx.exception.NetworkXNoPath:
            return 0

    def _weight_to_int(self, weight):
        try:
            return int(weight)
        except ValueError:
            return 1

    def _get_path(self, x, y):
        try:
            return nx.dijkstra_path(self.graph, x, y)
        except nx.exception.NetworkXNoPath:
            return []

    def _has_path(self, source, target):
        return nx.has_path(self.graph, source, target)

    @property
    def nodes(self):
        return sorted(self.graph.nodes())

    def save(self, pretty=app.debug):
        with open(self.graph_db, 'w') as fp:
            settings = self._get_json_serialization_settings(pretty=pretty)
            json.dump(json_graph.node_link_data(self.graph), fp, **settings)

    def get_paths_from(self, node):
        other_nodes = self.nodes

        if not self.graph.has_node(node):
            return OrderedDict((n, {}) for n in other_nodes)

        other_nodes.remove(node)

        def dict_item(node, n):
            has_edge = self.graph.has_edge(node, n)
            item_data = {
                'has_edge': has_edge,
                'path': [node, n] if has_edge else self._get_path(node, n),
                'weight': (
                    self.graph.get_edge_data(node, n)['weight']
                    if has_edge
                    else self._get_path_weight(node, n)
                )
            }
            return (n, item_data)
        return OrderedDict(dict_item(node, n) for n in other_nodes)

    def weight_matrix(self):
        nodes = self.nodes
        return [[self._get_path_weight(y, x) for x in nodes] for y in nodes]

    def add_node_with_edges(self, node, nodes, weights):
        if self.graph.has_node(node):
            return None
        self.graph.add_node(node)
        for i, n in enumerate(nodes):
            if self._has_path(node, n):
                continue
            self.graph.add_edge(
                node,
                n,
                weight=self._weight_to_int(weights[i])
            )
        self.save()
        return self
