import threading
import time
import os
import networkx as nx
import matplotlib.pyplot as plt
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

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

class Dashboards:

    def run_user_login():
        print("\n--- User Login ---")
        email = input("Enter email: ")
        password = input("Enter password: ")

        success, result = user_mgmt.login_user(email, password)
        if success:
            session_id = result
            print("Login successful!")
            Dashboards.user_dashboard(session_id)  # Pass session_id to access the dashboard
        else:
            print(result)  # Print error message from login failure

    def run_user_signup():
        print("\n--- User Signup ---")
        name = input("Enter your name: ")
        email = input("Enter email: ")
        phone = input("Enter phone number: ")
        password = input("Enter password: ")

        success, result = user_mgmt.register_user(name, email, phone, password)
        if success:
            user_mgmt.users.save_to_file('users_data.json')
            print(f"Signup successful! Your user ID is {result}")
            Dashboards.run_user_login()  # After successful signup, redirect to login
        else:
            print(result)  # Print error message from signup failure

    def user_dashboard(user_id):
        while True:
            print("\n--- User Dashboard ---")
            print("1. Request Ride")
            print("2. View Ride History")
            print("3. Select Location")
            print("4. Book Emergency Ride")
            print("5. View Rideshare Connections")
            print("6. Add Rideshare Connection")
            print("7. Visualize Map")
            print("8. Logout")

            choice = input("Enter your choice: ")

            if choice == '1':
                # Create an instance of IslamabadMap
                islamabad_map = IslamabadMap()
                all_locations = islamabad_map.get_all_locations()

                print("\n--- Available Locations ---")
                for idx, location in enumerate(all_locations, start=1):
                    print(f"{idx}. {location}")

                # Prompt the user to select pickup and destination locations
                try:
                    pickup_index = int(input("Enter the number for your pickup location: "))
                    destination_index = int(input("Enter the number for your destination: "))
                    
                    # Validate user input
                    if pickup_index < 1 or pickup_index > len(all_locations) or destination_index < 1 or destination_index > len(all_locations):
                        print("Invalid selection. Please choose valid location numbers.")
                        return

                    pickup = all_locations[pickup_index - 1]
                    destination = all_locations[destination_index - 1]

                    # Ensure pickup and destination are not the same
                    if pickup == destination:
                        print("Pickup and destination locations cannot be the same. Please try again.")
                        return

                    # Validate the locations and proceed with the ride request
                    if islamabad_map.is_valid_location(pickup) and islamabad_map.is_valid_location(destination):
                        success, ride_id = ride_request.request_ride(user_id, pickup, destination)
                        if success:
                            print("Ride requested successfully. Ride ID:", ride_id)
                            visualize_ride_path(islamabad_map, pickup, destination)
                        else:
                            print("Failed to request ride.")
                    else:
                        print("Invalid locations. Please try again.")
                except ValueError:
                    print("Invalid input. Please enter numbers corresponding to the locations.")

            elif choice == '2':
                history = ride_history.get_ride_history()
                print("--- Ride History ---")
                for ride in history:
                    print(ride)
            elif choice == '3':
                # Create an instance of IslamabadMap
                islamabad_map = IslamabadMap()
                location = input("Select your current location: ")

                # Validate the location using IslamabadMap
                if islamabad_map.is_valid_location(location):
                    user_mgmt.update_user_profile(user_id, {'location': location})
                    print("Location updated.")
                else:
                    print("Invalid location. Please select a valid location from the available options.")

            elif choice == '4':
                # Create an instance of IslamabadMap
                islamabad_map = IslamabadMap()
                all_locations = islamabad_map.get_all_locations()

                print("\n--- Available Locations ---")
                for idx, location in enumerate(all_locations, start=1):
                    print(f"{idx}. {location}")

                try:
                    # Prompt the user to select pickup and destination locations
                    pickup_index = int(input("Enter the number for your pickup location: "))
                    destination_index = int(input("Enter the number for your emergency destination: "))

                    # Validate user input
                    if pickup_index < 1 or pickup_index > len(all_locations) or destination_index < 1 or destination_index > len(all_locations):
                        print("Invalid selection. Please choose valid location numbers.")
                        return

                    pickup = all_locations[pickup_index - 1]
                    destination = all_locations[destination_index - 1]

                    # Ensure pickup and destination are not the same
                    if pickup == destination:
                        print("Pickup and destination locations cannot be the same. Please try again.")
                        return

                    # Validate the locations and proceed with the emergency request
                    if islamabad_map.is_valid_location(pickup) and islamabad_map.is_valid_location(destination):
                        success, ride_id = emergency_handler.add_emergency_request(user_id, pickup, destination)
                        if success:
                            print("Emergency ride booked successfully. Ride ID:", ride_id)
                            visualize_ride_path(islamabad_map, pickup, destination)
                        else:
                            print("Failed to book emergency ride.")
                    else:
                        print("Invalid locations. Please try again.")
                except ValueError:
                    print("Invalid input. Please enter numbers corresponding to the locations.")

            elif choice == '5':
                connections = social_rideshare.find_rideshare_partners(user_id, "", "")
                print("Potential rideshare partners:", connections)
            elif choice == '6':
                friend_id = input("Enter the ID of the friend to add as rideshare connection: ")
                social_rideshare.add_connection(user_id, friend_id)
                print("Rideshare connection added successfully.")
            elif choice == '7':
                visualize_map(location_service)
            elif choice == '8':
                print("Logging out...")
                break
            else:
                print("Invalid choice. Please try again.")

    def run_driver_login():
        print("\n--- Driver Login ---")
        email = input("Enter email: ")
        password = input("Enter password: ")

        success, result = driver_mgmt.login_driver(email, password)
        if success:
            driver_id = result
            print("Login successful!")
            Dashboards.driver_dashboard(driver_id)  # Pass driver_id to access the dashboard
        else:
            print(result)  # Print error message from login failure

    def run_driver_signup():
        print("\n--- Driver Signup ---")
        name = input("Enter your name: ")
        email = input("Enter email: ")
        phone = input("Enter phone number: ")
        password = input("Enter password: ")
        vehicle_type = input("Enter vehicle type: ")
        license_number = input("Enter license number: ")

        success, result = driver_mgmt.register_driver(name, email, phone, password, vehicle_type, license_number)
        if success:
            driver_mgmt.drivers.save_to_file('drivers_data.json')
            print(f"Signup successful! Your driver ID is {result}")
            Dashboards.run_driver_login()  # After successful signup, redirect to login
        else:
            print(result)  # Print error message from signup failure

    def driver_dashboard(driver_id):
        while True:
            print("\n--- Driver Dashboard ---")
            print("1. Toggle Availability")
            print("2. View Ride History")
            print("3. Update Location")
            print("4. Visualize Map")
            print("5. Logout")

            choice = input("Enter your choice: ")

            if choice == '1':
                status = input("Enter 'on' to be available or 'off' to go offline: ").lower()
                available = status == 'on'
                driver_mgmt.set_driver_availability(driver_id, available)
                print("Availability updated.")
            elif choice == '2':
                history = ride_history.get_ride_history()
                print("--- Ride History ---")
                for ride in history:
                    print(ride)
            elif choice == '3':
                # Create an instance of IslamabadMap
                islamabad_map = IslamabadMap()
                all_locations = islamabad_map.get_all_locations()

                print("\n--- Available Locations ---")
                for idx, location in enumerate(all_locations, start=1):
                    print(f"{idx}. {location}")

                try:
                    # Prompt the driver to select their current location
                    location_index = int(input("Enter the number for your current location: "))

                    # Validate user input
                    if location_index < 1 or location_index > len(all_locations):
                        print("Invalid selection. Please choose a valid location number.")
                        return

                    location = all_locations[location_index - 1]

                    # Validate the location and update the driver's location
                    if islamabad_map.is_valid_location(location):
                        driver_mgmt.update_driver_location(driver_id, location)
                        print("Location updated.")
                    else:
                        print("Invalid location. Please try again.")
                except ValueError:
                    print("Invalid input. Please enter a number corresponding to the locations.")
