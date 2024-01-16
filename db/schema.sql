CREATE DATABASE IF NOT EXISTS Biotrace;

USE Biotrace;

-- TODO: Change in prod
CREATE USER IF NOT EXISTS 'dev'@'localhost' IDENTIFIED BY 'dev';

GRANT ALL PRIVILEGES ON Biotrace.* to 'dev'@'localhost';


CREATE TABLE IF NOT EXISTS `file` (
	`id` int PRIMARY KEY AUTO_INCREMENT,
	`type` ENUM ('log', 'config'),
	`name` varchar(255),
	`content` blob,
	`created_at` date,
	`updated_at` date,
	`deleted_at` date COMMENT 'paranoid table'
);