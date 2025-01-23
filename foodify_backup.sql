-- MySQL dump 10.13  Distrib 8.0.40, for Linux (x86_64)
--
-- Host: localhost    Database: foodify_db
-- ------------------------------------------------------
-- Server version	8.0.40-0ubuntu0.20.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `clients`
--

DROP TABLE IF EXISTS `clients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `clients` (
  `username` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(128) DEFAULT NULL,
  `address` varchar(500) NOT NULL,
  `id` varchar(60) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `latitude` float DEFAULT NULL,
  `longitude` float DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `delivery_instructions` varchar(500) DEFAULT NULL,
  `contact_name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clients`
--

LOCK TABLES `clients` WRITE;
/*!40000 ALTER TABLE `clients` DISABLE KEYS */;
INSERT INTO `clients` VALUES ('tariq','Tariq@gmail.com','$2b$12$wFRE4VGyf4P6Uyto.0N8ce.K67/ZN.6QMyZtadYHm37JWWiKoKXSa','dddsd','78bb0876-5825-4784-ab35-fd4a06d07dfb','2025-01-07 13:54:45','2025-01-07 13:54:45',30.033,31.2176,'+249128007101','',NULL),('Talal4024 ','tala@gmail.com','$2b$12$2wYKH2GKPuYl2Fl5hMM9GeV4pMhpWoLDIAgofwQIeNy.kLxXpilsu','ppp','82127fb2-223f-4ed5-8a90-3934caf3101a','2025-01-12 17:36:23','2025-01-12 17:36:23',-15.4155,28.2773,NULL,'',NULL);
/*!40000 ALTER TABLE `clients` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `menu_items`
--

DROP TABLE IF EXISTS `menu_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `menu_items` (
  `restaurant_id` varchar(60) NOT NULL,
  `name` varchar(100) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `is_available` tinyint(1) DEFAULT NULL,
  `image_url` varchar(255) DEFAULT NULL,
  `id` varchar(60) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `restaurant_id` (`restaurant_id`),
  CONSTRAINT `menu_items_ibfk_1` FOREIGN KEY (`restaurant_id`) REFERENCES `restaurants` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `menu_items`
--

LOCK TABLES `menu_items` WRITE;
/*!40000 ALTER TABLE `menu_items` DISABLE KEYS */;
INSERT INTO `menu_items` VALUES ('dbfe79f4-cce8-11ef-af00-00155d5c995c','Double Beef Burger',15.99,0,'static/images/menu_items/Burger_Blast/Double_Beef_Burger.png','2a1d9e24-cc7b-11ef-981d-000d3ad5d001','2025-01-08 12:16:14','2025-01-08 12:16:14'),('dbfe79f4-cce8-11ef-af00-00155d5c995c','Crispy Chicken Strips',12.99,1,'static/images/menu_items/Burger_Blast/Crispy_Chicken_Strips.png','2a1d9e24-cc7b-11ef-981d-000d3ad5d002','2025-01-08 12:16:14','2025-01-08 12:16:14'),('dbfe79f4-cce8-11ef-af00-00155d5c995c','Cheesy Fries',6.99,1,'static/images/menu_items/Burger_Blast/Cheesy_Fries.png','2a1d9e24-cc7b-11ef-981d-000d3ad5d003','2025-01-08 12:16:14','2025-01-08 12:16:14'),('dbfe79f4-cce8-11ef-af00-00155d5c995c','Onion Rings',5.99,1,'static/images/menu_items/Burger_Blast/Onion_Rings.png','2a1d9e24-cc7b-11ef-981d-000d3ad5d004','2025-01-08 12:16:14','2025-01-08 12:16:14'),('dbfe79f4-cce8-11ef-af00-00155d5c995c','Chocolate Shake',5.99,1,'static/images/menu_items/Burger_Blast/Chocolate_Shake.png','2a1d9e24-cc7b-11ef-981d-000d3ad5d005','2025-01-08 12:16:14','2025-01-08 12:16:14'),('dbfefce7-cce8-11ef-af00-00155d5c995c','Grilled Chicken Salad',11.99,1,'static/images/menu_items/Green_Plate/Grilled_Chicken_Salad.png','2a1d9e24-cc7b-11ef-981d-000d3ad5d006','2025-01-08 12:16:14','2025-01-08 12:16:14'),('dbfefce7-cce8-11ef-af00-00155d5c995c','Lentil Soup',6.99,1,'static/images/menu_items/Green_Plate/Lentil_Soup.png','2a1d9e24-cc7b-11ef-981d-000d3ad5d007','2025-01-08 12:16:14','2025-01-08 12:16:14'),('dbfefce7-cce8-11ef-af00-00155d5c995c','Quinoa & Avocado Bowl',13.99,1,'static/images/menu_items/Green_Plate/Quinoa_&_Avocado_Bowl.png','2a1d9e24-cc7b-11ef-981d-000d3ad5d008','2025-01-08 12:16:14','2025-01-08 12:16:14'),('dbfefce7-cce8-11ef-af00-00155d5c995c','Smoothie Bowl Mixed Berries',9.99,1,'static/images/menu_items/Green_Plate/Smoothie_Bowl_Mixed_Berries.png','2a1d9e24-cc7b-11ef-981d-000d3ad5d009','2025-01-08 12:16:14','2025-01-08 12:16:14'),('dbfefce7-cce8-11ef-af00-00155d5c995c','Vegan Brownie',5.99,1,'static/images/menu_items/Green_Plate/Vegan Brownie.png','2a1d9e24-cc7b-11ef-981d-000d3ad5d010','2025-01-08 12:16:14','2025-01-08 12:16:14'),('dbff1ca1-cce8-11ef-af00-00155d5c995c','Baked Salmon with Veggies',16.99,1,'static/images/menu_items/Healthy_Bites/Baked_Salmon with_Veggies.png','2a1d9e24-cc7b-11ef-981d-000d3ad5d011','2025-01-08 12:16:14','2025-01-08 12:16:14'),('dbff1ca1-cce8-11ef-af00-00155d5c995c','Chia Pudding with Fruits',7.99,1,'static/images/menu_items/Healthy_Bites/Chia_Pudding_with_Fruits.png','2a1d9e24-cc7b-11ef-981d-000d3ad5d012','2025-01-08 12:16:14','2025-01-08 12:16:14'),('dbff1ca1-cce8-11ef-af00-00155d5c995c','Greek Salad',10.99,1,'static/images/menu_items/Healthy_Bites/Greek_Salad.png','2a1d9e24-cc7b-11ef-981d-000d3ad5d013','2025-01-08 12:16:14','2025-01-08 12:16:14'),('dbff1ca1-cce8-11ef-af00-00155d5c995c','Green Detox Smoothie',6.99,1,'static/images/menu_items/Healthy_Bites/Green_Detox_Smoothie.png','2a1d9e24-cc7b-11ef-981d-000d3ad5d014','2025-01-08 12:16:14','2025-01-08 12:16:14'),('dbff1ca1-cce8-11ef-af00-00155d5c995c','Zucchini Noodles with Pesto',12.99,1,'static/images/menu_items/Healthy_Bites/Zucchini_Noodles_with_Pesto.png','2a1d9e24-cc7b-11ef-981d-000d3ad5d015','2025-01-08 12:16:14','2025-01-08 12:16:14'),('dbff2a92-cce8-11ef-af00-00155d5c995c','Cheesy Garlic Bread',6.99,1,'static/images/menu_items/Pizza_Point/Cheesy_Garlic_Bread.png','2a1d9e24-cc7b-11ef-981d-000d3ad5d016','2025-01-08 12:16:14','2025-01-08 12:16:14'),('dbff2a92-cce8-11ef-af00-00155d5c995c','Chicken Alfredo Pasta',14.99,1,'static/images/menu_items/Pizza_Point/Chicken_Alfredo_Pasta.png','2a1d9e24-cc7b-11ef-981d-000d3ad5d017','2025-01-08 12:16:14','2025-01-08 12:16:14'),('dbff2a92-cce8-11ef-af00-00155d5c995c','Chocolate Brownie',5.99,1,'static/images/menu_items/Pizza_Point/Chocolate_Brownie.png','2a1d9e24-cc7b-11ef-981d-000d3ad5d018','2025-01-08 12:16:14','2025-01-08 12:16:14'),('dbff2a92-cce8-11ef-af00-00155d5c995c','Margherita Pizza Medium',15.99,1,'static/images/menu_items/Pizza_Point/Margherita_Pizza_Medium.png','2a1d9e24-cc7b-11ef-981d-000d3ad5d019','2025-01-08 12:16:14','2025-01-08 12:16:14'),('dbff2a92-cce8-11ef-af00-00155d5c995c','Pepperoni Pizza Large',18.99,1,'static/images/menu_items/Pizza_Point/Pepperoni_Pizza_Large.png','2a1d9e24-cc7b-11ef-981d-000d3ad5d020','2025-01-08 12:16:14','2025-01-08 12:16:14'),('dbff2ed1-cce8-11ef-af00-00155d5c995c','Beef Taco Combo',13.99,1,'static/images/menu_items/Taco_Tower/Beef_Taco Combo.png','2a1d9e24-cc7b-11ef-981d-000d3ad5d021','2025-01-08 12:16:14','2025-01-08 12:16:14'),('dbff2ed1-cce8-11ef-af00-00155d5c995c','Cheesy Quesadilla',9.99,1,'static/images/menu_items/Taco_Tower/Cheesy_Quesadilla.png','2a1d9e24-cc7b-11ef-981d-000d3ad5d022','2025-01-08 12:16:14','2025-01-08 12:16:14'),('dbff2ed1-cce8-11ef-af00-00155d5c995c','Chicken Burrito Bowl',12.99,1,'static/images/menu_items/Taco_Tower/Chicken_Burrito_Bowl.png','2a1d9e24-cc7b-11ef-981d-000d3ad5d023','2025-01-08 12:16:14','2025-01-08 12:16:14'),('dbff2ed1-cce8-11ef-af00-00155d5c995c','Churros with Chocolate Sauce',6.99,1,'static/images/menu_items/Taco_Tower/Churros_with_Chocolate_Sauce.png','2a1d9e24-cc7b-11ef-981d-000d3ad5d024','2025-01-08 12:16:14','2025-01-08 12:16:14'),('dbff2ed1-cce8-11ef-af00-00155d5c995c','Spicy Nacho Fries',7.99,1,'static/images/menu_items/Taco_Tower/Spicy_Nacho_Fries.png','2a1d9e24-cc7b-11ef-981d-000d3ad5d025','2025-01-08 12:16:14','2025-01-08 12:16:14'),('dbff2fc6-cce8-11ef-af00-00155d5c995c','BBQ Chicken Wings',13.99,1,'static/images/menu_items/Wings_and_Things/BBQ_Chicken_Wings.png','2a1d9e24-cc7b-11ef-981d-000d3ad5d026','2025-01-08 12:16:14','2025-01-08 12:16:14'),('dbff2fc6-cce8-11ef-af00-00155d5c995c','Buffalo Wings 12 pcs',16.99,1,'static/images/menu_items/Wings_and_Things/Buffalo_Wings_12_pcs.png','2a1d9e24-cc7b-11ef-981d-000d3ad5d027','2025-01-08 12:16:14','2025-01-08 12:16:14'),('dbff2fc6-cce8-11ef-af00-00155d5c995c','Loaded Nachos',9.99,1,'static/images/menu_items/Wings_and_Things/Loaded_Nachos.png','2a1d9e24-cc7b-11ef-981d-000d3ad5d028','2025-01-08 12:16:14','2025-01-08 12:16:14'),('dbff2fc6-cce8-11ef-af00-00155d5c995c','Sweet Chili Sauce Wings 6 pcs',11.99,1,'static/images/menu_items/Wings_and_Things/Sweet_Chili_Sauce_Wings_6_pcs.png','2a1d9e24-cc7b-11ef-981d-000d3ad5d029','2025-01-08 12:16:14','2025-01-08 12:16:14');
/*!40000 ALTER TABLE `menu_items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_items`
--

DROP TABLE IF EXISTS `order_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_items` (
  `id` varchar(60) NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `order_id` varchar(60) NOT NULL,
  `menu_item_id` varchar(60) NOT NULL,
  `quantity` int NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  KEY `idx_order_items_order` (`order_id`),
  KEY `idx_order_items_menu_item` (`menu_item_id`),
  CONSTRAINT `order_items_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`) ON DELETE CASCADE,
  CONSTRAINT `order_items_ibfk_2` FOREIGN KEY (`menu_item_id`) REFERENCES `menu_items` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_items`
--

LOCK TABLES `order_items` WRITE;
/*!40000 ALTER TABLE `order_items` DISABLE KEYS */;
/*!40000 ALTER TABLE `order_items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders` (
  `id` varchar(60) NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `client_id` varchar(60) NOT NULL,
  `status` varchar(20) NOT NULL DEFAULT 'active',
  `order_date` datetime DEFAULT CURRENT_TIMESTAMP,
  `total_price` decimal(10,2) DEFAULT '0.00',
  PRIMARY KEY (`id`),
  KEY `idx_orders_client` (`client_id`),
  KEY `idx_orders_status` (`status`),
  CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`client_id`) REFERENCES `clients` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `restaurants`
--

DROP TABLE IF EXISTS `restaurants`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `restaurants` (
  `name` varchar(100) NOT NULL,
  `city` varchar(100) NOT NULL,
  `logo_url` varchar(255) DEFAULT NULL,
  `id` varchar(60) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `restaurants`
--

LOCK TABLES `restaurants` WRITE;
/*!40000 ALTER TABLE `restaurants` DISABLE KEYS */;
INSERT INTO `restaurants` VALUES ('Burger Blast','New York','static/images/menu_items/Burger_Blast/logo.jpeg','dbfe79f4-cce8-11ef-af00-00155d5c995c','2025-01-07 13:16:36','2025-01-07 13:16:36'),('Green Plate','Los Angeles','static/images/menu_items/Green_Plate/logo.jpeg','dbfefce7-cce8-11ef-af00-00155d5c995c','2025-01-07 13:16:36','2025-01-07 13:16:36'),('Healthy Bites','Chicago','static/images/menu_items/Healthy_Bites/logo.jpeg','dbff1ca1-cce8-11ef-af00-00155d5c995c','2025-01-07 13:16:36','2025-01-07 13:16:36'),('Pizza Point','Miami','static/images/menu_items/Pizza_Point/logo.jpeg','dbff2a92-cce8-11ef-af00-00155d5c995c','2025-01-07 13:16:36','2025-01-07 13:16:36'),('Taco Tower','Houston','static/images/menu_items/Taco_Tower/logo.jpeg','dbff2ed1-cce8-11ef-af00-00155d5c995c','2025-01-07 13:16:36','2025-01-07 13:16:36'),('Wings and Things','Dallas','static/images/menu_items/Wings_and_Things/logo.jpeg','dbff2fc6-cce8-11ef-af00-00155d5c995c','2025-01-07 13:16:36','2025-01-07 13:16:36');
/*!40000 ALTER TABLE `restaurants` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reviews`
--

DROP TABLE IF EXISTS `reviews`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reviews` (
  `client_id` varchar(60) NOT NULL,
  `restaurant_id` varchar(60) NOT NULL,
  `rating` int NOT NULL,
  `comment` text,
  `id` varchar(60) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `client_id` (`client_id`),
  KEY `restaurant_id` (`restaurant_id`),
  CONSTRAINT `reviews_ibfk_1` FOREIGN KEY (`client_id`) REFERENCES `clients` (`id`),
  CONSTRAINT `reviews_ibfk_2` FOREIGN KEY (`restaurant_id`) REFERENCES `restaurants` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reviews`
--

LOCK TABLES `reviews` WRITE;
/*!40000 ALTER TABLE `reviews` DISABLE KEYS */;
/*!40000 ALTER TABLE `reviews` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-01-21 13:14:22
