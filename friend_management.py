# friend_management.py
from data_structures import HashTable
from save_load import save_data_to_file, load_data_from_file

class FriendManagement:
    def __init__(self, user_management, file_path='friend_data.json'):
        self.user_mgmt = user_management
        self.friend_requests = HashTable()  # Store pending friend requests
        self.friends_list = HashTable()     # Store accepted friends
        self.file_path = file_path

        # Load existing data from file
        data = load_data_from_file(self.file_path, dict) or {}
        self.friend_requests = HashTable.from_dict(data.get('friend_requests', {}))
        self.friends_list = HashTable.from_dict(data.get('friends_list', {}))

    def save_to_file(self):
        data = {
            'friend_requests': self.friend_requests.to_dict(),
            'friends_list': self.friends_list.to_dict()
        }
        save_data_to_file(data, self.file_path)

    def display_all_users(self):
        """Display all users with numbers for selection."""
        users = []
        for bucket in self.user_mgmt.users.table.values():
            if bucket:
                for user_id, user_data in bucket:
                    users.append((user_id, user_data))
        
        print("\n--- Available Users ---")
        for idx, (user_id, user_data) in enumerate(users, 1):
            print(f"{idx}. {user_data['name']} ({user_data['email']})")
        return users

    def send_friend_request(self, from_user_id, to_user_idx, users_list):
        """Send a friend request to selected user."""
        if to_user_idx < 1 or to_user_idx > len(users_list):
            return False, "Invalid user selection"
            
        to_user_id = users_list[to_user_idx - 1][0]
        print(f"Debug: Sending friend request to {to_user_id} from {from_user_id}")  # Debug

        # Validate and ensure correct user_id is used
        real_user_id = self.user_mgmt.active_sessions.get(from_user_id) or from_user_id
        
        # FIX: Check directly in user database instead of active_sessions
        if not self.user_mgmt.users.get(real_user_id):
            print("Error: User ID not found in user database.")
            return False, "Invalid user ID"
            
        if to_user_id == from_user_id:
            return False, "Cannot send friend request to yourself"
            
        # Check if already friends
        if self.are_friends(from_user_id, to_user_id):
            return False, "Already friends with this user"
            
        # Check if request already pending
        pending_requests = self.friend_requests.get(to_user_id) or []
        if from_user_id in pending_requests:
            return False, "Friend request already pending"
            
        # Store the friend request
        if not self.friend_requests.get(to_user_id):
            self.friend_requests.insert(to_user_id, [])
        pending_requests.append(from_user_id)
        self.friend_requests.insert(to_user_id, pending_requests)
        
        # Save immediately after sending request
        self.save_to_file()
        
        return True, "Friend request sent successfully"


    '''def get_pending_requests(self, user_id):
        """Get list of pending friend requests for a user."""
        pending_users = []
        print(f"Debug: Friend Requests Table: {self.friend_requests.to_dict()}")  # Debug statement
        print(f"Debug: Current User ID: {user_id}")  # Debug current user ID

        for bucket in self.friend_requests.table.values():
            if bucket:
                for to_user_id, from_user_list in bucket:
                    # Reverse lookup: Check if current user sent a request to this recipient
                    if user_id in from_user_list:
                        print(f"Debug: Match found for request sent by {user_id} to {to_user_id}")  # Confirm match
                        user_data = self.user_mgmt.get_user_by_id(to_user_id)
                        if user_data:
                            pending_users.append((to_user_id, user_data))
        
        return pending_users
        #this function used to show you the requests that you have sent to other users
        # say you logged in as hh, it shows the requests you as hh sent to others. not what others sent to you'''
    
    def get_pending_requests(self, user_id):
        """Get list of pending friend requests for a user."""
        pending_users = []
        requests_dict = self.friend_requests.to_dict()  # Get the dictionary representation
        print(f"Debug: Friend Requests Table: {requests_dict}")
        print(f"Debug: Current User ID: {user_id}")
        
        # Use the dictionary you just retrieved
        for to_user_id, from_user_list in requests_dict.items():
            if to_user_id == user_id:  # Look for incoming requests
                print(f"Debug: Match found for pending request to {user_id}")
                for from_user_id in from_user_list:
                    # Fetch user data
                    print(f"Debug: UserManagement internal data: {self.user_mgmt.__dict__}")  # This will show us the internal state
                    print(f"Debug: Type of user_mgmt: {type(self.user_mgmt)}")
                    user_data = self.user_mgmt.get_user_by_id(from_user_id)
                    print(f"Debug: Fetched user data for {from_user_id}: {user_data}")
                    if user_data:  # If valid user data is returned
                        pending_users.append((from_user_id, user_data))
                    else:
                        print(f"Debug: No user data found for {from_user_id}")
    
        # Debug statement to check the final list
        print(f"Debug: Pending Users: {pending_users}")
        return pending_users





    def accept_friend_request(self, user_id, from_user_idx, pending_requests):
        """Accept a friend request."""
        if from_user_idx < 1 or from_user_idx > len(pending_requests):
            return False, "Invalid selection"
        
        # Identify the sender of the request
        from_user_id = pending_requests[from_user_idx - 1][0]
        print(f"Debug: Accepting request from {from_user_id} for user {user_id}")

        # Add each user to the other's friend list
        if not self.friends_list.get(user_id):
            self.friends_list.insert(user_id, [])
        if not self.friends_list.get(from_user_id):
            self.friends_list.insert(from_user_id, [])

        # Update friend lists for both users
        user_friends = self.friends_list.get(user_id)
        from_user_friends = self.friends_list.get(from_user_id)
        
        if from_user_id not in user_friends:
            user_friends.append(from_user_id)
        if user_id not in from_user_friends:
            from_user_friends.append(user_id)
        
        self.friends_list.insert(user_id, user_friends)
        self.friends_list.insert(from_user_id, from_user_friends)

        # Remove the accepted request from pending requests
        pending_requests = self.friend_requests.get(user_id)
        pending_requests.remove(from_user_id)
        self.friend_requests.insert(user_id, pending_requests)
        
        # Save changes immediately
        self.save_to_file()

        return True, "Friend request accepted successfully"


    def are_friends(self, user_id1, user_id2):
        """Check if two users are friends."""
        user1_friends = self.friends_list.get(user_id1) or []
        return user_id2 in user1_friends

    def get_friends_list(self, user_id):
        """Get list of friends for a user."""
        friends = self.friends_list.get(user_id) or []
        friend_users = []
        
        for friend_id in friends:
            user_data = self.user_mgmt.get_user_by_id(friend_id)
            if user_data:
                friend_users.append((friend_id, user_data))
                
        return friend_users
