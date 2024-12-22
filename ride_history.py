# ride_history.py
from data_structures import DoublyLinkedList

class RideHistory:
    def __init__(self):
        self.ride_history = DoublyLinkedList()

    def add_ride(self, ride_data):
        """
        Adds a ride record to the user's ride history.
        """
        self.ride_history.append(ride_data)

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
