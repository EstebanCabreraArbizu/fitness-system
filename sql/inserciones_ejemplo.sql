CREATE DATABASE  IF NOT EXISTS `flaskcrud` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `flaskcrud`;
-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: flaskcrud
-- ------------------------------------------------------
-- Server version	9.1.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `cliente_datos`
--

DROP TABLE IF EXISTS `cliente_datos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cliente_datos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nivel_actividad` varchar(50) NOT NULL,
  `direccion` varchar(200) NOT NULL,
  `tipo_cliente` varchar(50) NOT NULL,
  `Usuario_id` int NOT NULL,
  `fecha_pago` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `Cliente_datos_Usuario` (`Usuario_id`),
  CONSTRAINT `Cliente_datos_Usuario` FOREIGN KEY (`Usuario_id`) REFERENCES `usuario` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cliente_datos`
--

LOCK TABLES `cliente_datos` WRITE;
/*!40000 ALTER TABLE `cliente_datos` DISABLE KEYS */;
INSERT INTO `cliente_datos` VALUES (1,'Moderado','Calle Cliente 123','regular',1,NULL),(2,'Principiante','Calle Principal 123','regular',10,NULL),(3,'Intermedio','Avenida Central 456','premium',11,NULL),(4,'Avanzado','Boulevard Norte 789','regular',12,NULL),(5,'Principiante','Calle Sur 321','premium',13,NULL),(6,'Intermedio','Avenida Este 654','regular',14,NULL);
/*!40000 ALTER TABLE `cliente_datos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cliente_instructor`
--

DROP TABLE IF EXISTS `cliente_instructor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cliente_instructor` (
  `id` int NOT NULL AUTO_INCREMENT,
  `Usuario_id` int NOT NULL,
  `Usuario_2_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Cliente_Instructor_Usuario` (`Usuario_id`),
  KEY `Cliente_Instructor_Usuario_2` (`Usuario_2_id`),
  CONSTRAINT `Cliente_Instructor_Usuario` FOREIGN KEY (`Usuario_id`) REFERENCES `usuario` (`id`),
  CONSTRAINT `Cliente_Instructor_Usuario_2` FOREIGN KEY (`Usuario_2_id`) REFERENCES `usuario` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cliente_instructor`
--

LOCK TABLES `cliente_instructor` WRITE;
/*!40000 ALTER TABLE `cliente_instructor` DISABLE KEYS */;
INSERT INTO `cliente_instructor` VALUES (1,1,2),(2,1,3),(3,10,2);
/*!40000 ALTER TABLE `cliente_instructor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comida`
--

DROP TABLE IF EXISTS `comida`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comida` (
  `id` int NOT NULL AUTO_INCREMENT,
  `tipo_comida` varchar(100) NOT NULL,
  `dia_dieta` varchar(100) NOT NULL,
  `hora` varchar(100) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `descripcion` text,
  `calorias` int NOT NULL,
  `proteinas` float NOT NULL,
  `carbohidratos` float NOT NULL,
  `grasas` float NOT NULL,
  `recomendacion` varchar(100) NOT NULL,
  `image_name` varchar(100) NOT NULL,
  `status` int NOT NULL,
  `Dieta_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Comida_Dieta` (`Dieta_id`),
  CONSTRAINT `Comida_Dieta` FOREIGN KEY (`Dieta_id`) REFERENCES `dieta` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comida`
--

LOCK TABLES `comida` WRITE;
/*!40000 ALTER TABLE `comida` DISABLE KEYS */;
INSERT INTO `comida` VALUES (1,'Desayuno','Lunes','08:00','Desayuno proteico','Yogurt con frutas y granola',350,15,45,12,'Consumir despacio','desayuno.jpg',1,1),(2,'Almuerzo','Lunes','13:00','Ensalada de pollo','Ensalada verde con pechuga de pollo a la parrilla',450,35,20,15,'Añadir limón al gusto','ensalada.jpg',1,1),(3,'Cena','Lunes','20:00','Cena ligera','Sopa de verduras con pescado al horno',380,25,25,12,'Evitar pan','cena.jpg',1,1);
/*!40000 ALTER TABLE `comida` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dieta`
--

DROP TABLE IF EXISTS `dieta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dieta` (
  `id` int NOT NULL AUTO_INCREMENT,
  `tipo_dieta` varchar(100) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `descripcion` varchar(300) NOT NULL,
  `fecha_inicio` date NOT NULL,
  `fecha_fin` date NOT NULL,
  `duracion_dieta` varchar(100) NOT NULL,
  `fecha_registro` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `edad` varchar(100) NOT NULL,
  `alergias` varchar(100) NOT NULL,
  `enfermedad_cronica` varchar(100) NOT NULL,
  `alergia_medicamento` varchar(100) NOT NULL,
  `dias_semana` varchar(100) NOT NULL,
  `meta_calorias` int NOT NULL,
  `status` int NOT NULL,
  `Discipline_id` int NOT NULL,
  `Usuario_id` int NOT NULL,
  `Usuario_2_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Dieta_Discipline` (`Discipline_id`),
  KEY `Dieta_Usuario` (`Usuario_id`),
  KEY `Dieta_Usuario_2` (`Usuario_2_id`),
  CONSTRAINT `Dieta_Discipline` FOREIGN KEY (`Discipline_id`) REFERENCES `discipline` (`id`),
  CONSTRAINT `Dieta_Usuario` FOREIGN KEY (`Usuario_id`) REFERENCES `usuario` (`id`),
  CONSTRAINT `Dieta_Usuario_2` FOREIGN KEY (`Usuario_2_id`) REFERENCES `usuario` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dieta`
--

LOCK TABLES `dieta` WRITE;
/*!40000 ALTER TABLE `dieta` DISABLE KEYS */;
INSERT INTO `dieta` VALUES (1,'Pérdida de peso','Dieta balanceada baja en calorías','Dieta equilibrada para bajar de peso de forma gradual','2023-05-01','2023-07-31','3 meses','2025-04-29 16:40:05','30-40','Ninguna','Ninguna','Ninguna','Lunes-Viernes',1800,1,2,1,2),(2,'Hipocalórica','Alimetacion para ganar masa muscular','Alimetacion para ganar masa muscular','2025-04-30','2025-05-07','2 semanas','2025-04-30 11:48:55','35','latectios frutos, fruto secos','ninguna','ninguna','Lunes a viernes',2497,1,2,10,2);
/*!40000 ALTER TABLE `dieta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dieta_images`
--

DROP TABLE IF EXISTS `dieta_images`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dieta_images` (
  `id` int NOT NULL AUTO_INCREMENT,
  `image_name` text NOT NULL,
  `Dieta_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Dieta_images_Dieta` (`Dieta_id`),
  CONSTRAINT `Dieta_images_Dieta` FOREIGN KEY (`Dieta_id`) REFERENCES `dieta` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dieta_images`
--

LOCK TABLES `dieta_images` WRITE;
/*!40000 ALTER TABLE `dieta_images` DISABLE KEYS */;
INSERT INTO `dieta_images` VALUES (1,'dieta1.jpg',1),(2,'plan_dieta.jpg',1),(3,'Pechuga_con_arroz_y_verduras_al_vapor__1746031735.jpeg',2);
/*!40000 ALTER TABLE `dieta_images` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `discipline`
--

DROP TABLE IF EXISTS `discipline`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `discipline` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `descripcion` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `discipline`
--

LOCK TABLES `discipline` WRITE;
/*!40000 ALTER TABLE `discipline` DISABLE KEYS */;
INSERT INTO `discipline` VALUES (1,'Fitness General','Entrenamiento general de fitness y acondicionamiento físico'),(2,'Nutrición Deportiva','Asesoramiento nutricional para deportistas'),(3,'Musculación','Entrenamiento enfocado en desarrollo muscular');
/*!40000 ALTER TABLE `discipline` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `discipline_cliente`
--

DROP TABLE IF EXISTS `discipline_cliente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `discipline_cliente` (
  `id` int NOT NULL AUTO_INCREMENT,
  `Discipline_id` int NOT NULL,
  `Usuario_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Discipline_Cliente_Discipline` (`Discipline_id`),
  KEY `Discipline_Cliente_Usuario` (`Usuario_id`),
  CONSTRAINT `Discipline_Cliente_Discipline` FOREIGN KEY (`Discipline_id`) REFERENCES `discipline` (`id`),
  CONSTRAINT `Discipline_Cliente_Usuario` FOREIGN KEY (`Usuario_id`) REFERENCES `usuario` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `discipline_cliente`
--

LOCK TABLES `discipline_cliente` WRITE;
/*!40000 ALTER TABLE `discipline_cliente` DISABLE KEYS */;
INSERT INTO `discipline_cliente` VALUES (1,1,1),(2,2,1);
/*!40000 ALTER TABLE `discipline_cliente` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `discipline_instructor`
--

DROP TABLE IF EXISTS `discipline_instructor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `discipline_instructor` (
  `id` int NOT NULL AUTO_INCREMENT,
  `Discipline_id` int NOT NULL,
  `Usuario_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Discipline_Instructor_Discipline` (`Discipline_id`),
  KEY `Discipline_Instructor_Usuario` (`Usuario_id`),
  CONSTRAINT `Discipline_Instructor_Discipline` FOREIGN KEY (`Discipline_id`) REFERENCES `discipline` (`id`),
  CONSTRAINT `Discipline_Instructor_Usuario` FOREIGN KEY (`Usuario_id`) REFERENCES `usuario` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `discipline_instructor`
--

LOCK TABLES `discipline_instructor` WRITE;
/*!40000 ALTER TABLE `discipline_instructor` DISABLE KEYS */;
INSERT INTO `discipline_instructor` VALUES (1,1,2),(2,2,2),(3,2,3),(4,3,3);
/*!40000 ALTER TABLE `discipline_instructor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ejercicio`
--

DROP TABLE IF EXISTS `ejercicio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ejercicio` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `descripcion` text NOT NULL,
  `series` int NOT NULL,
  `repeticiones` int NOT NULL,
  `tiempo_descanso` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ejercicio`
--

LOCK TABLES `ejercicio` WRITE;
/*!40000 ALTER TABLE `ejercicio` DISABLE KEYS */;
INSERT INTO `ejercicio` VALUES (1,'Sentadillas','Ejercicio para piernas con peso corporal',3,15,60),(2,'Flexiones de pecho','Ejercicio para pectorales con peso corporal',3,12,60),(3,'Plancha','Ejercicio isométrico para core',3,30,45),(4,'Sentadillas','Ejercicio para piernas y glúteos',4,12,60),(5,'Press de banca','Ejercicio para pecho y tríceps',4,10,90),(6,'Peso muerto','Ejercicio para espalda baja y piernas',3,8,120),(7,'Dominadas','Ejercicio para espalda y bíceps',3,10,90),(8,'Flexiones de pecho','Ejercicio para pectoral y tríceps con peso corporal',3,15,60),(9,'Press militar','Ejercicio para hombros y tríceps',4,10,90),(10,'Remo con barra','Ejercicio para espalda media',3,12,90),(11,'Curl de bíceps','Ejercicio de aislamiento para bíceps',3,12,60),(12,'Extensiones de tríceps','Ejercicio de aislamiento para tríceps',3,15,60),(13,'Elevaciones laterales','Ejercicio para el deltoides lateral',3,15,45),(14,'Zancadas','Ejercicio unilateral para piernas',3,12,60),(15,'Prensa de piernas','Ejercicio para cuádriceps y glúteos en máquina',4,12,90),(16,'Extensiones de cuádriceps','Ejercicio de aislamiento para cuádriceps',3,15,60),(17,'Curl de isquiotibiales','Ejercicio de aislamiento para isquiotibiales',3,12,60),(18,'Elevaciones de gemelos','Ejercicio para pantorrillas',4,20,45),(19,'Burpees','Ejercicio cardiovascular de cuerpo completo',5,15,45),(20,'Mountain climbers','Ejercicio cardiovascular para core y resistencia',3,30,30),(21,'Jumping jacks','Ejercicio cardiovascular básico de calentamiento',3,30,30),(22,'Saltos de cuerda','Ejercicio cardiovascular para coordinación y resistencia',3,60,45),(23,'Sprint en el sitio','Ejercicio de alta intensidad para quemar calorías',5,20,40),(24,'Plancha','Ejercicio isométrico para core',3,30,45),(25,'Crunch abdominal','Ejercicio para abdominales superiores',3,20,30),(26,'Elevación de piernas','Ejercicio para abdominales inferiores',3,15,30),(27,'Russian twist','Ejercicio para oblicuos con rotación',3,20,30),(28,'Superman','Ejercicio para espalda baja y glúteos',3,15,30),(29,'Kettlebell swing','Ejercicio con pesa rusa para glúteos y espalda',3,20,45),(30,'Clean and jerk','Levantamiento olímpico completo',4,8,120),(31,'Box jumps','Saltos a caja para potencia de piernas',4,10,60),(32,'Battle ropes','Ejercicio con cuerdas para resistencia y fuerza',3,30,45),(33,'Medicine ball slam','Lanzamiento de balón medicinal para potencia',3,15,45);
/*!40000 ALTER TABLE `ejercicio` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ejercicio_rutina`
--

DROP TABLE IF EXISTS `ejercicio_rutina`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ejercicio_rutina` (
  `id` int NOT NULL AUTO_INCREMENT,
  `orden` int NOT NULL,
  `Ejercicio_id` int NOT NULL,
  `Rutina_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Ejercicio_Rutina_Ejercicio` (`Ejercicio_id`),
  KEY `Ejercicio_Rutina_Rutina` (`Rutina_id`),
  CONSTRAINT `Ejercicio_Rutina_Ejercicio` FOREIGN KEY (`Ejercicio_id`) REFERENCES `ejercicio` (`id`),
  CONSTRAINT `Ejercicio_Rutina_Rutina` FOREIGN KEY (`Rutina_id`) REFERENCES `rutina` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ejercicio_rutina`
--

LOCK TABLES `ejercicio_rutina` WRITE;
/*!40000 ALTER TABLE `ejercicio_rutina` DISABLE KEYS */;
INSERT INTO `ejercicio_rutina` VALUES (1,1,1,1),(2,2,2,1),(3,3,3,1),(4,1,3,2),(5,2,1,2);
/*!40000 ALTER TABLE `ejercicio_rutina` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `historial_medidas`
--

DROP TABLE IF EXISTS `historial_medidas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `historial_medidas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `peso` float NOT NULL,
  `altura` float NOT NULL,
  `imc` float NOT NULL,
  `fecha_medicion` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `Usuario_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Historial_Medidas_Usuario` (`Usuario_id`),
  CONSTRAINT `Historial_Medidas_Usuario` FOREIGN KEY (`Usuario_id`) REFERENCES `usuario` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `historial_medidas`
--

LOCK TABLES `historial_medidas` WRITE;
/*!40000 ALTER TABLE `historial_medidas` DISABLE KEYS */;
INSERT INTO `historial_medidas` VALUES (1,70.5,1.75,23,'2025-04-29 16:40:05',1),(2,70.5,1.75,230204,'2025-04-30 11:22:02',1),(3,90,190,24.93,'2025-04-30 11:49:45',10);
/*!40000 ALTER TABLE `historial_medidas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `instructor_datos`
--

DROP TABLE IF EXISTS `instructor_datos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `instructor_datos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `certificaciones` text NOT NULL,
  `estudios` text NOT NULL,
  `anios_experiencia` int NOT NULL,
  `especialidad` varchar(100) NOT NULL,
  `Usuario_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Instructor_datos_Usuario` (`Usuario_id`),
  CONSTRAINT `Instructor_datos_Usuario` FOREIGN KEY (`Usuario_id`) REFERENCES `usuario` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `instructor_datos`
--

LOCK TABLES `instructor_datos` WRITE;
/*!40000 ALTER TABLE `instructor_datos` DISABLE KEYS */;
INSERT INTO `instructor_datos` VALUES (1,'Certificado de Entrenador Personal','Licenciatura en Educación Física',5,'Entrenamiento funcional',2),(2,'Certificación en Nutrición Deportiva','Maestría en Ciencias del Deporte',8,'Nutrición deportiva',3),(3,'Certificado de Entrenador Personal','Licenciatura en Educación Física',5,'Entrenamiento funcional',2);
/*!40000 ALTER TABLE `instructor_datos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `instructor_products`
--

DROP TABLE IF EXISTS `instructor_products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `instructor_products` (
  `id` int NOT NULL AUTO_INCREMENT,
  `Product_id` int NOT NULL,
  `Usuario_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Instructor_Products_Products` (`Product_id`),
  KEY `Instructor_Products_Usuario` (`Usuario_id`),
  CONSTRAINT `Instructor_Products_Products` FOREIGN KEY (`Product_id`) REFERENCES `product` (`id`),
  CONSTRAINT `Instructor_Products_Usuario` FOREIGN KEY (`Usuario_id`) REFERENCES `usuario` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `instructor_products`
--

LOCK TABLES `instructor_products` WRITE;
/*!40000 ALTER TABLE `instructor_products` DISABLE KEYS */;
INSERT INTO `instructor_products` VALUES (2,2,3),(3,1,2),(4,3,2);
/*!40000 ALTER TABLE `instructor_products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `meta`
--

DROP TABLE IF EXISTS `meta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `meta` (
  `id` int NOT NULL AUTO_INCREMENT,
  `descripcion` text NOT NULL,
  `fecha_inicio` date NOT NULL,
  `fecha_fin` date NOT NULL,
  `estado` varchar(50) NOT NULL,
  `Usuario_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Meta_Usuario` (`Usuario_id`),
  CONSTRAINT `Meta_Usuario` FOREIGN KEY (`Usuario_id`) REFERENCES `usuario` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `meta`
--

LOCK TABLES `meta` WRITE;
/*!40000 ALTER TABLE `meta` DISABLE KEYS */;
INSERT INTO `meta` VALUES (1,'Perder 5kg en 3 meses','2023-05-01','2023-07-31','En progreso',1),(3,'Aumentar la pierna un de 30 a 35','2025-04-30','2025-04-30','En progreso',10);
/*!40000 ALTER TABLE `meta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product`
--

DROP TABLE IF EXISTS `product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) DEFAULT NULL,
  `category` int DEFAULT NULL,
  `description` text,
  `marca` varchar(100) NOT NULL,
  `purchase_price` double(10,2) DEFAULT NULL,
  `price` double(10,2) DEFAULT NULL,
  `descuento` double(10,2) DEFAULT NULL,
  `previous_price` double(10,2) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  `status` int NOT NULL DEFAULT '1',
  `relevant` int NOT NULL DEFAULT '0',
  `additional` varchar(200) DEFAULT NULL,
  `outstanding` int NOT NULL DEFAULT '1',
  `palabras_claves` text NOT NULL,
  `fecha_inicio` date DEFAULT NULL,
  `fecha_fin` date DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product`
--

LOCK TABLES `product` WRITE;
/*!40000 ALTER TABLE `product` DISABLE KEYS */;
INSERT INTO `product` VALUES (1,'Proteína Whey',1,'Proteína de suero de leche de alta calidad','FitPro',25.00,40.00,0.00,45.00,'2023-04-15',2,1,1,NULL,1,'proteina, suplemento, fitness','2023-04-15','2023-12-31'),(2,'Banda elástica',2,'Banda de resistencia para ejercicios','GymPlus',8.00,15.00,2.00,17.00,'2023-04-20',3,1,0,NULL,1,'banda, resistencia, ejercicio','2023-04-20','2023-12-31'),(3,'Proteina',1,'Proteina','Proteina',15.00,15.00,15.00,15.00,'2025-04-30',NULL,1,0,NULL,1,'Proteina','2025-04-30','2025-05-12');
/*!40000 ALTER TABLE `product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_images`
--

DROP TABLE IF EXISTS `product_images`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product_images` (
  `id` int NOT NULL AUTO_INCREMENT,
  `image_name` text NOT NULL,
  `color_id` int NOT NULL,
  `Product_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Product_images_Products` (`Product_id`),
  CONSTRAINT `Product_images_Products` FOREIGN KEY (`Product_id`) REFERENCES `product` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_images`
--

LOCK TABLES `product_images` WRITE;
/*!40000 ALTER TABLE `product_images` DISABLE KEYS */;
INSERT INTO `product_images` VALUES (1,'proteina1.jpg',1,1),(2,'proteina2.jpg',2,1),(3,'banda1.jpg',1,2),(4,'comida_1746032174_0.jpeg',0,3);
/*!40000 ALTER TABLE `product_images` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rutina`
--

DROP TABLE IF EXISTS `rutina`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rutina` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `descripcion` text NOT NULL,
  `fecha_creacion` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `Usuario_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Rutina_Usuario` (`Usuario_id`),
  CONSTRAINT `Rutina_Usuario` FOREIGN KEY (`Usuario_id`) REFERENCES `usuario` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rutina`
--

LOCK TABLES `rutina` WRITE;
/*!40000 ALTER TABLE `rutina` DISABLE KEYS */;
INSERT INTO `rutina` VALUES (1,'Rutina inicial','Rutina para principiantes con ejercicios básicos','2025-04-29 16:40:05',1),(2,'Rutina de pierna','Rutina de pierna','2025-04-30 11:35:02',10);
/*!40000 ALTER TABLE `rutina` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `seguimiento_imagen`
--

DROP TABLE IF EXISTS `seguimiento_imagen`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `seguimiento_imagen` (
  `id` int NOT NULL AUTO_INCREMENT,
  `Seguimiento_Progreso_id` int NOT NULL,
  `nombre_imagen` varchar(255) NOT NULL,
  `tipo` varchar(50) NOT NULL COMMENT 'antes, durante, después',
  `fecha_carga` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `Seguimiento_Imagen_Progreso` (`Seguimiento_Progreso_id`),
  CONSTRAINT `Seguimiento_Imagen_Progreso` FOREIGN KEY (`Seguimiento_Progreso_id`) REFERENCES `seguimiento_progreso` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `seguimiento_imagen`
--

LOCK TABLES `seguimiento_imagen` WRITE;
/*!40000 ALTER TABLE `seguimiento_imagen` DISABLE KEYS */;
INSERT INTO `seguimiento_imagen` VALUES (1,1,'Usuario_Vector_Avatar_PNG_dibujos_Clipart_Humano_Mujeres_Usuarias_Icono_PNG_y_Vector_para_Descargar_Gratis___Pngtree_1746030122.jpeg','durante','2025-04-30 11:22:02');
/*!40000 ALTER TABLE `seguimiento_imagen` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `seguimiento_progreso`
--

DROP TABLE IF EXISTS `seguimiento_progreso`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `seguimiento_progreso` (
  `id` int NOT NULL AUTO_INCREMENT,
  `Usuario_id` int NOT NULL,
  `fecha_seguimiento` date NOT NULL,
  `Rutina_id` int DEFAULT NULL,
  `Meta_id` int DEFAULT NULL,
  `Dieta_id` int DEFAULT NULL,
  `peso_actual` float DEFAULT NULL,
  `imc_actual` float DEFAULT NULL,
  `nivel_esfuerzo` int DEFAULT NULL COMMENT 'Escala 1-10',
  `rendimiento` int DEFAULT NULL COMMENT 'Escala 1-10',
  `ejercicios_completados` int DEFAULT NULL COMMENT 'Porcentaje completado',
  `adherencia_dieta` int DEFAULT NULL COMMENT 'Porcentaje de cumplimiento',
  `sensacion_hambre` int DEFAULT NULL COMMENT 'Escala 1-10',
  `energia_diaria` int DEFAULT NULL COMMENT 'Escala 1-10',
  `dificultades` text,
  `logros` text,
  `observaciones` text,
  `calificacion_instructor` int DEFAULT NULL COMMENT 'Escala 1-10',
  `instructor_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Seguimiento_Usuario` (`Usuario_id`),
  KEY `Seguimiento_Rutina` (`Rutina_id`),
  KEY `Seguimiento_Meta` (`Meta_id`),
  KEY `Seguimiento_Dieta` (`Dieta_id`),
  KEY `Seguimiento_Instructor` (`instructor_id`),
  CONSTRAINT `Seguimiento_Dieta` FOREIGN KEY (`Dieta_id`) REFERENCES `dieta` (`id`),
  CONSTRAINT `Seguimiento_Instructor` FOREIGN KEY (`instructor_id`) REFERENCES `usuario` (`id`),
  CONSTRAINT `Seguimiento_Meta` FOREIGN KEY (`Meta_id`) REFERENCES `meta` (`id`),
  CONSTRAINT `Seguimiento_Rutina` FOREIGN KEY (`Rutina_id`) REFERENCES `rutina` (`id`),
  CONSTRAINT `Seguimiento_Usuario` FOREIGN KEY (`Usuario_id`) REFERENCES `usuario` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `seguimiento_progreso`
--

LOCK TABLES `seguimiento_progreso` WRITE;
/*!40000 ALTER TABLE `seguimiento_progreso` DISABLE KEYS */;
INSERT INTO `seguimiento_progreso` VALUES (1,1,'2025-04-30',1,1,1,70.5,NULL,5,3,0,50,6,10,'al seguir la rutina','logro grandes mejoras ','un buen inicio',5,2);
/*!40000 ALTER TABLE `seguimiento_progreso` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `servicio`
--

DROP TABLE IF EXISTS `servicio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `servicio` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `descripcion` text NOT NULL,
  `precio` decimal(10,2) NOT NULL,
  `duracion` int NOT NULL COMMENT 'duración en minutos',
  `categoria` varchar(50) NOT NULL,
  `modalidad` varchar(50) NOT NULL,
  `nivel` varchar(50) NOT NULL,
  `imagen` varchar(255) DEFAULT NULL,
  `instructor_id` int NOT NULL,
  `estado` varchar(20) NOT NULL DEFAULT 'activo',
  `fecha_creacion` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `Discipline_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `instructor_id` (`instructor_id`),
  KEY `Servicio_Discipline` (`Discipline_id`),
  CONSTRAINT `Servicio_Discipline` FOREIGN KEY (`Discipline_id`) REFERENCES `discipline` (`id`),
  CONSTRAINT `servicio_ibfk_1` FOREIGN KEY (`instructor_id`) REFERENCES `usuario` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servicio`
--

LOCK TABLES `servicio` WRITE;
/*!40000 ALTER TABLE `servicio` DISABLE KEYS */;
INSERT INTO `servicio` VALUES (1,'Clases de musculación','Clases de musculación',30.00,60,'Entrenamiento','Virtual','Principiante','service_disenon_horarios_1746022174.png',2,'activo','2025-04-30 09:09:34',NULL);
/*!40000 ALTER TABLE `servicio` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `servicio_horario`
--

DROP TABLE IF EXISTS `servicio_horario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `servicio_horario` (
  `id` int NOT NULL AUTO_INCREMENT,
  `servicio_id` int NOT NULL,
  `dia_semana` varchar(20) NOT NULL COMMENT 'lunes, martes, etc.',
  `hora_inicio` time NOT NULL,
  `hora_fin` time NOT NULL,
  `cupos_disponibles` int NOT NULL DEFAULT '1',
  `estado` varchar(20) NOT NULL DEFAULT 'activo',
  PRIMARY KEY (`id`),
  KEY `servicio_id` (`servicio_id`),
  CONSTRAINT `servicio_horario_ibfk_1` FOREIGN KEY (`servicio_id`) REFERENCES `servicio` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servicio_horario`
--

LOCK TABLES `servicio_horario` WRITE;
/*!40000 ALTER TABLE `servicio_horario` DISABLE KEYS */;
INSERT INTO `servicio_horario` VALUES (1,1,'lunes','09:00:00','10:00:00',15,'activo');
/*!40000 ALTER TABLE `servicio_horario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `servicio_producto`
--

DROP TABLE IF EXISTS `servicio_producto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `servicio_producto` (
  `id` int NOT NULL AUTO_INCREMENT,
  `servicio_id` int NOT NULL,
  `producto_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `servicio_id` (`servicio_id`),
  KEY `producto_id` (`producto_id`),
  CONSTRAINT `servicio_producto_ibfk_1` FOREIGN KEY (`servicio_id`) REFERENCES `servicio` (`id`) ON DELETE CASCADE,
  CONSTRAINT `servicio_producto_ibfk_2` FOREIGN KEY (`producto_id`) REFERENCES `product` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servicio_producto`
--

LOCK TABLES `servicio_producto` WRITE;
/*!40000 ALTER TABLE `servicio_producto` DISABLE KEYS */;
/*!40000 ALTER TABLE `servicio_producto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `servicio_reserva`
--

DROP TABLE IF EXISTS `servicio_reserva`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `servicio_reserva` (
  `id` int NOT NULL AUTO_INCREMENT,
  `horario_id` int NOT NULL,
  `usuario_id` int NOT NULL,
  `fecha` date NOT NULL,
  `estado` varchar(20) NOT NULL DEFAULT 'pendiente',
  `fecha_reserva` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `comentarios` text,
  PRIMARY KEY (`id`),
  KEY `horario_id` (`horario_id`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `servicio_reserva_ibfk_1` FOREIGN KEY (`horario_id`) REFERENCES `servicio_horario` (`id`) ON DELETE CASCADE,
  CONSTRAINT `servicio_reserva_ibfk_2` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servicio_reserva`
--

LOCK TABLES `servicio_reserva` WRITE;
/*!40000 ALTER TABLE `servicio_reserva` DISABLE KEYS */;
/*!40000 ALTER TABLE `servicio_reserva` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tipo_usuario`
--

DROP TABLE IF EXISTS `tipo_usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tipo_usuario` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  `descripcion` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_usuario`
--

LOCK TABLES `tipo_usuario` WRITE;
/*!40000 ALTER TABLE `tipo_usuario` DISABLE KEYS */;
INSERT INTO `tipo_usuario` VALUES (1,'Cliente','Usuario que busca servicios de fitness'),(2,'Instructor','Profesional que ofrece servicios de fitness');
/*!40000 ALTER TABLE `tipo_usuario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuario`
--

DROP TABLE IF EXISTS `usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuario` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombres` varchar(100) NOT NULL,
  `apellidos` varchar(100) NOT NULL,
  `celular` varchar(15) NOT NULL,
  `email` varchar(150) NOT NULL,
  `contrasenia` varchar(100) NOT NULL,
  `status` int NOT NULL,
  `imagen` varchar(255) NOT NULL,
  `fecha_registro` datetime NOT NULL,
  `Tipo_usuario_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Usuario_Tipo_usuario` (`Tipo_usuario_id`),
  CONSTRAINT `Usuario_Tipo_usuario` FOREIGN KEY (`Tipo_usuario_id`) REFERENCES `tipo_usuario` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario`
--

LOCK TABLES `usuario` WRITE;
/*!40000 ALTER TABLE `usuario` DISABLE KEYS */;
INSERT INTO `usuario` VALUES (1,'Cliente','Ejemplo','1234567890','cliente@ejemplo.com','Cliente123!',1,'default_user.png','2025-04-29 16:40:05',1),(2,'Instructor','Ejemplo','0987654321','instructor@ejemplo.com','Instructor123!',1,'Usuario_Vector_Avatar_PNG_dibujos_Clipart_Humano_Mujeres_Usuarias_Icono_PNG_y_Vector_para_Descargar_Gratis___Pngtree_1746027421.jpeg','2025-04-29 16:40:05',2),(3,'Admin','Sistema','5555555555','admin@sistema.com','Admin123!',1,'default_user.png','2025-04-29 16:40:05',2),(10,'Carlos','Rodríguez','6641234567','carlos@ejemplo.com','password123',1,'default_user.png','2025-04-30 11:33:50',1),(11,'Ana','Martínez','6642345678','ana@ejemplo.com','password123',1,'default_user.png','2025-04-30 11:33:50',1),(12,'Miguel','López','6643456789','miguel@ejemplo.com','password123',1,'default_user.png','2025-04-30 11:33:50',1),(13,'Laura','Sánchez','6644567890','laura@ejemplo.com','password123',1,'default_user.png','2025-04-30 11:33:50',1),(14,'Javier','González','6645678901','javier@ejemplo.com','password123',1,'default_user.png','2025-04-30 11:33:50',1);
/*!40000 ALTER TABLE `usuario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'flaskcrud'
--

--
-- Dumping routines for database 'flaskcrud'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-30 21:10:28
