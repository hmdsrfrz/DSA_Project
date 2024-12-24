from data_structures import Graph
from save_load import save_data_to_file, load_data_from_file

class SocialRideshare:
    def __init__(self, file_path='user_connections.json'):
        """
        Initializes the SocialRideshare with user connections loaded from a file if it exists.
        """
        self.file_path = file_path
        self.user_connections = load_data_from_file(self.file_path, Graph)  # Load the graph from file

    def add_connection(self, user1, user2):
        """
        Establishes a connection between two users for potential ridesharing and saves the updated graph.
        """
        self.user_connections.add_node(user1)
        self.user_connections.add_node(user2)
        self.user_connections.add_edge(user1, user2, 1)  # Edge weight represents connection strength
        save_data_to_file(self.user_connections, self.file_path)  # Save the graph to file

    def find_rideshare_partners(self, user, pickup_location, dropoff_location):
        """
        Finds potential rideshare partners based on user connections and route similarity.
        """
        potential_partners = self.user_connections.get_neighbors(user)
        matches = []

        for partner in potential_partners:
            # Here you can add logic to match routes based on similarity (e.g., same path, close destinations).
            matches.append(partner)

        return matches
