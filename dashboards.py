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
    def __init__(self, user_mgmt, driver_mgmt, ride_request, location_service, pricing, ride_history, emergency_handler, friend_mgmt, islamabad_map):
        self.user_mgmt = user_mgmt
        self.driver_mgmt = driver_mgmt
        self.ride_request = ride_request
        self.location_service = location_service
        self.pricing = pricing
        self.ride_history = ride_history
        self.emergency_handler = emergency_handler
        self.friend_mgmt = friend_mgmt
        self.islamabad_map = islamabad_map

    def run_user_login(self):
        email = input("Enter email: ")
        password = input("Enter password: ")

        success, session_id = self.user_mgmt.login_user(email, password)
        if success:
            user_id = self.user_mgmt.active_sessions.get(session_id)
            if not user_id:
                print("Error: Unable to resolve user ID from session.")
                return
            print("Login successful!")
            print("User ID after login:", user_id)
            self.user_dashboard(user_id)  # Pass user ID to the dashboard
        else:
            print("Invalid login details, please try again.")




    def run_user_signup(self):
        print("\n--- User Signup ---")
        name = input("Enter your name: ")
        email = input("Enter email: ")
        phone = input("Enter phone number: ")
        password = input("Enter password: ")

        success, result = self.user_mgmt.register_user(name, email, phone, password)
        if success:
            print(f"Signup successful! Your user ID is {result}")
            print("Redirecting to login...")
            self.run_user_login()
        else:
            print(result)

    # Helper methods for user_dashboard

    def _request_ride(self, user_id):
        print("\n--- Request a Ride ---")
        locations = self.islamabad_map.get_all_locations()
        for idx, location in enumerate(locations, start=1):
            print(f"{idx}. {location}")

        try:
            pickup_idx = int(input("Enter the number for your pickup location: "))
            destination_idx = int(input("Enter the number for your destination: "))

            if not (1 <= pickup_idx <= len(locations)) or not (1 <= destination_idx <= len(locations)):
                print("Invalid location numbers. Try again.")
                return

            pickup = locations[pickup_idx - 1]
            destination = locations[destination_idx - 1]

            if pickup == destination:
                print("Pickup and destination cannot be the same.")
                return

            success, ride_id = self.ride_request.request_ride(user_id, pickup, destination)
            if success:
                print(f"Ride successfully requested! Ride ID: {ride_id}")
                self.islamabad_map.visualize_ride_path(pickup, destination)
            else:
                print("Failed to request ride. Try again later.")

        except ValueError:
            print("Invalid input. Please enter valid numbers.")


    def _view_ride_history(self, user_id):
        print("\n--- Ride History ---")
        history = self.ride_history.get_ride_history(user_id)
        if not history:
            print("No ride history found.")
        else:
            for ride in history:
                print(ride)


    def _update_current_location(self, user_id):
        print("\n--- Update Current Location ---")
        locations = self.islamabad_map.get_all_locations()
        for idx, location in enumerate(locations, start=1):
            print(f"{idx}. {location}")

        try:
            location_idx = int(input("Enter the number for your current location: "))
            if not (1 <= location_idx <= len(locations)):
                print("Invalid location number.")
                return

            location = locations[location_idx - 1]
            if self.islamabad_map.is_valid_location(location):
                self.user_mgmt.update_user_profile(user_id, {'location': location})
                print("Location updated successfully.")
            else:
                print("Invalid location.")

        except ValueError:
            print("Invalid input. Please enter a valid number.")


    def _book_emergency_ride(self, user_id):
        print("\n--- Book Emergency Ride ---")
        locations = self.islamabad_map.get_all_locations()
        for idx, location in enumerate(locations, start=1):
            print(f"{idx}. {location}")

        try:
            pickup_idx = int(input("Enter the number for your pickup location: "))
            destination_idx = int(input("Enter the number for your emergency destination: "))

            if not (1 <= pickup_idx <= len(locations)) or not (1 <= destination_idx <= len(locations)):
                print("Invalid location numbers. Try again.")
                return

            pickup = locations[pickup_idx - 1]
            destination = locations[destination_idx - 1]

            if pickup == destination:
                print("Pickup and destination cannot be the same.")
                return

            success, ride_id = self.emergency_handler.add_emergency_request(user_id, pickup, destination)
            if success:
                print(f"Emergency ride booked successfully! Ride ID: {ride_id}")
                self.islamabad_map.visualize_ride_path(pickup, destination)
            else:
                print("Failed to book emergency ride.")

        except ValueError:
            print("Invalid input. Please enter valid numbers.")


    def _view_friends(self, user_id):
        print("\n--- Your Friends ---")
        friends = self.friend_mgmt.get_friends_list(user_id)
        if not friends:
            print("You have no friends added.")
        else:
            for idx, (friend_id, friend_data) in enumerate(friends, 1):
                print(f"{idx}. {friend_data['name']} ({friend_data['email']})")


    def _add_friend(self, user_id):
        print("\n--- Add a Friend ---")
        users = self.friend_mgmt.display_all_users()
        if not users:
            print("No users available to add as friends.")
            return

        try:
            friend_idx = int(input("Enter the number of the user to send a friend request: "))
            if not (1 <= friend_idx <= len(users)):
                print("Invalid user number.")
                return

            success, message = self.friend_mgmt.send_friend_request(user_id, friend_idx, users)
            print(message)

        except ValueError:
            print("Invalid input. Please enter a valid number.")


    def _view_friend_requests(self, user_id):
        print("\n--- Pending Friend Requests ---")
        pending_requests = self.friend_mgmt.get_pending_requests(user_id)
        if not pending_requests:
            print("You have no pending friend requests.")
        else:
            for idx, (from_id, from_user) in enumerate(pending_requests, 1):
                print(f"{idx}. {from_user['name']} ({from_user['email']})")

            try:
                request_idx = int(input("Enter the number of the request to accept (or 0 to skip): "))
                if request_idx == 0:
                    return

                if not (1 <= request_idx <= len(pending_requests)):
                    print("Invalid request number.")
                    return

                success, message = self.friend_mgmt.accept_friend_request(user_id, request_idx, pending_requests)
                print(message)

            except ValueError:
                print("Invalid input. Please enter a valid number.")


    def _visualize_map(self):
        print("\n--- Map Visualization ---")
        self.islamabad_map.visualize_map()



    def user_dashboard(self, user_id):
        """
        User dashboard to manage ride requests, history, friends, and other actions.
        """
        # Validate the user
        user_data = self.user_mgmt.get_user_by_id(user_id)
        if not user_data:
            print("Error: User not found. Please log in again.")
            return

        print(f"Welcome to your Dashboard, {user_data['name']}! (User ID: {user_id})")

        while True:
            # Display the dashboard menu
            print("\n--- User Dashboard ---")
            print("1. Request Ride")
            print("2. View Ride History")
            print("3. Select Current Location")
            print("4. Book Emergency Ride")
            print("5. View Friends")
            print("6. Add a Friend")
            print("7. View Friend Requests")
            print("8. Visualize Map")
            print("9. Logout")
            print("10. See Available Drivers")
            print("11. Provide Feedback")
            print("12. Visualize Last Ride Path")

            choice = input("Enter your choice: ")

            if choice == '1':
                self._request_ride(user_id)

            elif choice == '2':
                self._view_ride_history(user_id)

            elif choice == '3':
                self._update_current_location(user_id)

            elif choice == '4':
                self._book_emergency_ride(user_id)

            elif choice == '5':
                self._view_friends(user_id)

            elif choice == '6':
                self._add_friend(user_id)

            elif choice == '7':
                self._view_friend_requests(user_id)

            elif choice == '8':
                self._visualize_map()

            elif choice == '9':
                print("Logging out...")
                break

            elif choice == '10':
                self.see_available_drivers()

            elif choice == '11':
                self.user_mgmt.provide_feedback(user_id)

            elif choice == '12':
                self.user_mgmt.visualize_last_active_ride_path(user_id)

            else:
                print("Invalid choice. Please try again.")

