# ************************************************************
# Sequel Pro SQL dump
# Version 4541
#
# http://www.sequelpro.com/
# https://github.com/sequelpro/sequelpro
#
# Host: 127.0.0.1 (MySQL 5.5.5-10.0.26-MariaDB-0+deb8u1)
# Database: weather
# Generation Time: 2016-09-10 18:57:54 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table bme280
# ------------------------------------------------------------

CREATE TABLE `bme280` (
  `date_tIme` datetime NOT NULL,
  `temperature` decimal(17,13) DEFAULT NULL,
  `pressure` decimal(15,11) DEFAULT NULL,
  `humidity` decimal(17,13) DEFAULT NULL,
  PRIMARY KEY (`date_tIme`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table bme280_daily
# ------------------------------------------------------------

CREATE TABLE `bme280_daily` (
  `date` date NOT NULL,
  `temperature_high` decimal(17,13) DEFAULT NULL,
  `temperature_low` decimal(17,13) DEFAULT NULL,
  `pressure_high` decimal(15,11) DEFAULT NULL,
  `pressure_low` decimal(15,11) DEFAULT NULL,
  `humidity_high` decimal(17,13) DEFAULT NULL,
  `humidity_low` decimal(17,13) DEFAULT NULL,
  PRIMARY KEY (`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table bme280_hourly
# ------------------------------------------------------------

CREATE TABLE `bme280_hourly` (
  `date_time` datetime NOT NULL,
  `temperature_high` decimal(17,13) DEFAULT NULL,
  `temperature_low` decimal(17,13) DEFAULT NULL,
  `pressure_high` decimal(15,11) DEFAULT NULL,
  `pressure_low` decimal(15,11) DEFAULT NULL,
  `humidity_high` decimal(17,13) DEFAULT NULL,
  `humidity_low` decimal(17,13) DEFAULT NULL,
  PRIMARY KEY (`date_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;




/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
