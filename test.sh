echo 'create Client fullname="abu malik" email="aaaaaaaae@mail.com" password_hash="123456"' | Foodify_MYSQL_USER=root Foodify_MYSQL_PWD=root Foodify_MYSQL_HOST=localhost Foodify_MYSQL_DB=foodify_db ./console.py

echo 'create Client username="imad" email="imadaa1@mail.com" password_hash="123_456" address="hay_alnajah_N15_Rabat" id="e22c238a-9076-43ae-9ebb-256fa7827b46"' | Foodify_MYSQL_USER=root Foodify_MYSQL_PWD=root Foodify_MYSQL_HOST=localhost Foodify_MYSQL_DB=foodify_db ./console.py

echo 'create Restaurant name="Pizza_Hot" city="Rabat" id="6dc6e02a-acea-4d09-b4ed-550245ec5d9a"' | Foodify_MYSQL_USER=root Foodify_MYSQL_PWD=root Foodify_MYSQL_HOST=localhost Foodify_MYSQL_DB=foodify_db ./console.py

echo 'create Review client_id="e22c238a-9076-43ae-9ebb-256fa7827b46" restaurant_id="6dc6e02a-acea-4d09-b4ed-550245ec5d9a" rating=4 comment="Good_meals"' | Foodify_MYSQL_USER=root Foodify_MYSQL_PWD=root Foodify_MYSQL_HOST=localhost Foodify_MYSQL_DB=foodify_db ./console.py

# MySQL commands for creating user and setting privileges (only run once)
SET FOREIGN_KEY_CHECKS=0;

CREATE USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'root';

GRANT ALL PRIVILEGES ON *.* TO 'test'@'localhost';

FLUSH PRIVILEGES;
