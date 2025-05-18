-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: localhost    Database: crm_system
-- ------------------------------------------------------
-- Server version	8.0.42

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
-- Table structure for table `master`
--

DROP TABLE IF EXISTS `master`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `master` (
  `id` varchar(50) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `firm` varchar(255) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `region` varchar(100) DEFAULT NULL,
  `location_` varchar(255) DEFAULT NULL,
  `function_` varchar(100) DEFAULT NULL,
  `group_name` varchar(100) DEFAULT NULL,
  `focus` varchar(255) DEFAULT NULL,
  `prior_firm` varchar(255) DEFAULT NULL,
  `notes` text,
  `sr` varchar(10) DEFAULT NULL,
  `off_limits` varchar(50) DEFAULT NULL,
  `ix` int DEFAULT NULL,
  `date_added` date DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `master_snapshot`
--

DROP TABLE IF EXISTS `master_snapshot`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `master_snapshot` (
  `id` varchar(50) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `firm` varchar(255) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `region` varchar(100) DEFAULT NULL,
  `location_` varchar(255) DEFAULT NULL,
  `function_` varchar(100) DEFAULT NULL,
  `group_name` varchar(100) DEFAULT NULL,
  `focus` varchar(255) DEFAULT NULL,
  `prior_firm` varchar(255) DEFAULT NULL,
  `notes` text,
  `sr` varchar(10) DEFAULT NULL,
  `off_limits` varchar(50) DEFAULT NULL,
  `ix` int DEFAULT NULL,
  `date_added` date DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `work_history`
--

DROP TABLE IF EXISTS `work_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `work_history` (
  `id` int NOT NULL AUTO_INCREMENT,
  `person_id` varchar(50) DEFAULT NULL,
  `firm` varchar(255) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `location_` varchar(255) DEFAULT NULL,
  `date_start` date DEFAULT NULL,
  `date_end` date DEFAULT NULL,
  `note` text,
  `created_at` datetime DEFAULT NULL,
  `source` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `person_id` (`person_id`),
  CONSTRAINT `work_history_ibfk_1` FOREIGN KEY (`person_id`) REFERENCES `master` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3337 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-18  2:24:14
