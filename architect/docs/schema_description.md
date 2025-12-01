# 📘 Schema Description — Hotel Booking Database

This document describes the structure of the **Hotel Booking relational database**, including all tables, columns, primary keys, foreign keys, and relationships.

---

## 🏨 1. **hotels**

Stores information about hotel types.

| Column        | Type        | Description            |
| ------------- | ----------- | ---------------------- |
| hotel_id (PK) | INT         | Unique hotel ID        |
| hotel_type    | VARCHAR(50) | "City Hotel", "Resort" |

---

## 🛏️ 2. **rooms**

Stores room codes.

| Column       | Type       | Description        |
| ------------ | ---------- | ------------------ |
| room_id (PK) | INT        | Unique room ID     |
| room_code    | VARCHAR(5) | Room category code |

---

## 🍽️ 3. **meals**

Stores meal plan types.

| Column       | Type       | Description               |
| ------------ | ---------- | ------------------------- |
| meal_id (PK) | INT        | Unique meal ID            |
| meal         | VARCHAR(5) | BB, HB, FB, SC, Undefined |

---

## 💳 4. **deposit_types**

Deposit guarantees used during booking.

| Column             | Type        | Description              |
| ------------------ | ----------- | ------------------------ |
| deposit_type_id PK | INT         | Unique deposit type ID   |
| deposit_type       | VARCHAR(50) | Type of deposit required |

---

## 🌐 5. **distribution_channels**

Booking distribution channels.

| Column                     | Type        | Description             |
| -------------------------- | ----------- | ----------------------- |
| distribution_channel_id PK | INT         | Unique channel ID       |
| distribution_channel       | VARCHAR(50) | Direct / TA / Corporate |

---

## 👤 6. **customers**

Customer metadata.

| Column                         | Type        | Description                      |
| ------------------------------ | ----------- | -------------------------------- |
| customer_id (PK)               | INT         | Unique customer ID               |
| is_repeated_guest              | TINYINT(1)  | 1 = returning guest              |
| previous_cancellations         | INT         | Number of past cancellations     |
| previous_bookings_not_canceled | INT         | Number of successful bookings    |
| customer_type                  | VARCHAR(50) | Type (Transient, Contract, etc.) |
| country                        | VARCHAR(10) | ISO country code                 |

---

## 💼 7. **market_segments**

Booking sales segments.

| Column               | Type        | Description                 |
| -------------------- | ----------- | --------------------------- |
| market_segment_id PK | INT         | Unique segment ID           |
| market_segment       | VARCHAR(50) | Online TA, Offline TA, etc. |

---

## 📅 8. **bookings (FACT TABLE)**

The central table storing all booking information.

| Column                     | Type        | Description                      |
| -------------------------- | ----------- | -------------------------------- |
| booking_id (PK)            | INT         | Unique booking ID                |
| hotel_id (FK)              | INT         | → hotels                         |
| customer_id (FK)           | INT         | → customers                      |
| reserved_room_id (FK)      | INT         | → rooms                          |
| assigned_room_id (FK)      | INT         | → rooms                          |
| meal_id (FK)               | INT         | → meals                          |
| market_segment_id (FK)     | INT         | → market_segments                |
| distribution_channel_id FK | INT         | → distribution_channels          |
| deposit_type_id (FK)       | INT         | → deposit_types                  |
| is_canceled                | TINYINT(1)  | 1 = canceled                     |
| lead_time                  | INT         | Days between booking and arrival |
| arrival_date_year          | INT         | Year                             |
| arrival_date_month         | INT         | Month (1–12)                     |
| arrival_date_day_of_month  | INT         | Day of month                     |
| stays_in_weekend_nights    | INT         | Nights stayed on weekends        |
| stays_in_week_nights       | INT         | Nights stayed on weekdays        |
| adults                     | INT         | Number of adults                 |
| children                   | INT         | Number of children               |
| babies                     | INT         | Number of babies                 |
| booking_changes            | INT         | Number of modifications          |
| agent                      | INT         | Travel agency ID                 |
| company                    | INT         | Company ID                       |
| adr                        | DECIMAL     | Average daily rate               |
| required_car_parking       | INT         | Parking spaces                   |
| total_special_requests     | INT         | Special requests                 |
| reservation_status         | VARCHAR(50) | Current status                   |
| reservation_status_date    | DATE        | When status changed              |

---

## 🔗 Relationships Summary

| Parent Table          | Child Table | Key                     |
| --------------------- | ----------- | ----------------------- |
| hotels                | bookings    | hotel_id → hotel_id     |
| rooms                 | bookings    | reserved_room_id        |
| meals                 | bookings    | meal_id                 |
| market_segments       | bookings    | market_segment_id       |
| deposit_types         | bookings    | deposit_type_id         |
| distribution_channels | bookings    | distribution_channel_id |
| customers             | bookings    | customer_id             |

