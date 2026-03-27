from flask import Flask, request, jsonify, send_from_directory, session
from flask_cors import CORS
import os

from auth import AuthManager
from booking import BookingManager
from admin import AdminManager

app = Flask(__name__, static_folder='../frontend')
app.secret_key = 'super-secret-key-change-in-production'  # Для сессий
CORS(app, supports_credentials=True)

# Инициализация менеджеров
auth_manager = AuthManager()
booking_manager = BookingManager()
admin_manager = AdminManager(booking_manager)

# Каталог столиков (временное хранилище)
tables = [
    {'id': 1, 'number': 'A1', 'seats': 2, 'location': 'у окна', 'hall': 'Основной зал', 'image': '/images/table1.jpg'},
    {'id': 2, 'number': 'A2', 'seats': 4, 'location': 'центр зала', 'hall': 'Основной зал', 'image': '/images/table2.jpg'},
    {'id': 3, 'number': 'B1', 'seats': 6, 'location': 'отдельная кабинка', 'hall': 'Второй зал', 'image': '/images/table3.jpg'},
    {'id': 4, 'number': 'B2', 'seats': 4, 'location': 'у окна', 'hall': 'Второй зал', 'image': '/images/table4.jpg'},
    # для пятого столика можно добавить ещё одно фото
    {'id': 5, 'number': 'C1', 'seats': 8, 'location': 'вип-зона', 'hall': 'Вип-зал', 'image': '/images/table5.jpg'},
]

# ========== API для гостя ==========
@app.route('/api/tables', methods=['GET'])
def get_tables():
    date = request.args.get('date')
    time = request.args.get('time')
    if date and time:
        booked = booking_manager.get_booked_table_ids(date, time)
        free_tables = [t for t in tables if t['id'] not in booked]
        return jsonify(free_tables)
    return jsonify(tables)

@app.route('/api/book', methods=['POST'])
def book_table():
    data = request.json
    table_id = data.get('table_id')
    customer_name = data.get('customer_name')
    phone = data.get('phone')
    date = data.get('date')
    time = data.get('time')

    if not all([table_id, customer_name, phone, date, time]):
        return jsonify({'error': 'Не все поля заполнены'}), 400

    booked = booking_manager.get_booked_table_ids(date, time)
    if table_id in booked:
        return jsonify({'error': 'Столик уже забронирован на это время'}), 409

    booking = booking_manager.create_booking(table_id, customer_name, date, time)
    booking['phone'] = phone
    return jsonify({
        'booking_id': booking['id'],
        'status': booking['status'],
        'code': booking['code']
    }), 201

@app.route('/api/cancel_by_code', methods=['POST'])
def cancel_by_code():
    data = request.json
    code = data.get('code')
    if not code:
        return jsonify({'error': 'Код обязателен'}), 400

    success, booking = booking_manager.cancel_by_code(code)
    if success:
        return jsonify({'message': f'Бронь для {booking["customer_name"]} отменена'})
    else:
        return jsonify({'error': 'Неверный код или бронь уже отменена'}), 404

# ========== API администратора ==========
def admin_required(f):
    def wrapper(*args, **kwargs):
        if not session.get('admin'):
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    data = request.json
    if data.get('username') == 'admin' and data.get('password') == 'admin123':
        session['admin'] = True
        return jsonify({'success': True})
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/admin/logout', methods=['POST'])
def admin_logout():
    session.pop('admin', None)
    return jsonify({'success': True})

@app.route('/api/admin/bookings', methods=['GET'])
@admin_required
def admin_bookings():
    return jsonify(booking_manager.bookings)

@app.route('/api/admin/confirm/<int:booking_id>', methods=['POST'])
@admin_required
def confirm_booking(booking_id):
    if admin_manager.confirm_booking(booking_id):
        return jsonify({'message': 'Бронь подтверждена'})
    return jsonify({'error': 'Бронь не найдена'}), 404

@app.route('/api/admin/tables', methods=['GET', 'POST'])
@admin_required
def manage_tables():
    if request.method == 'GET':
        return jsonify(tables)
    if request.method == 'POST':
        data = request.json
        new_table = {
            'id': len(tables) + 1,
            'number': data.get('number'),
            'seats': data.get('seats'),
            'location': data.get('location')
        }
        tables.append(new_table)
        return jsonify(new_table), 201

@app.route('/api/admin/tables/<int:table_id>', methods=['DELETE'])
@admin_required
def delete_table(table_id):
    for i, t in enumerate(tables):
        if t['id'] == table_id:
            tables.pop(i)
            return jsonify({'success': True})
    return jsonify({'error': 'Table not found'}), 404

# ========== Статические файлы ==========
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/admin')
def admin_page():
    return send_from_directory(app.static_folder, 'admin.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    print("\n" + "=" * 50)
    print("Сервер запущен!!")
    print("Основной сайт: http://127.0.0.1:5000")
    print("Админка: http://127.0.0.1:5000/admin (логин: admin, пароль: admin123)")
    print("=" * 50 + "\n")
    app.run(debug=True, port=5000, host='127.0.0.1')