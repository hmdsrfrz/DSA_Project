from data_structures import PriorityQueue, Queue, HashTable, Graph
from save_load import save_data_to_file, load_data_from_file
from rating_system import RatingSystem
import map_visualization
import time
import uuid
from datetime import datetime

class RideRequest:
    def __init__(self, user_management, driver_management, location_service, pricing):  # Added missing dependencies
        self.user_mgmt = user_management
        self.driver_mgmt = driver_management
        self.location_service = location_service  # Added missing service
        self.pricing = pricing  # Added missing service
        self.rating_system = RatingSystem  # Store rating system instance
        self.map_visualization = map_visualization
        self.normal_requests = load_data_from_file('normal_requests.json', Queue) or Queue()  # Added fallback
        self.emergency_requests = load_data_from_file('emergency_requests.json', PriorityQueue) or PriorityQueue()
        self.active_rides = load_data_from_file('active_rides.json', HashTable) or HashTable()

                # Ensure the graph is initialized correctly

        if not isinstance(self.location_service.graph, Graph):
            self.location_service.graph = self.location_service._initialize_map()
    
    def request_ride(self, user_id, pickup_location, dropoff_location, is_emergency=False):
        user = self.user_mgmt.get_user_by_id(user_id)
        if not user or user['active_ride']:
            print(f"Debug: User validation failed. User data: {user}")
            return False, "Invalid user or user already has active ride"
        
        self.normal_requests = load_data_from_file('normal_requests.json', Queue)
        if not isinstance(self.normal_requests, Queue):
            print("Debug: Loaded data is not a Queue. Initializing empty Queue.")
            self.normal_requests = Queue()

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
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
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
            'request': request,
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
    
    def complete_ride(self, driver_id):
        print(f"Debug: Starting complete_ride for driver_id: {driver_id}")
        
        # Load data from files
        active_rides = load_data_from_file('active_rides.json', list) or []
        ride_history = load_data_from_file('ride_history.json', list) or []
        user_data = load_data_from_file('users_data.json', dict) or {}
        driver_data = load_data_from_file('drivers_data.json', dict) or {}

        # Find rides associated with the driver
        matching_rides = [
            ride for ride in active_rides
            if ride.get('driver_id') == driver_id
        ]
        
        if not matching_rides:
            print(f"Debug: No active rides found for driver_id: {driver_id}")
            print(f"Debug: Active rides list: {active_rides}")
            return False, "No active ride found for this driver."

        # Sort rides by timestamp to get the most recent one
        most_recent_ride = sorted(
            matching_rides,
            key=lambda x: x.get('timestamp', 0),
            reverse=True
        )[0]

        # Extract ride data
        ride_data = most_recent_ride

        # Ensure rating and feedback exist, initialize to None if not present
        if 'rating' not in ride_data:
            ride_data['rating'] = None
        if 'feedback' not in ride_data:
            ride_data['feedback'] = None

        # Handle duration calculation more robustly
        start_time = ride_data.get('start_time', time.time())
        end_time = time.time()

        # Update ride data
        ride_data['status'] = 'completed'
        ride_data['end_time'] = end_time
        ride_data['duration'] = end_time - start_time

        # Check if it's a merged ride
        if "merged_id" in ride_data:
            # Handle merged ride
            for request in ride_data.get('requests', []):
                user_id = request['user_id']
                if user_id in user_data:
                    user = user_data[user_id]
                    user_ride_entry = {
                        **ride_data,
                        'user_details': {
                            'name': user.get('name'),
                            'email': user.get('email'),
                            'phone': user.get('phone'),
                        },
                    }
                    user['ride_history'].append(user_ride_entry)
                    if user.get('active_ride') == ride_data.get('id'):
                        user['active_ride'] = None
            
            # Update driver history and availability
            driver = driver_data.get(driver_id)
            if driver:
                driver['ride_history'].append(ride_data)
                if driver.get('active_ride') == ride_data.get('id'):
                    driver['active_ride'] = None
                self.driver_mgmt.set_driver_availability(driver_id, True)

        else:
            # Handle individual ride
            user_id = ride_data.get('user_id')
            if user_id in user_data:
                user = user_data[user_id]
                user_ride_entry = {
                    **ride_data,
                    'user_details': {
                        'name': user.get('name'),
                        'email': user.get('email'),
                        'phone': user.get('phone'),
                    },
                }
                user['ride_history'].append(user_ride_entry)
                if user.get('active_ride') == ride_data.get('id'):
                    user['active_ride'] = None
            
            # Update driver history and availability
            driver = driver_data.get(driver_id)
            print("debug: ", driver)
            if driver:
                driver['ride_history'].append(ride_data)
                if driver.get('active_ride') == ride_data.get('id'):
                    driver['active_ride'] = None
                self.driver_mgmt.set_driver_availability(driver_id, True)

        # Add ride to ride history
        ride_history.append(ride_data)

        # Remove the ride from active rides
        active_rides.remove(ride_data)

        # Save updates
        save_data_to_file(active_rides, 'active_rides.json')
        save_data_to_file(ride_history, 'ride_history.json')
        save_data_to_file(user_data, 'users_data.json')
        save_data_to_file(driver_data, 'drivers_data.json')

        return True, "Ride completed successfully"

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

        # Update the active ride in the active rides list
        active_ride = {
            "id": ride_id,
            "user_id": ride_request['user_id'],
            "driver_id": driver_id,
            "pickup_location": ride_request['pickup_location'],
            "dropoff_location": ride_request['dropoff_location'],
            "status": "ongoing",
            "start_time": time.time()
        }

        # Load current active rides as a dictionary
        active_rides = load_data_from_file('active_rides.json', dict) or {}
        
        # Use ride_id as the key
        active_rides[ride_id] = active_ride  
        save_data_to_file(active_rides, 'active_rides.json')

        # Update the driver's active ride
        driver = self.driver_mgmt.get_driver_by_id(driver_id)
        print(driver_id)
        print(f"Debug: Retrieved driver before update: {driver}")  # Debug print
        if driver:
            driver['active_ride'] = ride_id  # Set the active ride ID
            self.driver_mgmt.update_driver(driver)
            self.driver_mgmt._sync_driver_requests(driver_id)
              # Ensure you have a method to update the driver in your data store
            print(f"Debug: Updated driver after accepting ride: {driver}")  # Debug print
        else:
            print("Error: Driver not found.")

        return True, "Ride accepted successfully."

    def _calculate_distance(self, location1, location2):
        return self.location_service.get_distance_between(location1, location2) or 0

    def _calculate_fare(self, distance):
        return self.pricing.calculate_fare(distance)



    '''def complete_ride(self, driver_id):
        print(f"Debug: Starting complete_ride for driver_id: {driver_id}")
        
        # Load active rides as a list
        active_rides = load_data_from_file('active_rides.json', list) or []
        ride_history = load_data_from_file('ride_history.json', list) or []
       
        # Find the most recent ride associated with the driver
        matching_rides = [
            (index, ride) for index, ride in enumerate(active_rides)
            if ride.get('driver_id') == driver_id
        ]
        
        if not matching_rides:
            return False, "No active ride found for this driver."
            
        # Sort by start_time in descending order and get the most recent
        most_recent_ride = sorted(
            matching_rides,
            key=lambda x: x[1].get('start_time', 0),
            reverse=True
        )[0]
        ride_index, ride_data = most_recent_ride
       
        # Update ride data
        ride_data['status'] = 'completed'
        ride_data['end_time'] = time.time()
        ride_data['duration'] = ride_data['end_time'] - ride_data['start_time']
       
        user_id = ride_data.get('user_id')
        user = self.user_mgmt.get_user_by_id(user_id)
        driver = self.driver_mgmt.get_driver_by_id(driver_id)
       
        if user and driver:
            # Update histories and clear active rides
            user['ride_history'].append(ride_data)
            driver['ride_history'].append(ride_data)
            
            ride_history_entry = {
                **ride_data,
                'user_details': {
                    'name': user.get('name'),
                    'email': user.get('email'),
                    'phone': user.get('phone')
                },
                'driver_details': {
                    'name': driver.get('name'),
                    'email': driver.get('email'),
                    'phone': driver.get('phone'),
                    'vehicle_type': driver.get('vehicle_type'),
                    'license_number': driver.get('license_number')
                }
            }
           
            ride_history.append(ride_history_entry)
            
            if user.get('active_ride') == ride_data.get('ride_id'):
                user['active_ride'] = None
            if driver.get('active_ride') == ride_data.get('ride_id'):
                driver['active_ride'] = None
           
            # Check for remaining active rides
            remaining_active_rides = any(
                ride.get('driver_id') == driver_id 
                for i, ride in enumerate(active_rides) 
                if i != ride_index
            )
            
            if not remaining_active_rides:
                self.driver_mgmt.set_driver_availability(driver_id, True)
           
            active_rides.pop(ride_index)
               
            # Save updates
            save_data_to_file(active_rides, 'active_rides.json')
            save_data_to_file(ride_history, 'ride_history.json')
           
            return True, "Ride completed successfully"
           
        return False, "Error updating user or driver profiles"
'''    