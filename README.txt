###############################################
#         RIDE MANAGEMENT SYSTEM              #
###############################################

===============================================
               OVERVIEW
===============================================
The Ride Management System is a Python-based 
application that provides a solution for ride 
management. It includes features like user 
and driver management, ride requests, 
emergency handling, map visualization, 
and friend management.

The system uses data structures such as 
graphs, hash tables, and queues to ensure 
efficient operations.

===============================================
               FEATURES
===============================================
1. USER MANAGEMENT
   - Signup and login functionality for users.
   - Session management and profile updates.

2. DRIVER MANAGEMENT
   - Driver registration and login.
   - Location and availability management.
   - Viewing and accepting ride requests.

3. RIDE MANAGEMENT
   - Request rides with specific pickup and 
     drop-off locations.
   - Emergency ride handling with priority 
     scheduling.
   - Visualizing ride paths using map data.

4. MAP & LOCATION SERVICES
   - Dynamic location management with 
     distance calculations.
   - Visualization of shortest paths and 
     connections.

5. FRIEND MANAGEMENT
   - Sending, accepting, and managing friend 
     requests.
   - Viewing friends and their profiles.

6. EMERGENCY SERVICES
   - Integration of hospitals and fire stations 
     into the map.
   - Emergency request prioritization and 
     nearest driver assignment.

===============================================
               SETUP INSTRUCTIONS
===============================================

1. CLONE THE PROJECT
   Download the project files and navigate to 
   the folder where they are stored.

2. INSTALL REQUIRED LIBRARIES
   Make sure Python 3.6+ is installed, then 
   install the required libraries:
   > pip install matplotlib networkx

3. DATA INITIALIZATION
   Prepare the following JSON files for user, 
   driver, and ride data:
   - `users_data.json`
   - `drivers_data.json`
   - `ride_history.json`

4. RUN THE APPLICATION
   Launch the program using:
   > python main.py

===============================================
               USAGE INSTRUCTIONS
===============================================

------ MAIN MENU ------
1. User Login
2. Driver Login
3. User Signup
4. Driver Signup
5. Exit

------ USER DASHBOARD ------
- Request rides and view ride history.
- Update location and manage friend requests.
- Book emergency rides.
- Visualize active ride paths.

------ DRIVER DASHBOARD ------
- Manage availability and update location.
- View and accept ride requests.
- Complete rides and synchronize data.

===============================================
               PROJECT STRUCTURE
===============================================

- `main.py`          : Entry point for the app.
- `dashboards.py`    : Handles user/driver UI.
- `data_structures.py`: Implements custom 
                        data structures.
- `driver_management.py`: Driver operations.
- `friend_management.py`: Manages friendships.
- `emergency_handler.py`: Emergency ride logic.
- `location_service.py`: Shortest path utilities.
- `map_data.py`       : Map locations and distances.

===============================================
               CONTACT
===============================================

For inquiries or issues, reach out to the 
project maintainer.

