from data_structures import DoublyLinkedList
from datetime import datetime
from save_load import save_data_to_file, load_data_from_file

class RideHistory:
    def __init__(self, file_path='ride_history.json'):
        """
        Initializes the RideHistory with data loaded from a file if it exists.
        """
        self.file_path = file_path
        self.ride_history = DoublyLinkedList()  # Initialize an empty DoublyLinkedList
        self.load_ride_history()  # Load existing ride history from the file

    def load_ride_history(self):
        """Load ride history from the JSON file into the doubly linked list."""
        try:
            rides = load_data_from_file(self.file_path)
            for ride in rides:
                self.ride_history.append(ride)  # Append each ride to the linked list
        except FileNotFoundError:
            print("Ride history file not found. Starting with an empty history.")
        except Exception as e:
            print(f"Error loading ride history: {e}")

    def add_ride(self, ride_data):
        """
        Adds a ride record to the user's ride history and saves the updated history to the file.
        """
        self.ride_history.append(ride_data)  # Append the new ride data to the linked list
        self.save_ride_history()  # Save the updated history to the file

    def save_ride_history(self):
        """Save the current ride history to the JSON file."""
        history = []
        current = self.ride_history.head
        while current:
            history.append(current.data)  # Collect all ride data from the linked list
            current = current.next
        save_data_to_file(history, self.file_path)  # Save to file

    def get_user_name(self, user_id):
        """
        Retrieve user name from user ID.
        """
        user_data = load_data_from_file('users_data.json', dict) or {}
        user = user_data.get(user_id, {})
        return user.get('name', 'Unknown User')

    def get_driver_name(self, driver_id):
        """
        Retrieve driver name from driver ID.
        """
        driver_data = load_data_from_file('drivers_data.json', dict) or {}
        driver = driver_data.get(driver_id, {})
        return driver.get('name', 'Unknown Driver')

    def get_user_ride_history(self, user_id):
        """
        Returns the list of all past rides for a specific user in a presentable format.
        """
        user_history = []
        current = self.ride_history.head
        ride_number = 1  # Initialize ride number

        while current:
            ride_data = current.data
            
            # If the ride is a merged ride, iterate through the requests
            if 'merged_id' in ride_data:
                # Check if this user is associated with the merged ride
                if any(request['user_id'] == user_id for request in ride_data.get('requests', [])):
                    # Get the other user in the merged ride
                    other_users = [
                        self.get_user_name(request['user_id'])
                        for request in ride_data.get('requests', []) 
                        if request['user_id'] != user_id
                    ]
                    
                    driver_name = self.get_driver_name(ride_data.get('driver_id', ''))
                    
                    ride_info = (
                        f"--- Merged Ride #{ride_number} ---\n"
                        f"Merged Ride ID: {ride_data.get('merged_id', 'N/A')}\n"
                        f"Pickup Location: {ride_data.get('pickup_location', 'N/A')}\n"
                        f"Dropoff Location: {ride_data.get('dropoff_location', 'N/A')}\n"
                        f"Status: {ride_data.get('status', 'Unknown')}\n"
                        f"Timestamp: {self.format_time(ride_data.get('timestamp', 0))}\n"
                        f"Driver: {driver_name}\n"
                        f"Shared with: {', '.join(other_users)}\n"
                        f"Total Fare: {ride_data.get('total_fare', 'N/A')}\n"
                        f"Split Fare: {ride_data.get('split_fare', 'N/A')}\n"
                    )
                    user_history.append(ride_info)
                    ride_number += 1
            
            else:  # Handle normal ride
                if ride_data.get('user_id') == user_id:
                    driver_name = self.get_driver_name(ride_data.get('driver_id', ''))
                    
                    ride_info = (
                        f"--- Ride #{ride_number} ---\n"
                        f"Ride ID: {ride_data.get('id', 'N/A')}\n"
                        f"Pickup Location: {ride_data.get('pickup_location', 'N/A')}\n"
                        f"Dropoff Location: {ride_data.get('dropoff_location', 'N/A')}\n"
                        f"Status: {ride_data.get('status', 'Unknown')}\n"
                        f"Start Time: {self.format_time(ride_data.get('start_time', 0))}\n"
                        f"End Time: {self.format_time(ride_data.get('end_time', 0))}\n"
                        f"Duration: {self.format_duration(ride_data.get('duration', 0))}\n"
                        f"Driver: {driver_name}\n"
                        f"Rating: {ride_data.get('rating', 'Not Rated')}\n"
                        f"Feedback: {ride_data.get('feedback', 'No Feedback')}\n"
                    )
                    user_history.append(ride_info)
                    ride_number += 1
            
            current = current.next

        return user_history if user_history else "No ride history found for this user."

    def get_driver_ride_history(self, driver_id):
        """
        Returns the list of all past rides for a specific driver in a presentable format.
        """
        driver_history = []
        current = self.ride_history.head
        ride_number = 1  # Initialize ride number

        while current:
            ride_data = current.data
            
            # Check if the ride belongs to the driver
            if ride_data.get('driver_id') == driver_id:
                # If the ride is a merged ride
                if 'merged_id' in ride_data:
                    # Get user names for merged ride
                    user_names = [
                        self.get_user_name(request.get('user_id', ''))
                        for request in ride_data.get('requests', [])
                    ]
                    
                    ride_info = (
                        f"--- Merged Ride #{ride_number} ---\n"
                        f"Merged Ride ID: {ride_data.get('merged_id', 'N/A')}\n"
                        f"Pickup Location: {ride_data.get('pickup_location', 'N/A')}\n"
                        f"Dropoff Location: {ride_data.get('dropoff_location', 'N/A')}\n"
                        f"Status: {ride_data.get('status', 'Unknown')}\n"
                        f"Timestamp: {self.format_time(ride_data.get('timestamp', 0))}\n"
                        f"Users: {', '.join(user_names)}\n"
                        f"Total Fare: {ride_data.get('total_fare', 'N/A')}\n"
                        f"Split Fare: {ride_data.get('split_fare', 'N/A')}\n"
                    )
                else:
                    # Get user name for individual ride
                    user_name = self.get_user_name(ride_data.get('user_id', ''))
                    
                    ride_info = (
                        f"--- Ride #{ride_number} ---\n"
                        f"Ride ID: {ride_data.get('id', 'N/A')}\n"
                        f"Pickup Location: {ride_data.get('pickup_location', 'N/A')}\n"
                        f"Dropoff Location: {ride_data.get('dropoff_location', 'N/A')}\n"
                        f"Status: {ride_data.get('status', 'Unknown')}\n"
                        f"Start Time: {self.format_time(ride_data.get('start_time', 0))}\n"
                        f"End Time: {self.format_time(ride_data.get('end_time', 0))}\n"
                        f"Duration: {self.format_duration(ride_data.get('duration', 0))}\n"
                        f"User: {user_name}\n"
                        f"Rating: {ride_data.get('rating', 'Not Rated')}\n"
                        f"Feedback: {ride_data.get('feedback', 'No Feedback')}\n"
                    )
                
                driver_history.append(ride_info)
                ride_number += 1
            
            current = current.next

        return driver_history if driver_history else None

    def format_time(self, timestamp):
        """Formats the timestamp (float) into a readable string."""
        dt_object = datetime.fromtimestamp(timestamp)
        return dt_object.strftime("%Y-%m-%d %H:%M:%S")


    def format_duration(self, duration):
        """Formats the duration into a readable string."""
        hours, remainder = divmod(duration, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours}h {minutes}m {seconds}s"

    def get_ride_history(self):
        """
        Returns the list of all past rides in chronological order.
        """
        history = []
        current = self.ride_history.head
        while current:
            history.append(current.data)  # Collect ride data
            current = current.next
        return history