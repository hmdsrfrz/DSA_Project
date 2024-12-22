# location_service.py
from data_structures import Graph
from map_data import IslamabadMap
from map_data import LOCATIONS  # If you need LOCATIONS to get coordinates, etc.

class LocationService:
    def __init__(self, map_data):
        self.graph = Graph()
        self._initialize_map(map_data)

    def _initialize_map(self, map_data):
        """
        Initializes the graph with locations and distances from the map data.
        """
        # Use map_data's method to get all locations
        locations = map_data.get_all_locations()  # This method returns a list of locations
        for location in locations:
            self.graph.add_node(location)

        # Use the global DISTANCES constant
        from map_data import DISTANCES  # Import DISTANCES explicitly if it's not globally available
        for (start, end), distance in DISTANCES.items():  # Now we use DISTANCES directly
            self.graph.add_edge(start, end, distance)

    def get_shortest_path(self, start, end):
        # Implement the method to get the shortest path
        pass

    def get_nearby_locations(self, location, max_distance):
        """
        Gets all locations within a specified distance from the given location.
        """
        distances, _ = self.graph.dijkstra(location)
        return [loc for loc, dist in distances.items() if dist <= max_distance]

    def get_distance_between(self, start, end):
        """
        Returns the direct distance between two connected locations, if available.
        """
        return self.graph.nodes.get(start, {}).get(end, None)

    def is_valid_location(self, location):
        """
        Checks if a location exists in the map.
        """
        return location in self.graph.nodes
