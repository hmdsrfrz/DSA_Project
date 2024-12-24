#main.py
import threading
import networkx as nx
import matplotlib.pyplot as plt
from user_management import UserManagement
from driver_management import DriverManagement
from friend_management import FriendManagement
from ride_request import RideRequest
from location_service import LocationService
from emergency_handler import EmergencyHandler
from social_rideshare import SocialRideshare
from pricing import Pricing
from ride_history import RideHistory
from map_data import IslamabadMap
from data_structures import Graph
from data_structures import HashTable
from polling import poll_file, reload_drivers, reload_users

from dashboards import Dashboards
from map_visualization import visualize_map, visualize_ride_path


def initialize_system():
    """Initialize all system components in the correct order"""
    # Initialize base services first
    map_data = IslamabadMap()
    location_service = LocationService(map_data)
    pricing = Pricing()
    
    # Initialize management systems
    user_mgmt = UserManagement()
    driver_mgmt = DriverManagement()
    friend_mgmt = FriendManagement(user_mgmt)
    ride_history = RideHistory()
    
    # Initialize ride request system with all required dependencies
    ride_request = RideRequest(
        user_management=user_mgmt,
        driver_management=driver_mgmt,
        location_service=location_service,
        pricing=pricing
    )
    
    # Initialize additional services that depend on core components
    emergency_handler = EmergencyHandler(ride_request, location_service, driver_mgmt)
    social_rideshare = SocialRideshare()
    
    # Initialize dashboard last as it depends on all other components
    dashboards = Dashboards(user_mgmt, driver_mgmt, ride_request, location_service, pricing, ride_history, emergency_handler, friend_mgmt)
    
    return {
        'user_mgmt': user_mgmt,
        'driver_mgmt': driver_mgmt,
        'location_service': location_service,
        'pricing': pricing,
        'ride_request': ride_request,
        'emergency_handler': emergency_handler,
        'social_rideshare': social_rideshare,
        'dashboards': dashboards,
        'ride_history': ride_history
    }

def main():

    # Initialize the system
    system = initialize_system()
    Dashboards = system['dashboards']

    # Start polling threads for user and driver data
    user_poll_thread = threading.Thread(target=poll_file, args=('users_data.json', reload_users), daemon=True)
    driver_poll_thread = threading.Thread(target=poll_file, args=('drivers_data.json', reload_drivers), daemon=True)
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
