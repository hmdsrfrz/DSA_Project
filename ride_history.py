from data_structures import DoublyLinkedList, HashTable
from save_load import save_data_to_file, load_data_from_file

class RideHistory:
    def __init__(self, file_path='ride_history.json'):
        """
        Initializes the RideHistory with data loaded from a file if it exists.
        """
        self.file_path = file_path
        self.ride_history = load_data_from_file(self.file_path, DoublyLinkedList)

    def add_ride(self, ride_data):
        """
        Adds a ride record to the user's ride history and saves the updated history to the file.
        """
        self.ride_history.append(ride_data)
        save_data_to_file(self.ride_history, self.file_path)

    def get_ride_history(self):
        """
        Returns the list of all past rides in chronological order.
        """
        history = []
        current = self.ride_history.head
        while current:
            history.append(current.data)
            current = current.next
        return history
