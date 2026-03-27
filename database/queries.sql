-- =====================================================
-- Примеры запросов
-- =====================================================

-- 1. Свободные столики на 25.03.2026 19:00
SELECT t.number, t.seats, t.location
FROM "table" t
WHERE NOT EXISTS (
    SELECT 1 FROM booking b
    WHERE b.table_id = t.id
      AND b.booking_date = '2026-03-25'
      AND b.booking_time = '19:00:00'
      AND b.status IN ('pending', 'confirmed')
);

-- 2. Все бронирования с деталями
SELECT 
    b.id,
    t.number AS table_number,
    c.name AS guest_name,
    c.phone,
    b.booking_date,
    b.booking_time,
    b.status
FROM booking b
JOIN "table" t ON b.table_id = t.id
JOIN customer c ON b.customer_id = c.id
ORDER BY b.booking_date, b.booking_time;

-- 3. Статистика по статусам
SELECT status, COUNT(*) AS count
FROM booking
GROUP BY status;
