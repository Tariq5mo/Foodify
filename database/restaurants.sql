USE foodify_db;

-- Insert restaurants with string UUID v4 format
INSERT INTO restaurants (id, name, city, logo_url, created_at, updated_at) VALUES
('5a1d9e24-cc7a-11ef-981d-000d3ad5d72a', 'Burger Blast', 'New York', 'static/images/menu_items/Burger_Blast/logo.jpeg', NOW(), NOW()),
('f72c4db3-cc7a-11ef-981d-000d3ad5d72b', 'Green Plate', 'Los Angeles', 'static/images/menu_items/Green_Plate/logo.jpeg', NOW(), NOW()),
('01f5e267-cc7b-11ef-981d-000d3ad5d72c', 'Healthy Bites', 'Chicago', 'static/images/menu_items/Healthy_Bites/logo.jpeg', NOW(), NOW()),
('0c1e7f51-cc7b-11ef-981d-000d3ad5d72d', 'Pizza Point', 'Miami', 'static/images/menu_items/Pizza_Point/logo.jpeg', NOW(), NOW()),
('166c1c3a-cc7b-11ef-981d-000d3ad5d72e', 'Taco Tower', 'Houston', 'static/images/menu_items/Taco_Tower/logo.jpeg', NOW(), NOW()),
('208d9e24-cc7b-11ef-981d-000d3ad5d72f', 'Wings and Things', 'Dallas', 'static/images/menu_items/Wings_and_Things/logo.jpeg', NOW(), NOW());
