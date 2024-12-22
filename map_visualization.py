import networkx as nx
import matplotlib.pyplot as plt
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def visualize_map(location_service):
    G = nx.Graph()
    for node in location_service.graph.nodes:
        G.add_node(node)
    for start, neighbors in location_service.graph.nodes.items():
        for end, distance in neighbors.items():
            G.add_edge(start, end, weight=distance)

    pos = nx.spring_layout(G)
    plt.figure(figsize=(10, 8))
    plt.gca().set_facecolor('black')

    nx.draw(
        G, pos,
        with_labels=True,
        node_color='lightgrey',
        edge_color='red',
        font_color='white',
        node_size=2000,
        font_size=10
    )

    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_color='white')

    plt.title("Islamabad Ride-Hailing Map", color='white', fontsize=14)
    plt.show()

def visualize_ride_path(location_service, start, end):
    distance, path = location_service.graph.get_shortest_path(start, end)
    if path:
        G = nx.Graph()
        for node in location_service.graph.nodes:
            G.add_node(node)
        for start_node, neighbors in location_service.graph.nodes.items():
            for end_node, distance in neighbors.items():
                G.add_edge(start_node, end_node, weight=distance)

        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, font_size=10)

        path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2)

        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

        plt.title(f"Ride Path from {start} to {end} (Distance: {distance})")
        plt.show()
    else:
        print("No path found between the selected locations.")
