from data_structures import HashTable, DoublyLinkedList, PriorityQueue
from save_load import save_data_to_file, load_data_from_file
import uuid
import time
import json

class DriverManagement:
    def __init__(self):
        # Load drivers from file or initialize an empty HashTable
        self.drivers = load_data_from_file('drivers_data.json', HashTable)
        self.active_drivers = HashTable()  # Currently available drivers

    def register_driver(self, name, email, phone, password, vehicle_type, license_number):
        """
        Register a new driver with simplified data handling.
        Returns tuple of (success, result).
        """
        try:
            driver_id = str(uuid.uuid4())
            
            driver_data = {
                "id": driver_id,
                "name": name,
                "email": email,
                "phone": phone,
                "password": password,
                "vehicle_type": vehicle_type,
                "license_number": license_number,
                "status": "available",
                "rating": 0.0,
                "total_rides": 0
            }

            # Load existing drivers
            try:
                with open('drivers_data.json', 'r') as f:
                    drivers = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                drivers = {}

            # Add new driver
            drivers[driver_id] = driver_data

            # Save updated drivers
            with open('drivers_data.json', 'w') as f:
                json.dump(drivers, f, indent=4)

            return True, driver_id

        except Exception as e:
            return False, f"Registration failed: {str(e)}"

    def login_driver(self, email, password):
        #print("Debug: Drivers table contents:", self.drivers.table)  # Debug statement
        for bucket in self.drivers.table.values():
           #print("Debug: Current bucket:", bucket)  # Debug statement
            if bucket:  # Ensure the bucket is not empty
                for driver_id, driver_data in bucket:  # Iterate through the list of key-value pairs
                    #print("Debug: Checking driver_data:", driver_data)  # Debug statement
                    if isinstance(driver_data, dict) and driver_data.get('email') == email and driver_data.get('password') == password:
                        return True, driver_id
        return False, "Invalid credentials"
    
    def update_driver(self, driver):
        # Logic to save the updated driver data back to the data store
        drivers_data = load_data_from_file('drivers_data.json', dict)  # Load existing drivers
        drivers_data[driver['id']] = driver  # Update the driver using the ID as the key
        save_data_to_file(drivers_data, 'drivers_data.json')  # Save updated drivers

    def update_driver_active_ride(self, driver_id, active_ride_id):
        """Update the active ride for a specific driver."""
        drivers_data = load_data_from_file('drivers_data.json', dict)  # Load existing drivers
        if driver_id in drivers_data:
            driver = drivers_data[driver_id]
            driver['active_ride'] = active_ride_id  # Update the active ride
            self.update_driver(driver)  # Call the existing method to save the updated driver
        else:
            print(f"Driver with ID {driver_id} not found.")

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
    
    
    def view_ride_requests(self, driver_id):
        # Load raw data from JSON file
        ride_requests_raw = load_data_from_file('normal_requests.json', dict)
        #print(f"Debug: Raw ride requests loaded:\n{ride_requests_raw}")

        # Check if the raw data is a list or a dictionary
        if isinstance(ride_requests_raw, list):
            requests_list = ride_requests_raw
        elif isinstance(ride_requests_raw, dict) and 'queue' in ride_requests_raw:
            requests_list = ride_requests_raw['queue']
        else:
            print("No ride requests available.")
            return

        # Extract the queue and convert to PriorityQueue
        try:
            ride_requests = PriorityQueue()
            for request in requests_list:
                priority = request.get('priority', 2)  # Default to priority 2 if missing
                ride_requests.push(priority, request)
            #print(f"Debug: PriorityQueue state after loading:\n{ride_requests.heap}")
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
            print(f"{idx}. Priority: {request.get('priority', 'N/A')}, "
                f"Pickup: {request.get('pickup_location', 'N/A')}, "
                f"Dropoff: {request.get('dropoff_location', 'N/A')}, "
                f"User ID: {request.get('user_id', 'N/A')}")

        try:
            # Prompt driver to select a ride
            choice = int(input("Enter the number of the ride to accept: ")) - 1
            if 0 <= choice < len(requests_list):
                # Select the chosen request
                selected_request = requests_list.pop(choice)[1]
                #print(f"Debug: Selected request details:\n{selected_request}")

                # Update the queue
                ride_requests.heap = [(priority, req) for priority, req in requests_list]
                save_data_to_file({'queue': ride_requests.to_list()}, 'normal_requests.json')
                print("Debug: Updated normal_requests.json successfully.")

                # Move the selected request to active rides
                # Modify this section in your view_ride_requests function
                # Move the selected request to active rides
                active_rides = load_data_from_file('active_rides.json', dict) or []  # Changed default to list
                #print(f"Debug: Active rides before update:\n{active_rides}")

                # Create the new active ride
                active_ride = {
                    "id": selected_request.get("id"),
                    "user_id": selected_request.get("user_id"),
                    "driver_id": driver_id,
                    "pickup_location": selected_request.get("pickup_location"),
                    "dropoff_location": selected_request.get("dropoff_location"),
                    "status": "ongoing",
                    "start_time": time.time()
                }

                # Append to list instead of using dictionary key
                active_rides.append(active_ride)
                #print(f"Debug: Active rides after update:\n{active_rides}")

                # Save the updated active rides to the file
                save_data_to_file(active_rides, 'active_rides.json')
                print("Debug: Updated active_rides.json successfully.")

                print("Ride accepted successfully!")
            else:
                print("Invalid selection. Please choose a valid ride number.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
        except Exception as e:
            print(f"Error: {e}")


    def sync_active_rides_with_drivers(self, driver_id):
        # Load active rides as a list
        active_rides = load_data_from_file('active_rides.json', list) or []
        print(f"Debug: Loaded active rides: {active_rides}")

        # Load drivers data as a dictionary
        drivers_data = load_data_from_file('drivers_data.json', dict) or {}
        print(f"Debug: Loaded drivers data: {drivers_data}")

        # Create a mapping of driver IDs to their active rides
        driver_to_active_ride = {}
        for ride in active_rides:  # Iterate over the list
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
