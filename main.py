import threading

import networkx as nx
import matplotlib.pyplot as plt
from user_management import UserManagement
from driver_management import DriverManagement
from ride_request import RideRequest
from location_service import LocationService
from emergency_handler import EmergencyHandler
from social_rideshare import SocialRideshare
from pricing import Pricing
from ride_history import RideHistory
from map_data import IslamabadMap
from data_structures import Graph
from data_structures import HashTable
from polling import poll_file

from dashboards import Dashboards
from map_visualization import visualize_map, visualize_ride_path

# Initialize components
user_mgmt = UserManagement()
driver_mgmt = DriverManagement()
location_service = LocationService(IslamabadMap())
pricing = Pricing()
ride_history = RideHistory()
ride_request = RideRequest(user_mgmt, driver_mgmt)
emergency_handler = EmergencyHandler(ride_request, location_service, driver_mgmt)
social_rideshare = SocialRideshare()
dashboards = Dashboards()


# Import other required components...

def main():
    # Start polling threads for user and driver data
    user_poll_thread = threading.Thread(target=poll_file, args=('users_data.json', user_mgmt.users), daemon=True)
    driver_poll_thread = threading.Thread(target=poll_file, args=('drivers_data.json', driver_mgmt.drivers), daemon=True)
    user_poll_thread.start()
    driver_poll_thread.start()

    while True:
        try:
            print("\n--- Main Menu ---")
            print("1. User Login")
            print("2. Driver Login")
            print("3. User Signup")
            print("4. Driver Signup")
            print("5. Exit")
            
            choice = input("Enter your choice: ")
            
            if choice == '1':
                Dashboards.run_user_login()
            elif choice == '2':
                Dashboards.run_driver_login()
            elif choice == '3':
                Dashboards.run_user_signup()
            elif choice == '4':
                Dashboards.run_driver_signup()
            elif choice == '5':
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")
        except KeyboardInterrupt:
            print("\nProgram interrupted. Exiting gracefully.")
            break

if __name__ == "__main__":
    main()
