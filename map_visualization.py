import networkx as nx
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# Updated dictionary of locations with unique coordinates
LOCATIONS = {
    'F-6 Markaz': (0, 0),
    'F-7 Markaz': (2, 1),
    'G-9 Markaz': (-2, 3.5),
    'I-8 Markaz': (-3, 5),
    'E-11 Markaz': (-3, -2),
    'F-10 Markaz': (1, 3),
    'G-11 Markaz': (-1, 4),
    'F-17': (5, 7),
    'E-11': (-3, -3),
    'G-10': (0, 4),
    'D-12': (-5, -1),
    'F-11': (2, 4),
    'G-6': (-1, 1),
    'IIUI': (-6, 6),
    'Air University': (3, 5),
    'FAST University': (1, 2),
    'COMSATS': (4, 3),
    'NUST': (-2, 6),
    'Faisal Mosque': (0, 6),
    'Shakarparian': (3, -1),
    'Pakistan Monument': (2, -2),
    'Daman-e-Koh': (1, 6),
    'Centaurus Mall': (2, 0),
    'Serena Hotel': (1, 1),
    # Added Hospitals (unique locations)
    'PIMS Hospital': (-1, 2.7),
    'Shifa Hospital': (-3, 6.5),
    'Ali Medical Hospital': (3.5, 2),
    # Added Fire Stations (unique locations)
    'Fire Station F-7': (2.5, 0.5),
    'Fire Station G-9': (-2.5, 2.5),
    'Fire Station I-8': (-4.5, 4.5)
}

# Updated distances with multiple connections for hospitals and fire stations
DISTANCES = {
    ('F-6 Markaz', 'F-7 Markaz'): 3,
    ('F-7 Markaz', 'F-10 Markaz'): 4,
    ('F-10 Markaz', 'F-11'): 2,
    ('G-9 Markaz', 'G-10'): 2,
    ('G-10', 'G-11 Markaz'): 3,
    ('E-11 Markaz', 'E-11'): 1,
    ('I-8 Markaz', 'G-9 Markaz'): 5,
    ('F-7 Markaz', 'FAST University'): 3,
    ('G-11 Markaz', 'NUST'): 4,
    ('F-10 Markaz', 'Air University'): 4,
    ('G-9 Markaz', 'COMSATS'): 6,
    ('E-11', 'IIUI'): 8,
    ('F-7 Markaz', 'Centaurus Mall'): 2,
    ('F-6 Markaz', 'Serena Hotel'): 2,
    ('G-10', 'Faisal Mosque'): 3,
    ('F-11', 'Daman-e-Koh'): 4,
    ('F-7 Markaz', 'Pakistan Monument'): 4,
    ('F-6 Markaz', 'Shakarparian'): 5,
    ('G-6', 'F-6 Markaz'): 2,
    ('G-6', 'G-9 Markaz'): 4,
    ('F-10 Markaz', 'G-10'): 2,
    ('F-11', 'E-11'): 5,
    ('D-12', 'E-11'): 3,
    ('F-17', 'Air University'): 4,
    # Connections for hospitals
    ('PIMS Hospital', 'G-9 Markaz'): 2,
    ('PIMS Hospital', 'G-10'): 2,
    ('PIMS Hospital', 'Faisal Mosque'): 3,
    ('Shifa Hospital', 'NUST'): 3,
    ('Shifa Hospital', 'G-11 Markaz'): 2,
    ('Shifa Hospital', 'I-8 Markaz'): 6,
    ('Ali Medical Hospital', 'FAST University'): 2,
    ('Ali Medical Hospital', 'Air University'): 2,
    ('Ali Medical Hospital', 'COMSATS'): 3,
    # Connections for fire stations
    ('Fire Station F-7', 'F-7 Markaz'): 1,
    ('Fire Station F-7', 'Centaurus Mall'): 2,
    ('Fire Station F-7', 'Pakistan Monument'): 3,
    ('Fire Station G-9', 'G-9 Markaz'): 1,
    ('Fire Station G-9', 'G-10'): 2,
    ('Fire Station G-9', 'G-6'): 2,
    ('Fire Station I-8', 'I-8 Markaz'): 1,
    ('Fire Station I-8', 'Shifa Hospital'): 2,
    ('Fire Station I-8', 'G-9 Markaz'): 5
}



# Then modify the visualize_map function in map_visualization.py
'''def visualize_map(location_service):
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
    plt.show()'''

'''def visualize_map(location_service):
    """
    Visualizes the map using a grid layout based on location coordinates.
    """
    G = nx.Graph()

    # Add nodes with coordinates
    locations = location_service.map_data.get_all_locations()
    coordinates = location_service.map_data.locations
    for location in locations:
        G.add_node(location, pos=coordinates[location])

    # Add edges with weights from DISTANCES dictionary
    distances = location_service.map_data.get_distances()
    for (start, end), distance in distances.items():
        G.add_edge(start, end, weight=distance)

    # Extract positions for visualization
    pos = nx.get_node_attributes(G, 'pos')

    # Visualization
    plt.figure(figsize=(12, 12))
    plt.gca().set_facecolor('white')

    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_color='skyblue', node_size=1200)

    # Draw edges
    nx.draw_networkx_edges(G, pos, edge_color='gray', width=2)

    # Draw node labels
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')

    # Draw edge labels (distances)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

    plt.title("Islamabad City Map - Grid Layout", fontsize=16, pad=20)
    plt.show()'''

'''def visualize_map(location_service):
    """
    Visualizes the map with nodes placed on a grid where x and y intersect.
    Distances are scaled for better separation, and edges follow the grid lines.
    """
    G = nx.Graph()

    # Add nodes with positions based on their coordinates
    locations = location_service.map_data.get_all_locations()
    coordinates = location_service.map_data.locations

    # Scaling factor to visually separate nodes
    scale = 100  # Adjust this as needed for better visualization

    for location, (x, y) in coordinates.items():
        G.add_node(location, pos=(x * scale, y * scale))

    # Add edges with weights
    distances = location_service.map_data.get_distances()
    for (start, end), distance in distances.items():
        G.add_edge(start, end, weight=distance)

    # Extract positions for visualization
    pos = nx.get_node_attributes(G, 'pos')

    # Adjust edge positions to follow the grid
    def snap_to_grid(x, y, grid_size=scale):
        """Snap coordinates to the nearest grid line."""
        return (round(x / grid_size) * grid_size, round(y / grid_size) * grid_size)

    # Visualization
    plt.figure(figsize=(12, 12))
    plt.gca().set_facecolor('white')

    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_color='skyblue', node_size=800)

    # Draw edges
    edge_positions = []
    for start, end in G.edges():
        x_start, y_start = pos[start]
        x_end, y_end = pos[end]
        edge_positions.append(((x_start, y_start), (x_end, y_end)))

    # Snap edge positions to grid
    edge_positions = [(snap_to_grid(x1, y1), snap_to_grid(x2, y2)) for (x1, y1), (x2, y2) in edge_positions]

    # Draw edges with adjusted positions
    for (x1, y1), (x2, y2) in edge_positions:
        plt.plot([x1, x2], [y1, y2], color='gray', linewidth=2)

    # Draw node labels
    nx.draw_networkx_labels(G, pos, font_size=8, font_weight='bold')

    # Draw edge labels (distances)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=6)

    # Add grid lines for better visualization
    x_min = min(x for x, y in coordinates.values()) * scale - scale
    x_max = max(x for x, y in coordinates.values()) * scale + scale
    y_min = min(y for x, y in coordinates.values()) * scale - scale
    y_max = max(y for x, y in coordinates.values()) * scale + scale

    for i in range(int(x_min), int(x_max) + scale, scale):
        plt.axvline(i, color='lightgray', linewidth=0.5, zorder=0)
    for i in range(int(y_min), int(y_max) + scale, scale):
        plt.axhline(i, color='lightgray', linewidth=0.5, zorder=0)

    plt.xticks(range(int(x_min), int(x_max) + scale, scale), [])
    plt.yticks(range(int(y_min), int(y_max) + scale, scale), [])
    plt.title("Islamabad City Map - Grid Intersection Layout", fontsize=16, pad=20)
    plt.gca().invert_yaxis()  # Optional: Invert y-axis for better alignment
    plt.show()'''




'''def visualize_map(location_service, scale=100):
    G = nx.Graph()

    # Scale up coordinates for better spacing
    for location, (x, y) in location_service.map_data.locations.items():
        G.add_node(location)
        G.nodes[location]['pos'] = (x * scale, y * scale)

    pos = nx.get_node_attributes(G, 'pos')

    if not pos:
        print("No locations to visualize.")
        return

    plt.figure(figsize=(20, 20))  # Increase figure size
    plt.gca().set_facecolor('white')

    # Grid lines for visual reference
    x_coords = [x for x, y in pos.values()]
    y_coords = [y for x, y in pos.values()]
    x_min, x_max = min(x_coords) - scale, max(x_coords) + scale
    y_min, y_max = min(y_coords) - scale, max(y_coords) + scale

    for x in range(int(x_min), int(x_max) + scale, scale):
        plt.axvline(x, color='lightgray', linewidth=0.5, zorder=0)
    for y in range(int(y_min), int(y_max) + scale, scale):
        plt.axhline(y, color='lightgray', linewidth=0.5, zorder=0)

    # Draw orthogonal edges
    for (start, end) in location_service.map_data.get_distances().keys():
        start_pos = pos[start]
        end_pos = pos[end]
        mid_point = (end_pos[0], start_pos[1])

        plt.plot([start_pos[0], mid_point[0]], [start_pos[1], mid_point[1]], 'gray', linewidth=2)
        plt.plot([mid_point[0], end_pos[0]], [mid_point[1], end_pos[1]], 'gray', linewidth=2)

    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=900, alpha=0.8)
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')

    plt.title("Islamabad City Map - Expanded Layout", fontsize=18)
    plt.axis('equal')
    plt.show()'''

'''def visualize_map(location_service, scale=100):
    locations = location_service.map_data.locations
    distances = location_service.map_data.get_distances()

    # Scale up coordinates for better spacing
    scaled_locations = {loc: (x * scale, y * scale) for loc, (x, y) in locations.items()}

    plt.figure(figsize=(12, 12))  # Set figure size

    # Plot nodes
    for loc, (x, y) in scaled_locations.items():
        plt.scatter(x, y, label=loc, s=200, alpha=0.5)
        plt.text(x + 0.3, y + 0.3, loc, fontsize=8)  # Label nodes

    # Plot edges with distances
    for (loc1, loc2), dist in distances.items():
        x1, y1 = scaled_locations[loc1]
        x2, y2 = scaled_locations[loc2]
        plt.plot([x1, x2], [y1, y2], 'k-', linewidth=1.5)  # Draw edge
        plt.text((x1 + x2) / 2, (y1 + y2) / 2, f'{dist}', fontsize=8, color='blue')  # Label edge

    plt.title('Map of Locations and Connections', fontsize=16)
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.grid(True)
    plt.legend()
    plt.show()

    import plotly.graph_objects as go'''

import plotly.graph_objects as go

'''def visualize_map(location_service, scale=100):
    # Scale up coordinates for better spacing
    locations = location_service.map_data.locations
    distances = location_service.map_data.get_distances()
    scaled_locations = {loc: (x * scale, y * scale) for loc, (x, y) in locations.items()}

    # Create figure
    fig = go.Figure()

    # Add edges to the figure
    for (loc1, loc2), dist in distances.items():
        x1, y1 = scaled_locations[loc1]
        x2, y2 = scaled_locations[loc2]
        fig.add_trace(go.Scatter(
            x=[x1, x2],
            y=[y1, y2],
            mode='lines',
            line=dict(width=1.5, color='gray'),
            hoverinfo='none'
        ))

    # Add nodes to the figure
    node_x = []
    node_y = []
    node_text = []

    for loc, (x, y) in scaled_locations.items():
        node_x.append(x)
        node_y.append(y)
        node_text.append(loc)

    fig.add_trace(go.Scatter(
        x=node_x,
        y=node_y,
        mode='markers+text',
        text=node_text,
        textposition='top center',
        marker=dict(size=10, color='blue', opacity=0.8),
        hoverinfo='text'
    ))

    # Layout adjustments
    fig.update_layout(
        title='Interactive Map of Locations and Connections',
        xaxis=dict(title='X Coordinate', showgrid=True, zeroline=False),
        yaxis=dict(title='Y Coordinate', showgrid=True, zeroline=False),
        showlegend=False,
        autosize=True,  # Automatically adjust to the browser window
        plot_bgcolor='white',
        margin=dict(l=0, r=0, t=30, b=0)  # Minimize margins for full-screen effect
    )

    fig.show()'''



def visualize_map(self, highlight_path=None):
    """
    Visualize the map with locations, distances, and optionally highlight a path.
    """
    plt.figure(figsize=(12, 12))

    for loc, (x, y) in LOCATIONS.items():
        # Differentiate types of locations
        if 'Hospital' in loc:
            plt.scatter(x, y, color='red', label='Hospital' if 'Hospital' not in plt.gca().get_legend_handles_labels()[1] else "", s=200, alpha=0.7)
        elif 'Fire Station' in loc:
            plt.scatter(x, y, color='orange', label='Fire Station' if 'Fire Station' not in plt.gca().get_legend_handles_labels()[1] else "", s=200, alpha=0.7)
        else:
            plt.scatter(x, y, color='blue', label='Location' if 'Location' not in plt.gca().get_legend_handles_labels()[1] else "", s=200, alpha=0.5)
        plt.text(x + 0.3, y + 0.3, loc, fontsize=8)

    for (loc1, loc2), dist in DISTANCES.items():
        x1, y1 = LOCATIONS[loc1]
        x2, y2 = LOCATIONS[loc2]
        plt.plot([x1, x2], [y1, y2], 'k-', linewidth=1.5)
        plt.text((x1 + x2) / 2, (y1 + y2) / 2, f'{dist}', fontsize=8, color='blue')
    if highlight_path:
        path_edges = list(zip(highlight_path[:-1], highlight_path[1:]))
        for loc1, loc2 in path_edges:
            x1, y1 = LOCATIONS[loc1]
            x2, y2 = LOCATIONS[loc2]
            plt.plot([x1, x2], [y1, y2], 'r-', linewidth=2)  # Highlight path in red

    plt.title('Map of Locations, Hospitals, and Fire Stations')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.grid(True)
    plt.legend()
    plt.show()



'''def visualize_ride_path(self, start, end):
    """
    Visualize the shortest path between two locations on the map.
    
    Args:
        start (str): Starting location name
        end (str): Ending location name
    """
    if not self.graph:
        print("Error: Graph not initialized")
        return
        
    # Get the shortest path
    path = self.graph.get_shortest_path(start, end)
    if not path:
        print(f"No path found between {start} and {end}")
        return
        
    # Create a new networkx graph for visualization
    G = nx.Graph()
    
    # Add all nodes and edges
    for node in self.graph.nodes:
        G.add_node(node)
    for node in self.graph.nodes:
        for neighbor, weight in self.graph.nodes[node].items():
            G.add_edge(node, neighbor, weight=weight)
    
    # Draw the graph
    pos = nx.spring_layout(G)
    plt.figure(figsize=(12, 8))
    
    # Draw all edges in light gray
    nx.draw_networkx_edges(G, pos, edge_color='lightgray', width=1)
    
    # Draw all nodes in light blue
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=500)
    
    # Highlight the path
    path_edges = list(zip(path[:-1], path[1:]))
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='r', width=2)
    
    # Highlight start and end nodes
    nx.draw_networkx_nodes(G, pos, nodelist=[start], node_color='g', node_size=500)
    nx.draw_networkx_nodes(G, pos, nodelist=[end], node_color='r', node_size=500)
    
    # Add labels
    nx.draw_networkx_labels(G, pos)
    
    plt.title(f"Shortest Path from {start} to {end}")
    plt.axis('off')
    plt.show()'''