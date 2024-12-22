# emergency_handler.py
from data_structures import PriorityQueue
import time
import uuid

class EmergencyHandler:
    def __init__(self, ride_request, location_service, driver_management):
        self.ride_request = ride_request
        self.location_service = location_service
        self.driver_mgmt = driver_management
        self.emergency_requests = PriorityQueue()

    def add_emergency_request(self, user_id, pickup_location, dropoff_location):
        """
        Adds an emergency ride request to the queue with the highest priority.
        Simulates forwarding the request to a 911-like service.
        """
        request = {
            'id': str(uuid.uuid4()),
            'user_id': user_id,
            'pickup_location': pickup_location,
            'dropoff_location': dropoff_location,
            'timestamp': time.time(),
        }
        print(f"Emergency request forwarded to 911 service: {request}")
        self.emergency_requests.push(1, request)  # Priority 1 for emergency requests
        return True, request['id']

    def dispatch_emergency_ride(self):
        """
        Processes the emergency ride queue and dispatches the nearest available emergency vehicle.
        Simulates fetching emergency vehicle location data from a 911-like service.
        """
        if self.emergency_requests.is_empty():
            return False, "No emergency requests in the queue."

        request = self.emergency_requests.pop()
        # Simulate receiving nearest vehicle location from 911 service
        print(f"Fetching nearest emergency vehicle for request: {request['id']}")
        driver = self._find_nearest_driver(request['pickup_location'])

        if driver:
            ride_id = self.ride_request._assign_ride(request, driver['id'])
            return True, f"Emergency ride dispatched. Ride ID: {ride_id}"

        return False, "No available emergency vehicles for dispatch."

    def _find_nearest_driver(self, pickup_location):
        """
        Finds the nearest available driver for the given pickup location.
        Simulates receiving driver data from 911.
        """
        available_drivers = self.driver_mgmt.get_available_drivers()
        print("Available drivers fetched from 911 system.")
        nearest_driver = None
        min_distance = float('inf')

        for driver in available_drivers:
            if driver['current_location']:
                distance = self.location_service.get_shortest_path_distance(pickup_location, driver['current_location'])
                if distance < min_distance:
                    min_distance = distance
                    nearest_driver = driver

        return nearest_driver
