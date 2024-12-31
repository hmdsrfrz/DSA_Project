from data_structures import PriorityQueue, Graph
from save_load import save_data_to_file, load_data_from_file
from map_data import IslamabadMap
import time
from datetime import datetime
import uuid

class EmergencyHandler:
    def __init__(self, ride_request, location_service, driver_management, file_path='emergency_requests.json'):
        self.ride_request = ride_request
        self.location_service = location_service
        self.driver_mgmt = driver_management
        self.file_path = file_path
        self.emergency_requests = {}

    def add_emergency_request(self, user_id, pickup_location, dropoff_location, emergency_type):
        """
        Adds an emergency ride request to the dictionary.
        Simulates forwarding the request to a 911-like service.
        
        Args:
            emergency_type (str): Type of emergency ('health' or 'fire')
        """
        request = {
            'id': str(uuid.uuid4()),
            'user_id': user_id,
            'pickup_location': pickup_location,
            'dropoff_location': dropoff_location,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'emergency_type': emergency_type,  # Add the type to the request
        }
        print(f"Emergency request forwarded to 911 service: {request}")
        self.emergency_requests[request['id']] = request  # Store the request by ID

        # Save updated emergency requests to file
        save_data_to_file(self.emergency_requests, self.file_path)
        return True, request['id']
    
    def handle_emergency_request(self, user_id):
        """
        Handles the process of creating an emergency ride request based on the user's needs (health or fire).
        Prompts the user for their type of emergency and location, highlights the shortest path on the map,
        and confirms dispatch of an emergency vehicle.
        """
        print("\n--- Emergency Ride Request ---")
        print("1. Health-related (Nearest Hospital)")
        print("2. Fire-related (Nearest Fire Station)")

        try:
            choice = int(input("Enter the type of emergency (1 or 2): "))
            if choice not in [1, 2]:
                print("Invalid choice. Please select 1 or 2.")
                return False, "Invalid choice."

            emergency_type = "hospital" if choice == 1 else "fire station"

            # Prompt user for current location
            all_locations = self.location_service.map_data.get_all_locations()
            print("\n--- Available Locations ---")
            for idx, location in enumerate(all_locations, start=1):
                print(f"{idx}. {location}")

            location_index = int(input("Enter the number for your current location: "))
            if location_index < 1 or location_index > len(all_locations):
                print("Invalid location selection.")
                return False, "Invalid location selection."

            pickup_location = all_locations[location_index - 1]

            # Find the nearest hospital or fire station
            target_location = self._find_nearest_facility(pickup_location, emergency_type)
            if not target_location:
                print(f"No {emergency_type} found nearby.")
                return False, f"No {emergency_type} found nearby."

            print(f"Nearest {emergency_type.capitalize()} located at: {target_location}")

            # Visualize the path on the map
            path = self.location_service.get_shortest_path(pickup_location, target_location)  # Only get the path
            if path:
                print(f"Shortest path from {pickup_location} to {target_location}: {path}")
                self.location_service.map_data.visualize_ride_path(pickup_location, target_location, highlight_path=path)
            else:
                print("Could not calculate the path.")
                return False, "Could not calculate the path."

            # Create and save the emergency request
            success, request_id = self.add_emergency_request(user_id, pickup_location, target_location, emergency_type)
            if success:
                print("Emergency vehicle is on the way!")
                return True, f"Emergency ride request created successfully. Request ID: {request_id}"

        except ValueError:
            print("Invalid input. Please enter a valid number.")
            return False, "Invalid input."
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")
            return False, "An unexpected error occurred."

    def _find_nearest_facility(self, pickup_location, facility_type):
        print(f"Looking for nearest {facility_type} from {pickup_location}")
        
        facilities = self.location_service.map_data.get_all_locations()
        matching_facilities = [
            loc for loc in facilities
            if facility_type in loc.lower()
        ]

        if not matching_facilities:
            print(f"No {facility_type}s found in the map data.")
            return None

        nearest_facility = None
        min_distance = float('inf')

        for facility in matching_facilities:
            print(f"Checking facility: {facility} against pickup location: {pickup_location}")
            try:
                # Get the path only
                path = self.location_service.get_shortest_path(start=pickup_location, end=facility)
                # Calculate the distance using the existing method
                distance = self.location_service.get_distance_between(start=pickup_location, end=facility)
                print(f"Distance: {distance}, Path: {path}")
                if path and isinstance(distance, (int, float)):
                    if distance < min_distance:
                        min_distance = distance
                        nearest_facility = facility
            except Exception as e:
                print(f"Error finding path to {facility}: {e}")

        if nearest_facility is None:
            print(f"No valid path found to any {facility_type}.")
        else:
            print(f"Nearest {facility_type} found: {nearest_facility} at distance {min_distance}")

        return nearest_facility

    def dispatch_emergency_ride(self):
        """
        Processes the emergency ride queue and dispatches the nearest available emergency vehicle.
        Simulates fetching emergency vehicle location data from a 911-like service.
        """
        if self.emergency_requests.is_empty():
            return False, "No emergency requests in the queue."

        request = self.emergency_requests.pop()
        # Save updated emergency requests to file
        save_data_to_file(self.emergency_requests, self.file_path)

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
