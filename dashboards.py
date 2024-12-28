import threading
import time
import os
import networkx as nx
import matplotlib.pyplot as plt
import sys
import traceback

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from user_management import UserManagement
from driver_management import DriverManagement
from ride_request import RideRequest
from location_service import LocationService
from emergency_handler import EmergencyHandler
from social_rideshare import SocialRideshare
from pricing import Pricing
from ride_history import RideHistory
from map_data import IslamabadMap, is_valid_location, LOCATIONS
from data_structures import Graph, HashTable
from map_visualization import visualize_map
from friend_management import FriendManagement
from save_load import save_data_to_file, load_data_from_file


class Dashboards:
    def __init__(self, user_mgmt, driver_mgmt, ride_request, location_service, pricing, ride_history, emergency_handler, friend_mgmt):
        self.user_mgmt = user_mgmt
        self.driver_mgmt = driver_mgmt
        self.ride_request = ride_request
        self.location_service = location_service
        self.pricing = pricing
        self.ride_history = ride_history
        self.emergency_handler = emergency_handler
        self.friend_mgmt = friend_mgmt

    def run_user_login(self):
        email = input("Enter email: ")
        password = input("Enter password: ")
        
        success, session_id = self.user_mgmt.login_user(email, password)
        if success:
            user_id = self.user_mgmt.active_sessions.get(session_id)  # Resolve user_id from session_id
            print("Login successful!")
            print("User ID after login:", user_id)
            self.user_dashboard(user_id)  # Pass correct user_id
        else:
            print("Invalid Login Details, Please try again.")


    def run_user_signup(self):
        print("\n--- User Signup ---")
        name = input("Enter your name: ")
        email = input("Enter email: ")
        phone = input("Enter phone number: ")
        password = input("Enter password: ")

        success, result = self.user_mgmt.register_user(name, email, phone, password)
        if success:
            save_data_to_file(self.user_mgmt.users, 'users_data.json')
            print(f"Signup successful! Your user ID is {result}")
            self.run_user_login()  # After successful signup, redirect to login
        else:
            print(result)  # Print error message from signup failure

    def user_dashboard(self, user_id):
        '''user_id = self.user_mgmt.get_user_by_session(user_id)
        if not user_id:
                print("Error: User ID not found for session.")
                return'''
            
                # Resolve session ID to actual user ID

        print("User ID in Dashboard:", user_id)
        while True:
            updates = self.ride_request.get_user_updates(user_id)
            if updates:
                if updates['type'] == 'ride_accepted':
                    print(f"\nRide accepted by driver {updates['driver']['name']}!")
                    print(f"Driver phone: {updates['driver']['phone']}")
                    print(f"Vehicle type: {updates['driver']['vehicle_type']}")

            print("\n--- User Dashboard ---")
            print("1. Request Ride")
            print("2. View Ride History")
            print("3. Select Location")
            print("4. Book Emergency Ride")
            print("5. View Friends")
            print("6. Add Friend")
            print("7. View Friend Requests")
            print("8. Visualize Map")
            print("9. Logout")
            print("10. See available drivers")
            print("11. Provide Feedback")
            print("12. Visualize Last Active Ride Path")

            choice = input("Enter your choice: ")

            if choice == '1':
                # Create an instance of IslamabadMap
                islamabad_map = IslamabadMap()
                all_locations = islamabad_map.get_all_locations()

                print("\n--- Available Locations ---")
                for idx, location in enumerate(all_locations, start=1):
                    print(f"{idx}. {location}")

                try:
                    # Prompt the user to select pickup and destination locations
                    pickup_index = int(input("Enter the number for your pickup location: "))
                    destination_index = int(input("Enter the number for your destination: "))

                    # Validate user input
                    if pickup_index < 1 or pickup_index > len(all_locations) or destination_index < 1 or destination_index > len(all_locations):
                        print("Invalid selection. Please choose valid location numbers.")
                        continue  # Continue to the next iteration of the loop

                    pickup = all_locations[pickup_index - 1]
                    destination = all_locations[destination_index - 1]

                    # Ensure pickup and destination are not the same
                    if pickup == destination:
                        print("Pickup and destination locations cannot be the same. Please try again.")
                        continue  # Continue to the next iteration of the loop

                    # Validate the locations and proceed with the ride request
                    if is_valid_location(pickup) and is_valid_location(destination):
                        success, ride_id = self.ride_request.request_ride(user_id, pickup, destination)
                        if success:
                            print("Ride requested successfully. Ride ID:", ride_id)
                            try:
                                islamabad_map.visualize_ride_path(pickup, destination)
                            except Exception as e:
                                print(f"Error visualizing path: {e}")
                                traceback.print_exc()
                        else:
                            print("Failed to request ride.")
                    else:
                        print("Invalid locations. Please try again.")
                except ValueError:
                    print("Invalid input. Please enter numbers corresponding to the locations.")

            elif choice == '2':
                history = self.ride_history.get_ride_history()
                print("--- Ride History ---")
                for ride in history:
                    print(ride)
            elif choice == '3':
                # Create an instance of IslamabadMap
                islamabad_map = IslamabadMap()
                location = input("Select your current location: ")

                # Validate the location using IslamabadMap
                if is_valid_location(location):
                    self.user_mgmt.update_user_profile(user_id, {'location': location})
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
                        continue  # Continue to the next iteration of the loop

                    pickup = all_locations[pickup_index - 1]
                    destination = all_locations[destination_index - 1]

                    # Ensure pickup and destination are not the same
                    if pickup == destination:
                        print("Pickup and destination locations cannot be the same. Please try again.")
                        continue  # Continue to the next iteration of the loop

                    # Validate the locations and proceed with the emergency request
                    if is_valid_location(pickup) and is_valid_location(destination):
                        success, ride_id = self.emergency_handler.add_emergency_request(user_id, pickup, destination)
                        if success:
                            print("Emergency ride booked successfully. Ride ID:", ride_id)
                            islamabad_map.visualize_ride_path(self.location_service, pickup, destination)
                        else:
                            print("Failed to book emergency ride.")
                    else:
                        print("Invalid locations. Please try again.")
                except ValueError:
                    print("Invalid input. Please enter numbers corresponding to the locations.")

            elif choice == '5':
                friends = self.friend_mgmt.get_friends_list(user_id)
                print("\n--- Your Friends ---")
                for idx, (friend_id, friend_data) in enumerate(friends, 1):
                    print(f"{idx}. {friend_data['name']} ({friend_data['email']})")

            elif choice == '6':
                users = self.friend_mgmt.display_all_users()
                if users:
                    choice = input("\nEnter the number of the user to add: ")
                    try:
                        idx = int(choice)
                        success, message = self.friend_mgmt.send_friend_request(user_id, idx, users)
                        print(message)
                    except ValueError:
                        print("Invalid input")

            elif choice == '7':
                pending_requests = self.friend_mgmt.get_pending_requests(user_id)
                if not pending_requests:
                    print("No pending friend requests")
                else:
                    print("\n--- Pending Friend Requests ---")
                    for idx, (from_id, from_user) in enumerate(pending_requests, 1):
                        print(f"{idx}. {from_user['name']} ({from_user['email']})")
                    choice = input("\nEnter request number to accept (or 0 to skip): ")
                    try:
                        idx = int(choice)
                        if idx > 0:
                            success, message = self.friend_mgmt.accept_friend_request(
                                user_id, idx, pending_requests)
                            print(message)
                    except ValueError:
                        print("Invalid input")
                        
            elif choice == '8':
                visualize_map(self.location_service)
            elif choice == '10':
                 self.see_available_drivers()
            elif choice == '9':
                print("Logging out...")
                break
            elif choice == '11':
                self.user_mgmt.provide_feedback(user_id)

            elif choice == '12':
                self.user_mgmt.visualize_last_active_ride_path(user_id)
            else:
                print("Invalid choice. Please try again.")

    def see_available_drivers(self):
        print("\n--- Available Drivers ---")
        available_drivers = self.driver_mgmt.get_available_drivers()
        if not available_drivers:
            print("No drivers are currently available.")
            return

        for idx, driver in enumerate(available_drivers, 1):
            print(f"\nDriver {idx}:")
            print(f"Name: {driver['name']}")
            print(f"Vehicle Type: {driver['vehicle_type']}")
            print(f"Current Location: {driver.get('current_location', 'Unknown')}")
            print(f"Availability: {driver.get('availability', 'Not Set')}")


    def run_driver_login(self):
        print("\n--- Driver Login ---")
        email = input("Enter email: ")
        password = input("Enter password: ")

        success, result = self.driver_mgmt.login_driver(email, password)
        if success:
            driver_id = result
            print("Login successful!")
            self.driver_dashboard(driver_id)  # Pass driver_id to access the dashboard
        else:
            print(result)  # Print error message from login failure

    def run_driver_signup(self):
        print("\n--- Driver Signup ---")
        name = input("Enter your name: ")
        email = input("Enter email: ")
        phone = input("Enter phone number: ")
        password = input("Enter password: ")
        vehicle_type = input("Enter vehicle type: ")
        license_number = input("Enter license number: ")

        success, result = self.driver_mgmt.register_driver(name, email, phone, password, vehicle_type, license_number)
        if success:
            save_data_to_file(self.driver_mgmt.drivers,'drivers_data.json')
            print(f"Signup successful! Your driver ID is {result}")
            self.run_driver_login()  # After successful signup, redirect to login
        else:
            print(result)  # Print error message from signup failure

    

    def driver_dashboard(self, driver_id):
        while True:
            print("\n--- Driver Dashboard ---")
            print("1. Toggle Availability")
            print("2. View Ride History")
            print("3. Update Location")
            print("4. View Available Requests")
            print("5. Complete Ride")
            print("6. Visualize Map")
            print("7. Logout")
            print("8. See available drivers")
            print("9. Synchronize Ride Requests")

            choice = input("Enter your choice: ")

            if choice == '1':
                status = input("Enter 'on' to be available or 'off' to go offline: ").lower()
                available = status == 'on'
                self.driver_mgmt.set_driver_availability(driver_id, available)
                print("Availability updated.")
            elif choice == '2':
                history = self.ride_history.get_ride_history()
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
                        continue  # Continue to the next iteration of the loop

                    location = all_locations[location_index - 1]

                    # Validate the location and update the driver's location
                    if is_valid_location(location):
                        self.driver_mgmt.update_driver_location(driver_id, location)
                        print("Location updated.")
                    else:
                        print("Invalid location. Please try again.")
                except ValueError:
                    print("Invalid input. Please enter a number corresponding to the locations.")

            elif choice == '4':
                # Ensure driver location is updated
                driver = self.driver_mgmt.get_driver_by_id(driver_id)
                if not driver['current_location']:
                    print("Please update your location first.")
                    continue

                # Call the view_ride_requests function to display and handle requests
                self.driver_mgmt.view_ride_requests(driver_id)

            elif choice == '5':
                driver = self.driver_mgmt.get_driver_by_id(driver_id)
                print(driver)
                if not driver['active_ride']:
                    print("You don't have any active rides.")
                    continue

                ride_id = driver['active_ride']
                success, message = self.ride_request.complete_ride(ride_id)
                print(message)

            elif choice == '6':
                visualize_map(self.location_service)

            elif choice == '7':
                print("Logging out...")

            elif choice == '8':
                 self.see_available_drivers()
                 break
            elif choice == '9':
                self.driver_mgmt.sync_active_rides_with_drivers(driver_id)

            else:
                print("Invalid choice. Please try again.")