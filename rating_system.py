from save_load import save_data_to_file, load_data_from_file
class RatingSystem:
    def __init__(self, driver_management):
        self.driver_mgmt = driver_management

    def post_ride_feedback(self, driver_id, ride_id, rating, feedback=""):
        if rating < 1 or rating > 5:
            return False, "Rating must be between 1 and 5"

        driver = self.driver_mgmt.get_driver_by_id(driver_id)
        if not driver:
            return False, "Driver not found"

        # Update driver's rating
        total_ratings = driver['total_ratings']
        current_rating = driver['rating']

        new_total = total_ratings + 1
        new_rating = ((current_rating * total_ratings) + rating) / new_total

        driver['rating'] = round(new_rating, 2)
        driver['total_ratings'] = new_total

        # Add feedback
        if 'feedback' not in driver:
            driver['feedback'] = []
        driver['feedback'].append({
            'ride_id': ride_id,
            'rating': rating,
            'feedback': feedback
        })

        # Save updated driver data
        self.driver_mgmt.drivers.insert(driver_id, driver)
        save_data_to_file(self.driver_mgmt, 'drivers_data.json')

        return True, "Feedback submitted successfully"
