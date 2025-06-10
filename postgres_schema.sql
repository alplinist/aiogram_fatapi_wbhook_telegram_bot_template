-- SQL schema for PostgreSQL
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    telegram_id BIGINT UNIQUE NOT NULL,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    phone_number VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS addresses (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    address TEXT,
    is_default BOOLEAN DEFAULT FALSE
);

CREATE TYPE order_status AS ENUM (
    'ordered',
    'received_in_china',
    'in_transit',
    'arrived_in_uzbekistan',
    'ready_for_pickup'
);

CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    tracking_number VARCHAR(255) UNIQUE NOT NULL,
    status order_status DEFAULT 'ordered',
    weight DOUBLE PRECISION,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
