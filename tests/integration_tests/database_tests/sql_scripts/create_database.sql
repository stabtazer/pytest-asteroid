CREATE DATABASE IF NOT EXISTS `superheroes`;

USE `superheroes`;


DROP TABLE IF EXISTS `superheroes`;
CREATE TABLE `superheroes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `cape` tinyint(1),
  `height_cm` int(4),
  `weigth_kg` int(4),
  PRIMARY KEY (`id`)
);

DROP TABLE IF EXISTS `associations`;
CREATE TABLE `associations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
);

DROP TABLE IF EXISTS `member_of`;
CREATE TABLE `member_of` (
  `superhero_id` int(11) NOT NULL,
  `associations_id` int(11) NOT NULL,
  PRIMARY KEY (`superhero_id`, `associations_id`),
  CONSTRAINT `fk_member_of_superhero_id` FOREIGN KEY (`superhero_id`) REFERENCES `superheroes` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_member_of_associations_id` FOREIGN KEY (`associations_id`) REFERENCES `associations` (`id`) ON DELETE CASCADE
);

DROP TABLE IF EXISTS `powers`;
CREATE TABLE `powers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `Description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
);

DROP TABLE IF EXISTS `superhero_powers`;
CREATE TABLE `superhero_powers` (
  `superhero_id` int(11) NOT NULL,
  `power_id` int(11) NOT NULL,
  PRIMARY KEY (`superhero_id`, `power_id`),
  CONSTRAINT `fk_superhero_powers_superhero_id` FOREIGN KEY (`superhero_id`) REFERENCES `superheroes` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_superhero_powers_power_id` FOREIGN KEY (`power_id`) REFERENCES `powers` (`id`) ON DELETE CASCADE
);
