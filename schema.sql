-- schema.sql
-- Kore: high-end consumer GPUs, orders, and address changes waiting for staff.

CREATE TABLE IF NOT EXISTS orders (
    order_id TEXT PRIMARY KEY,
    customer TEXT NOT NULL,
    card     TEXT NOT NULL,
    status   TEXT NOT NULL,
    address  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS products (
    name  TEXT PRIMARY KEY,
    price REAL NOT NULL,
    stock INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS change_requests (
    number      INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id    TEXT NOT NULL,
    new_address TEXT NOT NULL,
    status      TEXT NOT NULL DEFAULT 'waiting'
);

INSERT OR IGNORE INTO orders (order_id, customer, card, status, address) VALUES
    ('K100', 'Jordan Lee', 'K80', 'shipped', '14 Oak St, Austin TX'),
    ('K101', 'Sam Rivera', 'K60 Ti', 'processing', '3 Pine Ave, Denver CO'),
    ('K102', 'Alex Kim', 'K80 Ti', 'delivered', '88 Maple Dr, Seattle WA'),
    ('K103', 'Taylor Brooks', 'K20', 'processing', '21 Birch Ln, Miami FL'),
    ('K104', 'Morgan Diaz', 'K40 Ti', 'shipped', '7 Cedar Ct, Chicago IL'),
    ('K105', 'Casey Nguyen', 'K60', 'delivered', '40 Elm St, Boston MA');

INSERT OR IGNORE INTO products (name, price, stock) VALUES
    ('K80', 1799.00, 3),
    ('K80 Ti', 2199.00, 0),
    ('K60', 1199.00, 4),
    ('K60 Ti', 1499.00, 2),
    ('K40', 899.00, 0),
    ('K40 Ti', 1099.00, 6),
    ('K20', 699.00, 10),
    ('K20 Ti', 849.00, 5);
