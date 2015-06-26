from models.graph import Graph
from network_graph import app
import networkx as nx

with app.test_request_context():
    g = Graph()
    g.graph.add_node('Joe')
    g.graph.add_node('Tim')
    g.graph.add_node('Lesley')
    g.graph.add_node('Tony')
    g.graph.add_node('Jack')

    g.graph.add_edge('Joe', 'Lesley', weight=15)
    g.graph.add_edge('Joe', 'Tony', weight=5)
    g.graph.add_edge('Tony', 'Tim', weight=10)
    g.graph.add_edge('Tim', 'Jack', weight=20)
    #print nx.to_numpy_matrix(g.graph)
    #print nx.adjacency_matrix(g.graph).todense()

    nodes = g.graph.nodes()
    header = ''
    for n in nodes:
        header += '\t{}\t'.format(n)
    print header
    for y in nodes:
        line = ''
        for i, x in enumerate(nodes):
            line += '{}\t\t{} '.format(y if i == 0 else '',
                nx.dijkstra_path_length(g.graph, x, y)
            )
        print '{}\n'.format(line)

    g.save()