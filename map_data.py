from data_structures import Graph
from save_load import save_data_to_file, load_data_from_file

# Dictionary of locations with their coordinates (x, y)
LOCATIONS = {
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

class IslamabadMap:
    def __init__(self, file_path='map_data.json'):
        self.file_path = file_path
        self.graph = load_data_from_file(self.file_path, Graph) or self._initialize_map()
        self.locations = LOCATIONS  # Dictionary of locations and their coordinates
        self.distances = DISTANCES  # Dictionary of distances between locations

    def _initialize_map(self):
        """Initialize the map graph with locations and distances."""
        graph = Graph()
        for location in LOCATIONS:
            graph.add_node(location)
        for (start, end), distance in DISTANCES.items():
            graph.add_edge(start, end, distance)
            graph.add_edge(end, start, distance)  # Add reverse direction
        save_data_to_file(self.file_path, graph)
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
