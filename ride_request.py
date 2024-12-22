#ride_request.py
from data_structures import PriorityQueue, Queue, HashTable
import time
import uuid

class RideRequest:
    def __init__(self, user_management, driver_management):
        self.user_mgmt = user_management
        self.driver_mgmt = driver_management
        self.normal_requests = Queue()
        self.emergency_requests = PriorityQueue()
        self.active_rides = HashTable()
        
    def request_ride(self, user_id, pickup_location, dropoff_location, is_emergency=False):
        user = self.user_mgmt.get_user_by_id(user_id)
        if not user or user['active_ride']:
            return False, "Invalid user or user already has active ride"
            
        request = {
            'id': str(uuid.uuid4()),
            'user_id': user_id,
            'pickup_location': pickup_location,
            'dropoff_location': dropoff_location,
            'status': 'pending',
            'timestamp': time.time()
        }
        
        if is_emergency:
            self.emergency_requests.push(1, request)  # Priority 1 for emergency
        else:
            self.normal_requests.enqueue(request)
            
        return True, request['id']
        
    def process_ride_requests(self):
        # Process emergency requests first
        while not self.emergency_requests.is_empty():
            request = self.emergency_requests.pop()
            driver = self._find_nearest_driver(request['pickup_location'])
            if driver:
                self._assign_ride(request, driver['id'])
                
        # Process normal requests
        while not self.normal_requests.is_empty():
            request = self.normal_requests.dequeue()
            driver = self._find_nearest_driver(request['pickup_location'])
            if driver:
                self._assign_ride(request, driver['id'])
            else:
                self.normal_requests.enqueue(request)  # Re-queue if no driver found
                
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
        
    def _assign_ride(self, request, driver_id):
        ride_id = str(uuid.uuid4())
        ride_data = {
            'id': ride_id,
            'request': request,
            'driver_id': driver_id,
            'status': 'assigned',
            'start_time': time.time()
        }
        
        self.active_rides.insert(ride_id, ride_data)
        
        # Update user and driver status
        user = self.user_mgmt.get_user_by_id(request['user_id'])
        driver = self.driver_mgmt.get_driver_by_id(driver_id)
        
        user['active_ride'] = ride_id
        driver['active_ride'] = ride_id
        
        self.driver_mgmt.set_driver_availability(driver_id, False)
        
        return ride_id