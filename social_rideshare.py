import time
from data_structures import Graph
from save_load import save_data_to_file, load_data_from_file
from datetime import datetime

class SocialRideshare:
    def __init__(self, user_mgmt, driver_mgmt, location_service, friend_mgmt, pricing_service):
        self.user_mgmt = user_mgmt
        self.driver_mgmt = driver_mgmt
        self.location_service = location_service
        self.friend_mgmt = friend_mgmt
        self.pricing_service = pricing_service
        self.pending_rides = self.load_pending_rides()  # Load from file on init
        self.active_rides = self.load_active_rides()    # Load active rides from file
        
    def load_pending_rides(self):
        """Load pending rides from JSON file."""
        return load_data_from_file('pending_rides.json', dict) or {}
        
    def load_active_rides(self):
        """Load active rides from JSON file."""
        return load_data_from_file('active_rides.json', dict) or {}
        
    def save_pending_rides(self):
        """Save pending rides to JSON file."""
        save_data_to_file(self.pending_rides, 'pending_rides.json')
        
    def save_active_rides(self):
        """Save active rides to JSON file."""
        save_data_to_file(self.active_rides, 'active_rides.json')
        
    def request_ride(self, user_id, pickup_location, dropoff_location):
        """Create a new ride request with social matching capability."""
        user = self.user_mgmt.get_user_by_id(user_id)
        if not user:
            return False, "User not found."
            
        # Reload pending rides to get latest state
        self.pending_rides = self.load_pending_rides()
            
        # Create ride request
        request = {
            'request_id': f"req_{int(time.time())}_{user_id}",
            'user_id': user_id,
            'user_name': user['name'],  # Add user name for easier display
            'pickup_location': pickup_location,
            'dropoff_location': dropoff_location,
            'timestamp': time.time(),
            'status': 'pending',
            'matched_with': None,
            'is_merged': False
        }
        
        # Store the request and save immediately
        self.pending_rides[request['request_id']] = request
        self.save_pending_rides()
        
        # Look for potential matches
        matched_request = self._find_friend_match(request)
        
        if matched_request:
            # Merge the rides
            merged_ride = self._merge_rides(request, matched_request)
            return True, f"Ride request created and merged with {matched_request['user_name']}'s ride"
        
        return True, "Ride request created successfully. Looking for matches..."

    def find_friend_rides(self, user_id):
        """Find and return all available ride requests from friends."""
        # Reload pending rides to get latest state
        self.pending_rides = self.load_pending_rides()
        
        # Get list of friends
        friends_list = self.friend_mgmt.get_friends_list(user_id)
        if not friends_list:
            return []

        # Extract friend IDs
        friend_ids = [friend[0] for friend in friends_list]
        
        # Find all pending rides from friends
        friend_rides = []
        for req_id, ride in self.pending_rides.items():
            if (ride['user_id'] in friend_ids and 
                ride['status'] == 'pending' and 
                not ride['is_merged']):
                friend_rides.append(ride)
        
        return friend_rides

    def _merge_rides(self, request1, request2):
        """Merge two ride requests."""
        merged_id = f"merged_{int(time.time())}"
        
        total_fare = self.calculate_fare(
            request1['pickup_location'], request1['dropoff_location']
        )
        split_fare = total_fare / 2
        
        # Create merged ride object
        merged_ride = {
            'merged_id': merged_id,
            'requests': [request1, request2],
            'status': 'pending',
            'total_fare': total_fare,
            'split_fare': split_fare,
            'pickup_location': request1['pickup_location'],
            'dropoff_location': request1['dropoff_location'],
            'timestamp': time.time()
        }
        
        # Mark individual requests as merged
        request1['is_merged'] = True
        request1['matched_with'] = request2['request_id']
        request2['is_merged'] = True
        request2['matched_with'] = request1['request_id']
        
        # Save merged ride and update pending rides
        self.pending_rides[merged_id] = merged_ride
        self.save_pending_rides()
        
        return merged_ride

    def join_friend_ride(self, user_id, friend_ride):
        """Join an existing friend's ride request."""
        # Reload pending rides to get latest state
        self.pending_rides = self.load_pending_rides()
        
        # Verify the ride is still available
        if not isinstance(friend_ride, dict):
            return False, "Invalid ride data"
            
        ride_id = friend_ride.get('request_id')
        if not ride_id or ride_id not in self.pending_rides:
            return False, "This ride is no longer available."
        
        if self.pending_rides[ride_id].get('is_merged', False):
            return False, "This ride is no longer available for joining."
        
        user = self.user_mgmt.get_user_by_id(user_id)
        if not user:
            return False, "User not found."
            
        # Create a new ride request for the joining user
        request = {
            'request_id': f"req_{int(time.time())}_{user_id}",
            'user_id': user_id,
            'user_name': user['name'],
            'pickup_location': friend_ride['pickup_location'],
            'dropoff_location': friend_ride['dropoff_location'],
            'timestamp': time.time(),
            'status': 'pending',
            'matched_with': None,
            'is_merged': False
        }
        
        # Store the request
        self.pending_rides[request['request_id']] = request
        
        try:
            # Merge with friend's ride
            merged_ride = self._merge_rides(request, self.pending_rides[ride_id])
            self.save_pending_rides()
            return True, f"Successfully joined ride with {friend_ride['user_name']}"
        except Exception as e:
            # Remove the request if merging fails
            if request['request_id'] in self.pending_rides:
                del self.pending_rides[request['request_id']]
            self.save_pending_rides()
            return False, f"Failed to join ride: {str(e)}"

    def _find_friend_match(self, request):
        """
        Find matching ride requests from friends with similar routes.
        """
        # Get user's friends list directly from friend_mgmt
        friends_list = self.friend_mgmt.get_friends_list(request['user_id'])
        if not friends_list:
            return None
            
        # Extract just the friend IDs from the list of tuples
        friend_ids = [friend[0] for friend in friends_list]
                
        for req_id, pending_req in self.pending_rides.items():
            if pending_req['status'] != 'pending' or pending_req['is_merged']:
                continue
                    
            if pending_req['user_id'] in friend_ids:
                # Check if pickup locations are same or adjacent
                pickup_match = self._locations_match(
                    request['pickup_location'],
                    pending_req['pickup_location']
                )
                    
                # Check if dropoff locations match
                dropoff_match = request['dropoff_location'] == pending_req['dropoff_location']
                    
                if pickup_match and dropoff_match:
                    return pending_req
                        
        return None

    def _locations_match(self, loc1, loc2):
        """
        Check if locations are same or adjacent nodes.
        """
        if loc1 == loc2:
            return True
            
        # Get adjacent nodes
        adj_nodes = self.location_service.get_adjacent_locations(loc1)
        return loc2 in adj_nodes


    def save_pending_rides(self):
        save_data_to_file(self.pending_rides, 'pending_rides.json')

    def calculate_fare(self, origin, destination):
        """
        Calculate the fare for a given route.
        """
        distance = self.location_service.get_distance_between(origin, destination)
        return self.pricing_service.calculate_fare(distance)

    def get_ride_status(self, request_id):
        """
        Get the current status of a ride request.
        """
        if request_id in self.pending_rides:
            request = self.pending_rides[request_id]
            
            if request['is_merged']:
                merged_ride = self._find_merged_ride(request_id)
                if merged_ride:
                    return self._format_merged_ride_status(merged_ride)
            
            return self._format_single_ride_status(request)
            
        return "Ride request not found."

    def _find_merged_ride(self, request_id):
        """
        Find the merged ride containing this request.
        """
        for merged_id, ride in self.active_rides.items():
            if any(req['request_id'] == request_id for req in ride['requests']):
                return ride
        return None

    def _format_merged_ride_status(self, merged_ride):
        """
        Format the status message for a merged ride.
        """
        passengers = [
            self.user_mgmt.get_user_by_id(req['user_id'])['name']
            for req in merged_ride['requests']
        ]
        
        return {
            'status': 'merged',
            'passengers': passengers,
            'pickup': merged_ride['pickup_location'],
            'dropoff': merged_ride['dropoff_location'],
            'total_fare': merged_ride['total_fare'],
            'split_fare': merged_ride['split_fare'],
            'timestamp': datetime.fromtimestamp(merged_ride['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
        }

    def _format_single_ride_status(self, request):
        """
        Format the status message for a single ride.
        """
        return {
            'status': request['status'],
            'pickup': request['pickup_location'],
            'dropoff': request['dropoff_location'],
            'timestamp': datetime.fromtimestamp(request['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
        }

    def display_ride_status(self, request_id):
        """
        Display formatted ride status in the terminal.
        """
        status = self.get_ride_status(request_id)
        
        if isinstance(status, dict):
            if status['status'] == 'merged':
                print("\n=== Shared Ride Status ===")
                print(f"Passengers: {', '.join(status['passengers'])}")
                print(f"Pickup: {status['pickup']}")
                print(f"Dropoff: {status['dropoff']}")
                print(f"Total Fare: ${status['total_fare']:.2f}")
                print(f"Split Fare (per person): ${status['split_fare']:.2f}")
                print(f"Requested at: {status['timestamp']}")
            else:
                print("\n=== Ride Status ===")
                print(f"Status: {status['status']}")
                print(f"Pickup: {status['pickup']}")
                print(f"Dropoff: {status['dropoff']}")
                print(f"Requested at: {status['timestamp']}")
        else:
            print(status)

    def get_pending_rides(self):
        """Retrieve all pending rides."""
        # Reload pending rides to get the latest state
        self.pending_rides = self.load_pending_rides()
        # Filter to return only rides that are pending
        return {
            req_id: ride for req_id, ride in self.pending_rides.items() 
            if ride.get('status') == 'pending'
        }


    def accept_social_ride(self, driver_id):
        pending_social_rides = self.get_pending_rides()
        
        # Filter to get only merged rides
        merged_rides = [
            ride for ride in pending_social_rides.values() 
            if ride.get('status') == 'pending' and 
            any(req.get('is_merged') for req in ride.get('requests', []))
        ]
        
        if not merged_rides:
            print("\nNo social ride requests available.")
            return
        
        print("\n--- Pending Social Ride Requests ---")
        for idx, ride in enumerate(merged_rides, start=1):
            print(f"{idx}. Ride from {ride['pickup_location']} to {ride['dropoff_location']}")
            # Display the names of all users in the merged ride
            user_names = ', '.join(req['user_name'] for req in ride['requests'])
            print(f"   Requested by: {user_names}")
            print(f"   Request ID: {ride['merged_id']}")
        
        choice = input("Enter the number of the ride to accept (0 to cancel): ")
        
        try:
            idx = int(choice)
            if idx == 0:
                return
            selected_ride = merged_rides[idx - 1]
            self._confirm_social_ride(driver_id, selected_ride)
        except ValueError:
            print("Invalid input.")
            
    def _confirm_social_ride(self, driver_id, ride):
        if ride['status'] != 'pending':
            print("Ride already accepted by another driver.")
            return
        
        ride['status'] = 'active'
        ride['driver_id'] = driver_id
        
        # Ensure active_rides is a dictionary
        if not isinstance(self.active_rides, dict):
            self.active_rides = {}
        
        # Store the ride in active rides as a dictionary
        self.active_rides[ride['merged_id']] = ride
        
        # Remove from pending rides and save to active rides
        del self.pending_rides[ride['merged_id']]  # Use merged_id to remove from pending rides
        self.save_pending_rides()
        
        # Convert active_rides to a list for saving to JSON
        active_rides_list = list(self.active_rides.values())
        save_data_to_file(active_rides_list, 'active_rides.json')
        
        self.driver_mgmt.update_driver_active_ride(driver_id, ride['merged_id'])
        
        print("Ride accepted successfully.")

        
    def get_active_merged_ride(self, driver_id):
        """Retrieve the active merged ride for a specific driver."""
        driver = self.driver_mgmt.get_driver_by_id(driver_id)
        
        if not driver or 'active_ride' not in driver or not driver['active_ride']:
            return None  # No active ride for this driver
        
        ride_id = driver['active_ride']
        active_ride = self.active_rides.get(ride_id)
        
        # Check if the active ride is a merged ride
        if active_ride and 'requests' in active_ride and len(active_ride['requests']) > 1:
            return active_ride  # Return the active merged ride
        
        return None  # Not a merged ride

    def complete_ride(self, driver_id):
        # Use the combined method to get the active merged ride
        active_ride = self.get_active_merged_ride(driver_id)

        if active_ride is None:
            print("No active merged rides to complete.")
            return

        # Check if the ride is assigned to the driver
        if active_ride.get('driver_id') != driver_id:
            print("This ride is not assigned to you.")
            return

        # Mark the ride as completed
        active_ride['status'] = 'completed'
        
        # Save the ride to history
        self.add_to_history(active_ride, driver_id)
        
        # Remove from active rides
        del self.active_rides[active_ride['merged_id']]
        self.save_active_rides()
        
        # Clear driver's active ride
        driver = self.driver_mgmt.get_driver_by_id(driver_id)
        driver['active_ride'] = None
        self.driver_mgmt.update_driver(driver)
        
        print("Ride completed and saved to history.")



    def add_to_history(self, ride, driver_id):
        ride_data = {
            'ride_id': ride['merged_id'],
            'driver_id': driver_id,
            'requests': ride['requests'],
            'pickup': ride['pickup_location'],
            'dropoff': ride['dropoff_location'],
            'fare': ride['total_fare'],
            'status': 'completed'
        }
        
        # Add to user and driver history
        for request in ride['requests']:
            user_id = request['user_id']
            user_history = self.get_user_ride_history(user_id)
            user_history.append(ride_data)
            save_data_to_file(user_history, f'user_history_{user_id}.json')
        
        driver_history = self.get_driver_ride_history(driver_id)
        driver_history.append(ride_data)
        save_data_to_file(driver_history, f'driver_history_{driver_id}.json')

    def display_friend_rides(self, user_id):
        """
        Display all available rides from friends in a formatted way.
        """
        friend_rides = self.find_friend_rides(user_id)
        
        if not friend_rides:
            print("\nNo available rides from friends at the moment.")
            return []
        
        print("\n=== Available Rides From Friends ===")
        for idx, ride in enumerate(friend_rides, 1):
            print(f"\nRide #{idx}")
            print(f"Friend: {ride['user_name']}")
            print(f"From: {ride['pickup_location']}")
            print(f"To: {ride['dropoff_location']}")
            print(f"Request ID: {ride['request_id']}")
            print("Status: Available for sharing")
            print("-" * 40)
        
        return friend_rides
    
    def get_shared_ride_history(self, user_id):
        """
        Get the shared ride history for a specific user.
        
        Args:
            user_id (str): The ID of the user
        Returns:
            list: List of shared rides the user has taken
        """
        try:
            # Load the ride history for all users
            history_file = f'users_data.json'
            user_data = load_data_from_file(history_file, dict) or {}

            shared_rides = []

            # Iterate over all users' ride history to find shared rides
            for user in user_data.values():
                user_history = user.get('ride_history', [])
                
                # Check for shared rides (rides with multiple passengers or merged rides)
                for ride in user_history:
                    # If the ride is a merged ride, check if the user is part of the merged requests
                    if 'merged_id' in ride:
                        for request in ride.get('requests', []):
                            if request['user_id'] == user_id:
                                shared_rides.append(ride)
                                break
                    elif len(ride.get('requests', [])) > 1:  # Normal shared ride with multiple passengers
                        shared_rides.append(ride)

            # Sort shared rides by the most recent first
            shared_rides.sort(key=lambda x: x.get('timestamp', 0), reverse=True)
            
            return shared_rides
        
        except Exception as e:
            print(f"Error loading ride history: {str(e)}")
            return []

        
    def display_shared_ride_history(self, user_id):
        """
        Display formatted shared ride history for a user.
        
        Args:
            user_id (str): The ID of the user
        """
        history = self.get_shared_ride_history(user_id)
        
        if not history:
            print("\nNo shared ride history found.")
            return
        
        print("\n=== Shared Ride History ===")
        for ride in history:
            print("\nRide Details:")
            print(f"From: {ride.get('pickup', 'Unknown')}")
            print(f"To: {ride.get('dropoff', 'Unknown')}")
            print(f"Shared with:")
            for request in ride.get('requests', []):
                if request['user_id'] != user_id:
                    friend = self.user_mgmt.get_user_by_id(request['user_id'])
                    friend_name = friend.get('name', 'Unknown') if friend else 'Unknown'
                    print(f"- {friend_name}")
            print(f"Fare: ${ride.get('fare', 0):.2f}")
            print(f"Status: {ride.get('status', 'Unknown')}")
            print("-" * 40)

    def find_friend_rides(self, user_id):
        """Find and return all available ride requests from friends."""
        # Reload pending rides to get latest state
        self.pending_rides = self.load_pending_rides()
        
        # Get list of friends
        friends_list = self.friend_mgmt.get_friends_list(user_id)
        if not friends_list:
            return []

        # Extract friend IDs
        friend_ids = [friend[0] for friend in friends_list]
        
        # Find all pending rides from friends
        friend_rides = []
        for req_id, ride in self.pending_rides.items():
            # Skip if ride doesn't have required fields
            if not isinstance(ride, dict):
                continue
                
            if not all(key in ride for key in ['user_id', 'status', 'is_merged']):
                continue
                
            if (ride['user_id'] in friend_ids and 
                ride['status'] == 'pending' and 
                not ride['is_merged']):
                friend_rides.append(ride)
        
        return friend_rides

    def view_and_accept_friend_rides(self, user_id):
        """
        View available friend ride requests and choose to accept or decline them.
        
        Args:
            user_id (str): The ID of the user viewing friend rides
            
        Returns:
            tuple: (bool, str) Success status and message
        """
        # Reload pending rides to get latest state
        self.pending_rides = self.load_pending_rides()
        
        # Get and display available friend rides
        friend_rides = self.find_friend_rides(user_id)
        
        if not friend_rides:
            print("\nNo available rides from friends at the moment.")
            return False, "No available rides found."
        
        print("\n=== Available Rides From Friends ===")
        for idx, ride in enumerate(friend_rides, 1):
            print(f"\nRide #{idx}")
            print(f"Friend: {ride['user_name']}")
            print(f"From: {ride['pickup_location']}")
            print(f"To: {ride['dropoff_location']}")
            print(f"Request ID: {ride['request_id']}")
            print("-" * 40)
        
        while True:
            try:
                choice = input("\nEnter ride number to accept (0 to cancel): ")
                choice = int(choice)
                
                if choice == 0:
                    return False, "Operation cancelled."
                    
                if choice < 1 or choice > len(friend_rides):
                    print("Invalid ride number. Please try again.")
                    continue
                    
                selected_ride = friend_rides[choice - 1]
                
                # Verify the ride still exists and is available
                if selected_ride['request_id'] not in self.pending_rides:
                    return False, "This ride is no longer available."
                    
                # Confirm with user
                confirm = input(f"\nConfirm joining ride with {selected_ride['user_name']} (y/n)? ").lower()
                
                if confirm != 'y':
                    return False, "Ride join cancelled."
                
                # Create a new ride request for the joining user
                request = {
                    'request_id': f"req_{int(time.time())}_{user_id}",
                    'user_id': user_id,
                    'user_name': self.user_mgmt.get_user_by_id(user_id)['name'],
                    'pickup_location': selected_ride['pickup_location'],
                    'dropoff_location': selected_ride['dropoff_location'],
                    'timestamp': time.time(),
                    'status': 'pending',
                    'matched_with': None,
                    'is_merged': False
                }
                
                # Store the request
                self.pending_rides[request['request_id']] = request
                
                # Merge with friend's ride
                merged_ride = self._merge_rides(request, selected_ride)
                self.save_pending_rides()
                
                return True, f"Successfully joined ride with {selected_ride['user_name']}"
                
            except ValueError:
                print("Invalid input. Please enter a number.")
            except Exception as e:
                print(f"An error occurred: {str(e)}")
                return False, "An error occurred while processing your request."




        

