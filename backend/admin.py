class AdminManager:
    def __init__(self, booking_manager):
        self.booking_manager = booking_manager
    
    def view_all_bookings(self):
        return self.booking_manager.bookings
    
    def confirm_booking(self, booking_id):
        for booking in self.booking_manager.bookings:
            if booking['id'] == booking_id:
                booking['status'] = 'confirmed'
                return True
        return False
