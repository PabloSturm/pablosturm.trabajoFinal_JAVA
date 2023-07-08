CREATE DATABASE  IF NOT EXISTS `tienda_vicky_gurumis` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `tienda_vicky_gurumis`;
-- MySQL dump 10.13  Distrib 8.0.33, for Win64 (x86_64)
--
-- Host: localhost    Database: tienda_vicky_gurumis
-- ------------------------------------------------------
-- Server version	8.0.33

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
-- Table structure for table `amigurumi`
--

DROP TABLE IF EXISTS `amigurumi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `amigurumi` (
  `idamigurumi` int NOT NULL AUTO_INCREMENT,
  `idproducto` int NOT NULL,
  `codigo` int NOT NULL,
  `nombre` varchar(20) NOT NULL,
  `descripcion` varchar(100) DEFAULT NULL,
  `precio` double DEFAULT NULL,
  PRIMARY KEY (`idamigurumi`),
  KEY `idproducto` (`idproducto`),
  CONSTRAINT `amigurumi_ibfk_1` FOREIGN KEY (`idproducto`) REFERENCES `producto` (`idproducto`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `amigurumi`
--

LOCK TABLES `amigurumi` WRITE;
/*!40000 ALTER TABLE `amigurumi` DISABLE KEYS */;
/*!40000 ALTER TABLE `amigurumi` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cliente`
--

DROP TABLE IF EXISTS `cliente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cliente` (
  `idcliente` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(20) NOT NULL,
  `apellido` varchar(20) NOT NULL,
  `edad` int NOT NULL,
  `cel` varchar(15) NOT NULL,
  `direccion` varchar(50) NOT NULL,
  `email` varchar(30) NOT NULL,
  `password` varchar(32) NOT NULL,
  PRIMARY KEY (`idcliente`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cliente`
--

LOCK TABLES `cliente` WRITE;
/*!40000 ALTER TABLE `cliente` DISABLE KEYS */;
/*!40000 ALTER TABLE `cliente` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `factura`
--

DROP TABLE IF EXISTS `factura`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `factura` (
  `idfactura` int NOT NULL AUTO_INCREMENT,
  `idcliente` int DEFAULT NULL,
  `fecha_emision` date DEFAULT NULL,
  PRIMARY KEY (`idfactura`),
  KEY `idcliente` (`idcliente`),
  CONSTRAINT `factura_ibfk_1` FOREIGN KEY (`idcliente`) REFERENCES `cliente` (`idcliente`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `factura`
--

LOCK TABLES `factura` WRITE;
/*!40000 ALTER TABLE `factura` DISABLE KEYS */;
/*!40000 ALTER TABLE `factura` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patron`
--

DROP TABLE IF EXISTS `patron`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `patron` (
  `idpatron` int NOT NULL AUTO_INCREMENT,
  `idproducto` int NOT NULL,
  `codigo` int NOT NULL,
  `nombre` varchar(20) NOT NULL,
  `descripcion` varchar(100) DEFAULT NULL,
  `precio` double DEFAULT NULL,
  PRIMARY KEY (`idpatron`),
  KEY `idproducto` (`idproducto`),
  CONSTRAINT `patron_ibfk_1` FOREIGN KEY (`idproducto`) REFERENCES `producto` (`idproducto`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patron`
--

LOCK TABLES `patron` WRITE;
/*!40000 ALTER TABLE `patron` DISABLE KEYS */;
/*!40000 ALTER TABLE `patron` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pedido`
--

DROP TABLE IF EXISTS `pedido`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pedido` (
  `idpedido` int NOT NULL AUTO_INCREMENT,
  `idcliente` int NOT NULL,
  `fecha` date DEFAULT NULL,
  `idproducto` int DEFAULT NULL,
  `cantidad_solicitada` int DEFAULT NULL,
  `precio` double DEFAULT NULL,
  `fecha_pedido` date DEFAULT NULL,
  `estado_pedido` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`idpedido`),
  KEY `idcliente` (`idcliente`),
  KEY `idproducto` (`idproducto`),
  CONSTRAINT `pedido_ibfk_1` FOREIGN KEY (`idcliente`) REFERENCES `cliente` (`idcliente`),
  CONSTRAINT `pedido_ibfk_2` FOREIGN KEY (`idproducto`) REFERENCES `producto` (`idproducto`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedido`
--

LOCK TABLES `pedido` WRITE;
/*!40000 ALTER TABLE `pedido` DISABLE KEYS */;
/*!40000 ALTER TABLE `pedido` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `producto`
--

DROP TABLE IF EXISTS `producto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `producto` (
  `idproducto` int NOT NULL AUTO_INCREMENT,
  `tipo` varchar(20) NOT NULL,
  PRIMARY KEY (`idproducto`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `producto`
--

LOCK TABLES `producto` WRITE;
/*!40000 ALTER TABLE `producto` DISABLE KEYS */;
/*!40000 ALTER TABLE `producto` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-07-07 20:44:03
