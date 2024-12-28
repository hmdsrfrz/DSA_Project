from data_structures import Graph
from map_data import IslamabadMap
from save_load import save_data_to_file, load_data_from_file

class LocationService:
    def __init__(self, map_data: IslamabadMap, file_path='location_service.json'):
        self.map_data = map_data  
        self.file_path = file_path
        self.graph = load_data_from_file(self.file_path, Graph)
        if not self.graph:
            self.graph = Graph()
            self._initialize_map()
            save_data_to_file(self.file_path, self.graph)

    def _initialize_map(self):
        """
        Initializes the graph with locations and distances from the IslamabadMap instance.
        """
        # Add all locations as nodes
        locations = self.map_data.get_all_locations()
        for location in locations:
            self.graph.add_node(location)

        # Add all distances as edges
        distances = self.map_data.get_distances()  # Use the get_distances method
        for (start, end), distance in distances.items():
            self.graph.add_edge(start, end, distance)
            # Add reverse direction since roads are typically bidirectional
            self.graph.add_edge(end, start, distance)
        
        return self.graph

    def get_shortest_path(self, start, end):
        """Get the shortest path and its distance between two locations."""
        if not self.is_valid_location(start) or not self.is_valid_location(end):
            return None, "Invalid locations provided."
        
        try:
            distances, previous_nodes = self.graph.dijkstra_with_path(start)
            if distances[end] == float('inf'):
                return None, "No path exists between the specified locations."
            
            # Reconstruct path
            path = []
            current = end
            while current:
                path.insert(0, current)
                current = previous_nodes.get(current)
                
            return path, distances[end]
        except Exception as e:
            return None, f"Error calculating path: {str(e)}"

    def get_nearby_locations(self, location, max_distance):
        """Gets all locations within a specified distance from the given location."""
        if not self.is_valid_location(location):
            return []
        
        try:
            distances, _ = self.graph.dijkstra(location)
            return [loc for loc, dist in distances.items() if 0 < dist <= max_distance]
        except Exception:
            return []

    def get_distance_between(self, start, end):
        """Returns the shortest path distance between two locations."""
        if not self.is_valid_location(start) or not self.is_valid_location(end):
            return None
            
        try:
            distances, _ = self.graph.dijkstra(start)
            distance = distances.get(end)
            return None if distance == float('inf') else distance
        except Exception:
            return None

    def is_valid_location(self, location):
        """Checks if a location exists in the map."""
        return location in self.graph.nodes

    def save(self):
        """Save the current state of the graph."""
        save_data_to_file(self.graph, self.file_path)
