import json
from save_load import save_data_to_file, load_data_from_file

class RatingSystem:
    def __init__(self, ride_history_file):
        self.ride_history_file = ride_history_file
        self.ride_history = load_data_from_file(ride_history_file, list) or []
        self.drivers_data = load_data_from_file('drivers_data.json', dict) or {}

    def post_ride_feedback(self, user_id, rating, feedback):
        """
        Add feedback and rating to the most recent ride and update driver's ratings.
        
        Args:
            user_id (str): The ID of the user.
            rating (float): The rating given by the user (1-5).
            feedback (str): Additional feedback provided by the user.
        Returns:
            tuple: (success, message)
        """
        if not (1 <= rating <= 5):
            return False, "Rating must be between 1 and 5."
        
        # Find the most recent ride for the user
        user_rides = [ride for ride in self.ride_history if ride.get("user_id") == user_id]
        if not user_rides:
            return False, "No ride history found for the user."
        
        latest_ride = user_rides[-1]
        
        # Check if the ride is a merged ride
        if 'merged_id' in latest_ride:
            # Iterate through the requests in the merged ride
            for request in latest_ride['requests']:
                if request['user_id'] == user_id:
                    # Check if the ride already has feedback
                    if 'rating' in request and 'feedback' in request:
                        return False, "Your last merged ride has already been rated by you."
                    
                    # Update the matched request with feedback
                    request['rating'] = rating
                    request['feedback'] = feedback
                    
                    driver_id = latest_ride.get("driver_id")
                    if driver_id:
                        # Update driver's ratings
                        driver = self.drivers_data.get(driver_id)
                        if driver:
                            # Initialize feedback list if it doesn't exist
                            if 'feedback' not in driver:
                                driver['feedback'] = []

                            # Add new feedback
                            feedback_entry = {
                                'rating': rating,
                                'feedback': feedback,
                                'ride_id': latest_ride['merged_id'],
                                'user_id': user_id
                            }
                            driver['feedback'].append(feedback_entry)

                            # Recalculate average rating
                            total_ratings = len(driver['feedback'])
                            average_rating = sum(entry['rating'] for entry in driver['feedback']) / total_ratings

                            # Update driver attributes
                            driver['rating'] = round(average_rating, 2)
                            driver['total_ratings'] = total_ratings

                            # Save updated driver data
                            self.drivers_data[driver_id] = driver
                            save_data_to_file(self.drivers_data, 'drivers_data.json')

                            # Save updated ride history
                            save_data_to_file(self.ride_history, self.ride_history_file)
                            return True, "Feedback submitted successfully for your merged ride."
                        else:
                            return False, "Driver not found in database for merged ride."
                    else:
                        return False, "Driver ID not found in merged ride details."
        
        # For normal rides
        if "rating" in latest_ride and "feedback" in latest_ride:
            return False, "Your last ride has already been rated by you."
        
        driver_id = latest_ride.get("driver_id")
        
        if not driver_id:
            return False, "Driver ID not found in ride details."
        
        # Update ride history
        latest_ride["rating"] = rating
        latest_ride["feedback"] = feedback
        save_data_to_file(self.ride_history, self.ride_history_file)
        
        # Update driver's ratings in drivers_data.json
        if driver_id not in self.drivers_data:
            return False, "Driver not found in database."
        
        driver = self.drivers_data[driver_id]
        
        # Initialize feedback list if it doesn't exist
        if 'feedback' not in driver:
            driver['feedback'] = []
        
        # Add new feedback
        feedback_entry = {
            'rating': rating,
            'feedback': feedback,
            'ride_id': latest_ride['id'],
            'user_id': user_id
        }
        driver['feedback'].append(feedback_entry)
        
        # Recalculate average rating
        total_ratings = len(driver['feedback'])
        average_rating = sum(entry['rating'] for entry in driver['feedback']) / total_ratings
        
        # Update driver attributes
        driver['rating'] = round(average_rating, 2)
        driver['total_ratings'] = total_ratings
        
        # Save updated driver data
        self.drivers_data[driver_id] = driver
        save_data_to_file(self.drivers_data, 'drivers_data.json')
        
        return True, "Feedback submitted successfully and driver rating updated."

    def get_driver_feedback(self, driver_id):
        """
        Retrieve all feedback for a specific driver along with total rating.
        
        Args:
            driver_id (str): The ID of the driver.
        Returns:
            tuple: (list, float) containing feedback entries and total rating.
        """
        if driver_id not in self.drivers_data:
            return [], 0.0
            
        driver = self.drivers_data[driver_id]
        feedback_entries = driver.get('feedback', [])
        total_rating = driver.get('rating', 0.0)
        return feedback_entries, total_rating

    def calculate_driver_rating(self, driver_id):
        """
        Recalculate the driver's rating based on all feedback.
        
        Args:
            driver_id (str): The ID of the driver.
        Returns:
            float: The recalculated rating.
        """
        if driver_id not in self.drivers_data:
            return 0.0

        driver = self.drivers_data[driver_id]
        feedback = driver.get('feedback', [])
        total_ratings = len(feedback)
        
        if total_ratings == 0:
            return 0.0
            
        total_score = sum(entry['rating'] for entry in feedback)
        return round(total_score / total_ratings, 2)

    def reset_driver_ratings(self, driver_id):
        """
        Reset a driver's ratings and feedback.
        
        Args:
            driver_id (str): The ID of the driver.
        Returns:
            bool: True if successful, False otherwise.
        """
        if driver_id not in self.drivers_data:
            return False

        driver = self.drivers_data[driver_id]
        driver['rating'] = 0.0
        driver['total_ratings'] = 0
        driver['feedback'] = []
        
        self.drivers_data[driver_id] = driver
        save_data_to_file(self.drivers_data, 'drivers_data.json')
        return True