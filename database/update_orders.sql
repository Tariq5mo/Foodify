-- Drop any existing order_items and orders tables to start fresh
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;

-- Create the orders table
CREATE TABLE orders (
    id VARCHAR(60) PRIMARY KEY,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    client_id VARCHAR(60) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'active',
    order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (client_id) REFERENCES clients(id) ON DELETE CASCADE
);

-- Create the order_items table
CREATE TABLE order_items (
    id VARCHAR(60) PRIMARY KEY,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    order_id VARCHAR(60) NOT NULL,
    menu_item_id VARCHAR(60) NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (menu_item_id) REFERENCES menu_items(id) ON DELETE CASCADE
);

-- Add indexes for better query performance
CREATE INDEX idx_orders_client ON orders(client_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_order_items_order ON order_items(order_id);
CREATE INDEX idx_order_items_menu_item ON order_items(menu_item_id);
