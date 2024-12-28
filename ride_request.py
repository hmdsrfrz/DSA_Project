from data_structures import PriorityQueue, Queue, HashTable
from save_load import save_data_to_file, load_data_from_file
from rating_system import RatingSystem
import map_visualization
import time
import uuid

class RideRequest:
    def __init__(self, user_management, driver_management, location_service, pricing):  # Added missing dependencies
        self.user_mgmt = user_management
        self.driver_mgmt = driver_management
        self.location_service = location_service  # Added missing service
        self.pricing = pricing  # Added missing service
        self.rating_system = RatingSystem  # Store rating system instance
        self.map_visualization = map_visualization
        self.normal_requests = load_data_from_file('normal_requests.json', Queue) or Queue()
        self.emergency_requests = load_data_from_file('emergency_requests.json', PriorityQueue) or PriorityQueue()

        self.active_rides = load_data_from_file('active_rides.json', HashTable) or HashTable()

    '''def request_ride(self, user_id, pickup_location, dropoff_location, is_emergency=False):
        user = self.user_mgmt.get_user_by_id(user_id)
        print("User Data in request_ride:", user)
        if not user or user['active_ride']:
            print("User Data:", user)
            return False, "Invalid user or user already has active ride"
        


        # Calculate distance and price
        distance = self.location_service.graph.get_shortest_path_distance(pickup_location, dropoff_location)
        if distance is None:
            print("Pickup:", pickup_location, "Destination:", dropoff_location)
            print("Graph Nodes:", self.location_service.graph.nodes)
            print("Graph Edges:", self.location_service.graph.nodes)

            return False, "Could not calculate route"

        price = self.pricing.calculate_fare(distance)

        request = {
            'id': str(uuid.uuid4()),
            'user_id': user_id,
            'pickup_location': pickup_location,
            'dropoff_location': dropoff_location,
            'status': 'pending',
            'timestamp': time.time(),
            'distance': distance,
            'price': price
        }

        if is_emergency:
            self.emergency_requests.push(1, request)
            save_data_to_file(self.emergency_requests, 'emergency_requests.json')
        else:
            self.normal_requests.enqueue(request)
            print("Enqueued Request:", request)
            save_data_to_file(self.normal_requests, 'normal_requests.json')

        return True, request'''
        
    '''def request_ride(self, user_id, pickup_location, dropoff_location, is_emergency=False):
        user = self.user_mgmt.get_user_by_id(user_id)
        if not user or user['active_ride']:
            return False, "Invalid user or user already has active ride"
        
        # Force graph initialization if empty
        if not self.location_service.graph.nodes:
            print("Graph is empty. Reinitializing map...")
            self.location_service.graph = self.location_service._initialize_map()

        # Calculate distance and price
        distance = self.location_service.graph.get_shortest_path_distance(pickup_location, dropoff_location)
        if distance is None:
            return False, "Could not calculate route"

        price = self.pricing.calculate_fare(distance)
        request = {
            'id': str(uuid.uuid4()),
            'user_id': user_id,
            'pickup_location': pickup_location,
            'dropoff_location': dropoff_location,
            'status': 'pending',
            'timestamp': time.time(),
            'distance': distance,
            'price': price
        }

        if is_emergency:
            self.emergency_requests.push(distance, request)
            save_data_to_file(self.emergency_requests, 'emergency_requests.json')
        else:
            self.normal_requests.enqueue(request)
            save_data_to_file(self.normal_requests, 'normal_requests.json')

        return True, request'''
    
    '''def request_ride(self, user_id, pickup_location, dropoff_location, is_emergency=False):
        user = self.user_mgmt.get_user_by_id(user_id)
        if not user or user['active_ride']:
            print(f"Debug: User validation failed. User data: {user}")
            return False, "Invalid user or user already has active ride"

        # Validate graph and locations
        if not self.location_service.graph.nodes:
            print("Debug: Graph is empty. Reinitializing...")
            self.location_service.graph = self.location_service._initialize_map()

        if pickup_location not in self.location_service.graph.nodes:
            print(f"Debug: Pickup location '{pickup_location}' not found in graph.")
            return False, "Invalid pickup location"

        if dropoff_location not in self.location_service.graph.nodes:
            print(f"Debug: Dropoff location '{dropoff_location}' not found in graph.")
            return False, "Invalid dropoff location"

        # Calculate distance and price
        distance = self.location_service.graph.get_shortest_path_distance(pickup_location, dropoff_location)
        if distance is None:
            print(f"Debug: No path found between '{pickup_location}' and '{dropoff_location}'.")
            return False, "Could not calculate route"

        price = self.pricing.calculate_fare(distance)
        print(f"Debug: Calculated price: {price}, Distance: {distance}")

        # Add request to queue
        request = {
            'id': str(uuid.uuid4()),
            'user_id': user_id,
            'pickup_location': pickup_location,
            'dropoff_location': dropoff_location,
            'status': 'pending',
            'timestamp': time.time(),
            'distance': distance,
            'price': price,
            'priority': 1 if is_emergency else 2,
            'type': 'emergency' if is_emergency else 'normal'
        }

        if is_emergency:
            self.emergency_requests.push(1, request)
            print(f"Debug: Emergency request added: {request}")
        else:
            self.normal_requests.enqueue(request)
            print(f"Debug: Normal request added: {request}")

        save_data_to_file(self.normal_requests, 'normal_requests.json')
            # Visualize the shortest path
        print("Debug: Visualizing shortest path...")
        try:
            self.map_visualization.visualize_ride_path(
            location_service=self.location_service,  # Location service
            start=pickup_location,                  # Pickup location (start)
            end=dropoff_location                    # Dropoff location (end)
        )
        except Exception as e:
            print(f"Error during visualization: {e}")
        return True, request'''
    

    def request_ride(self, user_id, pickup_location, dropoff_location, is_emergency=False):
        user = self.user_mgmt.get_user_by_id(user_id)
        
        # Check if the user has an active ride
        if not user or user['active_ride']:
            # Check if the active ride is not completed
            active_ride_id = user['active_ride']
            active_ride = self.active_rides.get(active_ride_id) if active_ride_id else None
            
            if active_ride and active_ride['status'] != 'completed':
                return False, "You have an active ride that is not completed. Please complete it before requesting another ride."

        # Validate graph and locations
        if not self.location_service.graph.nodes:
            print("Debug: Graph is empty. Reinitializing...")
            self.location_service.graph = self.location_service._initialize_map()

        if pickup_location not in self.location_service.graph.nodes:
            print(f"Debug: Pickup location '{pickup_location}' not found in graph.")
            return False, "Invalid pickup location"

        if dropoff_location not in self.location_service.graph.nodes:
            print(f"Debug: Dropoff location '{dropoff_location}' not found in graph.")
            return False, "Invalid dropoff location"

        # Calculate distance and price
        distance = self.location_service.graph.get_shortest_path_distance(pickup_location, dropoff_location)
        if distance is None:
            print(f"Debug: No path found between '{pickup_location}' and '{dropoff_location}'.")
            return False, "Could not calculate route"

        price = self.pricing.calculate_fare(distance)
        print(f"Debug: Calculated price: {price}, Distance: {distance}")

        # Add request to queue
        request = {
            'id': str(uuid.uuid4()),
            'user_id': user_id,
            'pickup_location': pickup_location,
            'dropoff_location': dropoff_location,
            'status': 'pending',
            'timestamp': time.time(),
            'distance': distance,
            'price': price,
            'priority': 1 if is_emergency else 2,
            'type': 'emergency' if is_emergency else 'normal'
        }

        if is_emergency:
            self.emergency_requests.push(1, request)
            print(f"Debug: Emergency request added: {request}")
        else:
            self.normal_requests.enqueue(request)
            print(f"Debug: Normal request added: {request}")

        save_data_to_file(self.normal_requests, 'normal_requests.json')
        
        # Visualize the shortest path
        print("Debug: Visualizing shortest path...")
        try:
            self.map_visualization.visualize_ride_path(
                location_service=self.location_service,  # Location service
                start=pickup_location,                  # Pickup location (start)
                end=dropoff_location                    # Dropoff location (end)
            )
        except Exception as e:
            print(f"Error during visualization: {e}")
        
        return True, request


    def _sync_driver_requests(self):
        """Sync ride requests to driver viewable file (ride_requests.json)."""
        save_data_to_file(self.normal_requests, 'ride_requests.json')


    '''def process_ride_requests(self):
        # Process emergency requests first
        while not self.emergency_requests.is_empty():
            request = self.emergency_requests.pop()
            save_data_to_file(self.emergency_requests, 'emergency_requests.json')
            driver = self._find_nearest_driver(request['pickup_location'])
            if driver:
                self._assign_ride(request, driver['id'])

        # Process normal requests
        while not self.normal_requests.is_empty():
            request = self.normal_requests.dequeue()
            save_data_to_file(self.normal_requests, 'normal_requests.json')
            driver = self._find_nearest_driver(request['pickup_location'])
            if driver:
                self._assign_ride(request, driver['id'])
            else:
                self.normal_requests.enqueue(request)
                save_data_to_file(self.normal_requests, 'normal_requests.json')'''
    
    def process_ride_requests(self):
        # Load ride requests from JSON
        ride_requests = load_data_from_file('ride_requests.json', list)  # Load as a list

        # Convert requests to a priority queue
        priority_queue = PriorityQueue()
        for request in ride_requests:
            priority_queue.push(request['priority'], request)

        # Process requests from the priority queue
        updated_requests = []
        while not priority_queue.is_empty():
            priority, request = priority_queue.pop()

            # Find the nearest driver
            driver = self._find_nearest_driver(request['pickup_location'])
            if driver:
                # Assign ride if a driver is found
                self._assign_ride(request, driver['id'])
            else:
                # Requeue the request if no driver is found
                updated_requests.append(request)

        # Save remaining requests back to the JSON file
        save_data_to_file(updated_requests, 'ride_requests.json')


    def _assign_ride(self, request, driver_id):
        ride_id = str(uuid.uuid4())
        ride_data = {
            'id': ride_id,
            'driver_id': driver_id,
            'status': 'assigned',
            'start_time': time.time()
        }

        # Add to active rides and save
        active_rides = load_data_from_file('active_rides.json', list)  # Load active rides as a list
        active_rides.append(ride_data)
        save_data_to_file(active_rides, 'active_rides.json')

        # Update user and driver statuses
        user = self.user_mgmt.get_user_by_id(request['user_id'])
        driver = self.driver_mgmt.get_driver_by_id(driver_id)

        user['active_ride'] = ride_id
        driver['active_ride'] = ride_id
        self.driver_mgmt.set_driver_availability(driver_id, False)

        return ride_id

    def complete_ride(self, ride_id):
        ride_data = self.active_rides.get(ride_id)
        if not ride_data:
            return False, "Ride not found"

        ride_data['status'] = 'completed'
        ride_data['end_time'] = time.time()
        ride_data['duration'] = ride_data['end_time'] - ride_data['start_time']

        user_id = ride_data['user_id']  # Assuming user_id is directly in ride_data
        driver_id = ride_data['driver_id']

        user = self.user_mgmt.get_user_by_id(user_id)
        driver = self.driver_mgmt.get_driver_by_id(driver_id)

        if user and driver:
            user['ride_history'].append(ride_data)
            driver['ride_history'].append(ride_data)

            user['active_ride'] = None
            driver['active_ride'] = None
            self.driver_mgmt.set_driver_availability(driver_id, True)

            self.active_rides.delete(ride_id)
            save_data_to_file(self.active_rides, 'active_rides.json')

            # Notify the user to provide feedback
            return True, f"Ride completed successfully. Please provide feedback for your ride ID: {ride_id}."
        
        return False, "Error updating user or driver profiles"
    def _find_nearest_driver(self, pickup_location):
        available_drivers = self.driver_mgmt.get_available_drivers()
        nearest_driver = None
        min_distance = float('inf')

        for driver in available_drivers:
            if driver['current_location']:
                distance = self._calculate_distance(pickup_location, driver['current_location'])
                if distance < min_distance:
                    min_distance = distance
                    nearest_driver = driver

        return nearest_driver


    def get_user_updates(self, user_id):
        user = self.user_mgmt.get_user_by_id(user_id)
        if not user or not user['active_ride']:
            return None

        ride_data = self.active_rides.get(user['active_ride'])
        if not ride_data:
            return None

        driver = self.driver_mgmt.get_driver_by_id(ride_data['driver_id'])
        if not driver:
            return None

        return {
            'type': 'ride_accepted',
            'ride_id': ride_data['id'],
            'driver': {
                'name': driver['name'],
                'phone': driver['phone'],
                'vehicle_type': driver['vehicle_type'],
                'current_location': driver['current_location']
            },
            'status': ride_data['status']
        }

    def get_driver_requests(self, current_location):
        if not self.normal_requests.queue:
            return []

        available_requests = []
        for request in self.normal_requests.queue:
            distance_to_pickup = self._calculate_distance(current_location, request['pickup_location'])
            ride_distance = self._calculate_distance(request['pickup_location'], request['dropoff_location'])
            fare = self._calculate_fare(ride_distance)

            request_data = {
                'id': request['id'],
                'pickup_location': request['pickup_location'],
                'dropoff_location': request['dropoff_location'],
                'distance': ride_distance,
                'distance_to_pickup': distance_to_pickup,
                'price': fare
            }
            available_requests.append(request_data)

        return available_requests
    

    def accept_ride(self, ride_request):
        # Logic to accept the ride
        ride_id = ride_request['id']
        driver_id = ride_request['driver_id']

        # Create the active ride data
        active_ride = {
            "id": ride_id,
            "user_id": ride_request['user_id'],
            "driver_id": driver_id,
            "pickup_location": ride_request['pickup_location'],
            "dropoff_location": ride_request['dropoff_location'],
            "status": "ongoing",
            "start_time": time.time()
        }

        # Load current active rides from the JSON file
        active_rides = load_data_from_file('active_rides.json', dict) or {}

        # Update the active rides dictionary with the new ride
        active_rides[ride_id] = active_ride  # Use ride_id as the key
        save_data_to_file(active_rides, 'active_rides.json')  # Save the updated active rides

        # Update the driver's active ride
        driver = self.driver_mgmt.get_driver_by_id(driver_id)
        print(driver_id)
        print(f"Debug: Retrieved driver before update: {driver}")  # Debug print
        if driver:
            driver['active_ride'] = ride_id  # Set the active ride ID
            self.driver_mgmt.update_driver(driver)  # Ensure you have a method to update the driver in your data store
            print(f"Debug: Updated driver after accepting ride: {driver}")  # Debug print
        else:
            print("Error: Driver not found.")

        return True, "Ride accepted successfully."
    
    def _calculate_distance(self, location1, location2):
        return self.location_service.get_distance_between(location1, location2) or 0

    def _calculate_fare(self, distance):
        return self.pricing.calculate_fare(distance)
