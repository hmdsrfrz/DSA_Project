from data_structures import HashTable, DoublyLinkedList
import uuid

# driver_management.py
class DriverManagement:
    def __init__(self):
        self.drivers = HashTable()
        self.active_drivers = HashTable()  # Currently available drivers
        self.drivers.load_from_file('drivers_data.json')
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
            return True
        return False
        
    def set_driver_availability(self, driver_id, available):
        if available:
            driver_data = self.drivers.get(driver_id)
            if driver_data and not driver_data['active_ride']:
                self.active_drivers.insert(driver_id, driver_data)
                return True
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
        return self.active_drivers.table.values()

    def get_driver_by_id(self, driver_id):
        return self.drivers.get(driver_id)