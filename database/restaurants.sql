USE foodify_db;

-- Insert restaurants with string UUID v4 format
INSERT INTO restaurants (id, name, city, logo_url, created_at, updated_at) VALUES
(uuid(), 'Burger Blast', 'New York', 'static/images/menu_items/Burger_Blast/logo.jpeg', NOW(), NOW()),
(uuid(), 'Green Plate', 'Los Angeles', 'static/images/menu_items/Green_Plate/logo.jpeg', NOW(), NOW()),
(uuid(), 'Healthy Bites', 'Chicago', 'static/images/menu_items/Healthy_Bites/logo.jpeg', NOW(), NOW()),
(uuid(), 'Pizza Point', 'Miami', 'static/images/menu_items/Pizza_Point/logo.jpeg', NOW(), NOW()),
(uuid(), 'Taco Tower', 'Houston', 'static/images/menu_items/Taco_Tower/logo.jpeg', NOW(), NOW()),
(uuid(), 'Wings and Things', 'Dallas', 'static/images/menu_items/Wings_and_Things/logo.jpeg', NOW(), NOW());
