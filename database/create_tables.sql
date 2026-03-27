-- =====================================================
-- Система бронирования столиков в ресторане
-- Создание таблиц (PostgreSQL)
-- =====================================================

-- Таблица столиков
CREATE TABLE IF NOT EXISTS "table" (
    id SERIAL PRIMARY KEY,
    number VARCHAR(10) NOT NULL UNIQUE,
    seats INTEGER NOT NULL CHECK (seats > 0),
    location VARCHAR(100)
);

-- Таблица гостей
CREATE TABLE IF NOT EXISTS customer (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL UNIQUE,
    email VARCHAR(100)
);

-- Таблица бронирований
CREATE TABLE IF NOT EXISTS booking (
    id SERIAL PRIMARY KEY,
    table_id INTEGER NOT NULL REFERENCES "table"(id) ON DELETE CASCADE,
    customer_id INTEGER NOT NULL REFERENCES customer(id) ON DELETE CASCADE,
    booking_date DATE NOT NULL,
    booking_time TIME NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (table_id, booking_date, booking_time)
);

-- Индексы
CREATE INDEX IF NOT EXISTS idx_booking_date_time ON booking(booking_date, booking_time);
CREATE INDEX IF NOT EXISTS idx_booking_status ON booking(status);
CREATE INDEX IF NOT EXISTS idx_customer_phone ON customer(phone);

-- Таблица пользователей
CREATE TABLE IF NOT EXISTS "user" (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'admin'
);
