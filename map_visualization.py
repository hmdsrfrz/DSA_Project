import networkx as nx
import matplotlib.pyplot as plt


# Then modify the visualize_map function in map_visualization.py
def visualize_map(location_service):
    """
    Visualizes the map using the graph data from the location service.
    """
    G = nx.Graph()

    # Add nodes
    locations = location_service.map_data.get_all_locations()
    for location in locations:
        G.add_node(location)

    # Add edges with weights from DISTANCES dictionary
    distances = location_service.map_data.get_distances()
    for (start, end), distance in distances.items():
        G.add_edge(start, end, weight=distance)

    # Visualization
    pos = nx.spring_layout(G)
    plt.figure(figsize=(12, 8))
    plt.gca().set_facecolor('black')

    nx.draw(
        G, pos,
        with_labels=True,
        node_color='lightgrey',
        edge_color='red',
        font_color='white',
        node_size=2000,
        font_size=8,
        font_weight='bold'
    )

    # Draw edge labels
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='white')

    plt.title("Islamabad Ride-Hailing Map", color='white', fontsize=14, pad=20)
    plt.show()

def visualize_ride_path(location_service, start, end):
    distance, path = location_service.get_shortest_path(start, end)
    if path:
        G = nx.Graph()
        for location in location_service.map_data.get_all_locations():
            G.add_node(location)

        for (start_node, end_node), dist in location_service.map_data.get_distances().items():
            G.add_edge(start_node, end_node, weight=dist)

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
