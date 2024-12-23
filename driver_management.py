from data_structures import HashTable, DoublyLinkedList, PriorityQueue
from save_load import save_data_to_file, load_data_from_file
import uuid
import time

class DriverManagement:
    def __init__(self):
        # Load drivers from file or initialize an empty HashTable
        self.drivers = load_data_from_file('drivers_data.json', HashTable)
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
        self.drivers.save_to_file('drivers_data.json')
        return True, driver_id

    def login_driver(self, email, password):
        print("Debug: Drivers table contents:", self.drivers.table)  # Debug statement
        for bucket in self.drivers.table.values():
            print("Debug: Current bucket:", bucket)  # Debug statement
            if bucket:  # Ensure the bucket is not empty
                for driver_id, driver_data in bucket:  # Iterate through the list of key-value pairs
                    print("Debug: Checking driver_data:", driver_data)  # Debug statement
                    if isinstance(driver_data, dict) and driver_data.get('email') == email and driver_data.get('password') == password:
                        return True, driver_id
        return False, "Invalid credentials"

    def update_driver_location(self, driver_id, location):
        driver_data = self.drivers.get(driver_id)
        if driver_data:
            driver_data['current_location'] = location
            self.drivers.insert(driver_id, driver_data)
            # Save updated data
            self.drivers.save_to_file('drivers_data.json')
            return True
        return False
    

    def set_driver_availability(self, driver_id, available):
        driver_data = self.drivers.get(driver_id)
        if driver_data:
            driver_data['availability'] = available  # Add or update availability
            self.drivers.insert(driver_id, driver_data)
            self.drivers.save_to_file('drivers_data.json')  # Save changes
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
        ride_requests = load_data_from_file('ride_requests.json', PriorityQueue) or PriorityQueue()

        if ride_requests.is_empty():
            print("No ride requests available.")
            return

        print("\n--- Ride Requests ---")
        requests_list = sorted(ride_requests.heap, key=lambda x: x[0])  # Sort by priority
        for idx, (_, request) in enumerate(requests_list, start=1):
            print(f"{idx}. Priority: {request['priority']}, Pickup: {request['pickup_location']}, Dropoff: {request['dropoff_location']}, User ID: {request['user_id']}")

        try:
            # Driver selects a ride
            choice = int(input("Enter the number of the ride to accept: ")) - 1
            if 0 <= choice < len(requests_list):
                selected_request = requests_list.pop(choice)[1]

                # Update the queue
                ride_requests.heap = requests_list
                save_data_to_file(ride_requests, 'ride_requests.json')

                # Move selected request to active rides
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
                save_data_to_file(active_rides, 'active_rides.json')

                print("Ride accepted successfully!")
            else:
                print("Invalid selection.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
