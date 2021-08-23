/*
SQLyog Ultimate v11.11 (64 bit)
MySQL - 5.5.5-10.4.13-MariaDB : Database - ttdpdf
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
USE `ttdpdf`;

/*Table structure for table `authors` */

DROP TABLE IF EXISTS `authors`;

CREATE TABLE `authors` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `longname` varchar(255) NOT NULL,
  `prime1` int(11) DEFAULT NULL,
  `prime2` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`,`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;

/*Data for the table `authors` */

insert  into `authors`(`id`,`username`,`password`,`longname`,`prime1`,`prime2`) values (1,'test','123','test user',13,17);

/*Table structure for table `commons` */

DROP TABLE IF EXISTS `commons`;

CREATE TABLE `commons` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `tgl_lahir` date DEFAULT NULL,
  PRIMARY KEY (`id`,`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;

/*Data for the table `commons` */

insert  into `commons`(`id`,`username`,`password`,`name`,`tgl_lahir`) values (1,'made','555','Made Mas Adi','1997-08-05');

/*Table structure for table `files` */

DROP TABLE IF EXISTS `files`;

CREATE TABLE `files` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `filename` text DEFAULT NULL,
  `md5hash` text DEFAULT NULL,
  `privkey1` text DEFAULT NULL,
  `privkey2` text DEFAULT NULL,
  `pubkey1` text DEFAULT NULL,
  `pubkey2` text DEFAULT NULL,
  `owner_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;

/*Data for the table `files` */

insert  into `files`(`id`,`filename`,`md5hash`,`privkey1`,`privkey2`,`pubkey1`,`pubkey2`,`owner_id`) values (1,'lappembatalan','e45f9aae5f1f4daf1c5e427f4f48d176','113','221','17','221',1),(2,'rekapdrdperwilayah','57295b3b20bdb234d5cd94506e0f8d98','133','221','13','221',1);

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
