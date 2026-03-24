class BookingManager:
    def __init__(self):
        self.bookings = []
        self.next_id = 1
    
    def create_booking(self, table_id, customer_name, date, time):
        booking = {
            'id': self.next_id,
            'table_id': table_id,
            'customer_name': customer_name,
            'date': date,
            'time': time,
            'status': 'pending'
        }
        self.bookings.append(booking)
        self.next_id += 1
        return booking
    
    def cancel_booking(self, booking_id):
        for booking in self.bookings:
            if booking['id'] == booking_id:
                booking['status'] = 'cancelled'
                return True
        return False
