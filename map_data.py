import networkx as nx
from data_structures import Graph
from save_load import save_data_to_file, load_data_from_file


# Dictionary of locations with their coordinates (x, y)
'''LOCATIONS = {
    # Sectors
    'F-6 Markaz': (0, 0),
    'F-7 Markaz': (2, 1),
    'G-9 Markaz': (-2, 3),
    'I-8 Markaz': (-4, 5),
    'E-11 Markaz': (-3, -2),
    'F-10 Markaz': (1, 3),
    'G-11 Markaz': (-1, 4),
    'F-17': (5, 7),
    'E-11': (-3, -3),
    'G-10': (0, 4),
    'D-12': (-5, -1),
    'F-11': (2, 4),
    'G-6': (-1, 1),

    # Universities
    'IIUI': (-6, 6),
    'Air University': (3, 5),
    'FAST University': (1, 2),
    'COMSATS': (4, 3),
    'NUST': (-2, 6),

    # Landmarks
    'Faisal Mosque': (0, 5),
    'Shakarparian': (3, -1),
    'Pakistan Monument': (2, -2),
    'Daman-e-Koh': (1, 6),
    'Centaurus Mall': (2, 0),
    'Serena Hotel': (1, 1)
}'''

'''# Dictionary of locations with their coordinates (x, y)
LOCATIONS = {
    # Sectors
    'F-6 Markaz': (0, 0),
    'F-7 Markaz': (6, 3),
    'G-9 Markaz': (-5, 7),
    'I-8 Markaz': (-10, 13),
    'E-11 Markaz': (-7, -4),
    'F-10 Markaz': (3, 10),
    'G-11 Markaz': (-2, 10),
    'F-17': (10, 18),
    'E-11': (-6, -6),
    'G-10': (0, 10),
    'D-12': (-13, -2),
    'F-11': (5, 10),
    'G-6': (-3, 2),

    # Universities
    'IIUI': (-15, 15),
    'Air University': (7, 13),
    'FAST University': (2, 5),
    'COMSATS': (10, 7),
    'NUST': (-5, 14),

    # Landmarks
    'Faisal Mosque': (0, 13),
    'Shakarparian': (7, -2),
    'Pakistan Monument': (5, -5),
    'Daman-e-Koh': (2, 15),
    'Centaurus Mall': (5, 0),
    'Serena Hotel': (2, 2)
}


# Dictionary of direct distances between connected locations
DISTANCES = {
    # Major connections between sectors
    ('F-6 Markaz', 'F-7 Markaz'): 3,
    ('F-7 Markaz', 'F-10 Markaz'): 4,
    ('F-10 Markaz', 'F-11'): 2,
    ('G-9 Markaz', 'G-10'): 2,
    ('G-10', 'G-11 Markaz'): 3,
    ('E-11 Markaz', 'E-11'): 1,
    ('I-8 Markaz', 'G-9 Markaz'): 5,

    # Connections to universities
    ('F-7 Markaz', 'FAST University'): 3,
    ('G-11 Markaz', 'NUST'): 4,
    ('F-10 Markaz', 'Air University'): 4,
    ('G-9 Markaz', 'COMSATS'): 6,
    ('E-11', 'IIUI'): 8,

    # Connections to landmarks
    ('F-7 Markaz', 'Centaurus Mall'): 2,
    ('F-6 Markaz', 'Serena Hotel'): 2,
    ('G-10', 'Faisal Mosque'): 3,
    ('F-11', 'Daman-e-Koh'): 4,
    ('F-7 Markaz', 'Pakistan Monument'): 4,
    ('F-6 Markaz', 'Shakarparian'): 5,

    # Additional strategic connections
    ('G-6', 'F-6 Markaz'): 2,
    ('G-6', 'G-9 Markaz'): 4,
    ('F-10 Markaz', 'G-10'): 2,
    ('F-11', 'E-11'): 5,
    ('D-12', 'E-11'): 3,
    ('F-17', 'Air University'): 4
}

# Dynamically calculate scaling factor to fit within bounds
def calculate_scaling_factor(locations, target_range=10):
    x_vals = [x for x, y in locations.values()]
    y_vals = [y for x, y in locations.values()]
    x_range = max(x_vals) - min(x_vals)
    y_range = max(y_vals) - min(y_vals)
    max_range = max(x_range, y_range)
    return target_range / max_range if max_range != 0 else 1

SCALING_FACTOR = calculate_scaling_factor(LOCATIONS, target_range=10)

# Scale locations
def scale_locations(locations, factor):
    return {loc: (x * factor, y * factor) for loc, (x, y) in locations.items()}

LOCATIONS = scale_locations(LOCATIONS, SCALING_FACTOR)'''
import matplotlib.pyplot as plt
import numpy as np


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

# Dynamically calculate scaling factor to fit within bounds
def calculate_scaling_factor(locations, target_range=10, min_spacing=2):
    x_vals = [x for x, y in locations.values()]
    y_vals = [y for x, y in locations.values()]
    x_range = max(x_vals) - min(x_vals)
    y_range = max(y_vals) - min(y_vals)
    max_range = max(x_range, y_range)
    
    # Apply non-linear scaling for more separation
    scaling_factor = target_range / max_range if max_range != 0 else 1
    return scaling_factor + min_spacing / max_range

SCALING_FACTOR = calculate_scaling_factor(LOCATIONS, target_range=10)

# Scale locations
def scale_locations(locations, factor):
    return {loc: (x * factor, y * factor) for loc, (x, y) in locations.items()}

LOCATIONS = scale_locations(LOCATIONS, SCALING_FACTOR)

# Plot the map
'''def plot_map(locations, distances):
    plt.figure(figsize=(12, 12))

    for loc, (x, y) in locations.items():
        # Differentiate types of locations
        if 'Hospital' in loc:
            plt.scatter(x, y, color='red', label='Hospital' if 'Hospital' not in plt.gca().get_legend_handles_labels()[1] else "", s=200, alpha=0.7)
        elif 'Fire Station' in loc:
            plt.scatter(x, y, color='orange', label='Fire Station' if 'Fire Station' not in plt.gca().get_legend_handles_labels()[1] else "", s=200, alpha=0.7)
        else:
            plt.scatter(x, y, color='blue', label='Location' if 'Location' not in plt.gca().get_legend_handles_labels()[1] else "", s=200, alpha=0.5)
        plt.text(x + 0.3, y + 0.3, loc, fontsize=8)

    for (loc1, loc2), dist in distances.items():
        x1, y1 = locations[loc1]
        x2, y2 = locations[loc2]
        plt.plot([x1, x2], [y1, y2], 'k-', linewidth=1.5)
        plt.text((x1 + x2) / 2, (y1 + y2) / 2, f'{dist}', fontsize=8, color='blue')

    plt.title('Map of Locations, Hospitals, and Fire Stations')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.grid(True)
    plt.legend()
    plt.show()

plot_map(LOCATIONS, DISTANCES)'''

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


class IslamabadMap:
    def __init__(self, file_path='map_data.json'):
        self.file_path = file_path
        self.graph = load_data_from_file(self.file_path, Graph) or self._initialize_map()
        self.locations = LOCATIONS  # Dictionary of locations and their coordinates
        self.distances = DISTANCES  # Dictionary of distances between locations
        self.visualize_map = visualize_map

    def _initialize_map(self):
        """Initialize the map graph with locations and distances."""
        graph = Graph()
        for location in LOCATIONS:
            graph.add_node(location)
        for (start, end), distance in DISTANCES.items():
            graph.add_edge(start, end, distance)
            graph.add_edge(end, start, distance)  # Add reverse direction
        #save_data_to_file(self.file_path, graph)
        return graph

    def get_location_coordinates(self, location):
        """Get the coordinates of a specific location."""
        return LOCATIONS.get(location)

    def get_direct_distance(self, start, end):
        """Get the direct distance between two locations if they're directly connected."""
        return DISTANCES.get((start, end)) or DISTANCES.get((end, start))

    def get_shortest_path(self, start, end):
            """Delegate shortest path calculation to the graph."""
            return self.graph.get_shortest_path(start, end)


    def get_nearby_locations(self, location, max_distance):
        """Get all locations within a specified distance of a given location."""
        if location not in LOCATIONS:
            return []
        distances, _ = self.graph.dijkstra(location)
        return [loc for loc, dist in distances.items() if 0 < dist <= max_distance]

    def get_all_locations(self):
        """Return a list of all locations in the map."""
        return list(LOCATIONS.keys())

    def get_location_type(self, location):
        """Return the type of location (Sector, University, or Landmark)."""
        if location not in LOCATIONS:
            return None
        if 'University' in location or 'NUST' in location or 'IIUI' in location or 'COMSATS' in location:
            return 'University'
        if any(sector in location for sector in ['F-', 'G-', 'I-', 'E-', 'D-']):
            return 'Sector'
        return 'Landmark'

    def get_distances(self):
        """Return all distances between connected locations."""
        return self.distances

    def visualize_ride_path(self, start, end):
        """
        Visualize the shortest path between two locations on the map.
        """
        print(f"Debug - Visualization starting with: start={start}, end={end}")

        # First ensure we have a graph
        if not hasattr(self, 'graph') or not self.graph.nodes:
            print("Debug: Graph not initialized or empty, initializing now...")
            self.graph = self._initialize_map()  # Assuming this is your initialization method

        # Verify nodes exist in graph
        if start not in self.graph.nodes:
            print(f"Debug: Start node '{start}' not found in graph nodes: {list(self.graph.nodes)}")
            return
        if end not in self.graph.nodes:
            print(f"Debug: End node '{end}' not found in graph nodes: {list(self.graph.nodes)}")
            return

        # Get the shortest path
        path = self.graph.get_shortest_path(start, end)
        if not path:
            print(f"No path found between {start} and {end}")
            return

        # Debugging: Print the path
        print(f"Debug - Shortest path found: {path}")

        # Reuse the visualize_map function with path highlighting
        visualize_map(self, highlight_path=path)


# Helper functions for the map
def is_valid_location(location):
    """Check if a location exists in the map."""
    return location in LOCATIONS

def get_distance_matrix():
    """Generate a complete distance matrix between all locations."""
    map_instance = IslamabadMap()
    locations = list(LOCATIONS.keys())
    matrix = {}

    for start in locations:
        matrix[start] = {}
        distances, _ = map_instance.graph.dijkstra(start)
        for end in locations:
            matrix[start][end] = distances.get(end, float('inf'))

    return matrix

