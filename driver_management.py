from data_structures import HashTable, DoublyLinkedList, PriorityQueue
from save_load import save_data_to_file, load_data_from_file
import uuid
import time

class DriverManagement:
    def __init__(self):
        # Load drivers from file or initialize an empty HashTable
        self.drivers = load_data_from_file('drivers_data.json', HashTable) or HashTable()
        self.active_drivers = HashTable()  # Currently available drivers

    def register_driver(self, name, email, phone, password, vehicle_type, license_number):
        driver_id = str(uuid.uuid4())
        driver_data = {
            'id': driver_id,
            'name': name,
            'email': email,
            'phone': phone,
            'password': password,  # Should be hashed in real system
            'vehicle_type': vehicle_type,
            'license_number': license_number,
            'rating': 0.0,
            'total_ratings': 0,
            'current_location': None,
            'active_ride': None,
            'ride_history': DoublyLinkedList()
        }

        if self.get_driver_by_email(email):
            return False, "Email already registered"

        self.drivers.insert(driver_id, driver_data)
        # Save to file immediately
        save_data_to_file(self.drivers, 'drivers_data.json')
        return True, driver_id

    def login_driver(self, email, password):
        print("Debug: Drivers table contents:", self.drivers.table)  # Debug statement
        for bucket in self.drivers.table:  # Iterate over each bucket
            print("Debug: Current bucket:", bucket)  # Debug statement
            if bucket:  # Ensure the bucket is not empty
                for driver_id, driver_data in bucket:  # Iterate through the list of key-value pairs
                    print("Debug: Checking driver_data:", driver_data)  # Debug statement
                    if isinstance(driver_data, dict) and driver_data.get('email') == email and driver_data.get('password') == password:
                        return True, driver_id
        return False, "Invalid credentials"

    
    def update_driver(self, driver):
        # Logic to save the updated driver data back to the data store
        drivers_data = load_data_from_file('drivers.json', dict)  # Load existing drivers
        drivers_data[driver['id']] = driver  # Update the driver using the ID as the key
        save_data_to_file(drivers_data, 'drivers.json')  # Save updated drivers

    def update_driver_location(self, driver_id, location):
        driver_data = self.drivers.get(driver_id)
        if driver_data:
            driver_data['current_location'] = location
            self.drivers.insert(driver_id, driver_data)
            # Save updated data
            save_data_to_file(self.drivers, 'drivers_data.json')
            return True
        return False
    

    def set_driver_availability(self, driver_id, available):
        driver_data = self.drivers.get(driver_id)
        if driver_data:
            driver_data['availability'] = available  # Add or update availability
            self.drivers.insert(driver_id, driver_data)
            save_data_to_file(self.drivers, 'drivers_data.json')  # Save changes
        if available:
            self.active_drivers.insert(driver_id, driver_data)
        else:
            self.active_drivers.delete(driver_id)
            return True
        return False

    def get_driver_by_email(self, email):
        # Check if any driver has the given email
        for driver_data_list in self.drivers.table:
            if driver_data_list:  # Ensure there is data in this bucket
                for _, driver in driver_data_list:
                    if driver['email'] == email:
                        return driver
        return None

    def get_available_drivers(self):
        return [driver for driver in self.drivers.values() if driver.get('availability')]


    def get_driver_by_id(self, driver_id):
        return self.drivers.get(driver_id)
    
  
    '''def view_ride_requests(self, driver_id):
        ride_requests = load_data_from_file('ride_requests.json', list) or []
        
        if not ride_requests:
            print("No ride requests available.")
            return

        print("\n--- Ride Requests ---")
        for idx, request in enumerate(ride_requests, start=1):
            print(f"{idx}. Pickup: {request['pickup_location']}, Dropoff: {request['dropoff_location']}, User ID: {request['user_id']}")

        try:
            choice = int(input("Enter the number of the ride to accept: ")) - 1
            if 0 <= choice < len(ride_requests):
                selected_request = ride_requests.pop(choice)
                
                # Move to active rides
                active_rides = load_data_from_file('active_rides.json', list) or []
                active_rides.append({
                    "id": selected_request["id"],
                    "user_id": selected_request["user_id"],
                    "driver_id": driver_id,
                    "pickup_location": selected_request["pickup_location"],
                    "dropoff_location": selected_request["dropoff_location"],
                    "status": "ongoing",
                    "start_time": time.time()
                })

                # Save updated files
                save_data_to_file(ride_requests, 'ride_requests.json')
                save_data_to_file(active_rides, 'active_rides.json')
                print("Ride accepted successfully!")
            else:
                print("Invalid selection.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")'''
    

    def view_ride_requests(self, driver_id):
        # Load raw data from JSON file
        ride_requests_raw = load_data_from_file('normal_requests.json', dict)
        print(f"Debug: Raw ride requests loaded:\n{ride_requests_raw}")

        # Check if the raw data contains the 'queue' key
        if not ride_requests_raw or 'queue' not in ride_requests_raw:
            print("No ride requests available.")
            return

        # Extract the queue and convert to PriorityQueue
        try:
            ride_requests = PriorityQueue()
            for request in ride_requests_raw['queue']:
                # Add requests to the priority queue with their distance or priority
                priority = request.get('priority', 2)  # Default to priority 2 if missing
                ride_requests.push(priority, request)
            print(f"Debug: PriorityQueue state after loading:\n{ride_requests.heap}")
        except Exception as e:
            print(f"Error processing ride requests: {e}")
            return

        if ride_requests.is_empty():
            print("No ride requests available.")
            return

        print("\n--- Ride Requests ---")
        # Sort requests by priority for display
        requests_list = sorted(ride_requests.heap, key=lambda x: x[0])  # Sort by priority
        for idx, (_, request) in enumerate(requests_list, start=1):
            # Use .get() to avoid KeyError
            print(f"{idx}. Priority: {request.get('priority', 'N/A')}, "
                  f"Pickup: {request.get('pickup_location', 'N/A')}, "
                  f"Dropoff: {request.get('dropoff_location', 'N/A')}, "
                  f"User  ID: {request.get('user_id', 'N/A')}")

        try:
            # Prompt driver to select a ride
            choice = int(input("Enter the number of the ride to accept: ")) - 1
            if 0 <= choice < len(requests_list):
                # Select the chosen request
                selected_request = requests_list.pop(choice)[1]

                # Debug: Show the selected request
                print(f"Debug: Selected request details:\n{selected_request}")

                # Update the queue
                ride_requests.heap = [(priority, req) for priority, req in requests_list]
                save_data_to_file({'queue': ride_requests.to_list()}, 'normal_requests.json')
                print("Debug: Updated normal requests saved successfully.")

                # Move the selected request to active rides
                active_rides = load_data_from_file('active_rides.json', dict) or {}
                ride_id = selected_request.get("id")  # Get the ride ID from the selected request
                active_ride = {
                    "id": ride_id,
                    "user_id": selected_request.get("user_id"),
                    "driver_id": driver_id,
                    "pickup_location": selected_request.get("pickup_location"),
                    "dropoff_location": selected_request.get("dropoff_location"),
                    "status": "ongoing",
                    "start_time": time.time()
                }
                active_rides[ride_id] = active_ride  # Use ride_id as the key
                save_data_to_file(active_rides, 'active_rides.json')  # Save the updated active rides

                print(f"Debug: Added ride to active rides:\n{active_ride}")
                print("Ride accepted successfully!")
            else:
                print("Invalid selection. Please choose a valid ride number.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    def sync_active_rides_with_drivers(self, driver_id):
        # Load active rides as a dictionary
        active_rides = load_data_from_file('active_rides.json', dict) or {}
        print(f"Debug: Loaded active rides: {active_rides}")

        # Load drivers data as a dictionary
        drivers_data = load_data_from_file('drivers_data.json', dict) or {}
        print(f"Debug: Loaded drivers data: {drivers_data}")

        # Create a mapping of driver IDs to their active rides
        driver_to_active_ride = {}
        for ride_id, ride in active_rides.items():  # Iterate over the dictionary
            driver_to_active_ride[ride['driver_id']] = ride['id']

        print(f"Debug: Driver to active ride mapping: {driver_to_active_ride}")

        # Check if the specified driver ID exists in the drivers data
        if driver_id in drivers_data:
            driver = drivers_data[driver_id]
            # Update the driver's active_ride field
            if driver_id in driver_to_active_ride:
                driver['active_ride'] = driver_to_active_ride[driver_id]
            else:
                driver['active_ride'] = None

            # Save updated drivers data
            save_data_to_file(drivers_data, 'drivers_data.json')
            print("Debug: Updated drivers_data.json successfully.")
        else:
            print(f"Debug: Driver with ID {driver_id} not found in drivers data.")