CREATE DATABASE IF NOT EXISTS Biotrace;

USE Biotrace;

-- TODO: Change in prod
CREATE USER IF NOT EXISTS 'dev' @'localhost' IDENTIFIED BY 'dev';

GRANT ALL PRIVILEGES ON Biotrace.* TO 'dev' @'localhost';

CREATE TABLE IF NOT EXISTS `file` (
	`id` int PRIMARY KEY AUTO_INCREMENT,
	`type` ENUM ('log', 'config') NOT NULL,
	`name` varchar(255) NOT NULL,
	`content` BLOB NOT NULL,
	`created_at` datetime DEFAULT NOW() NOT NULL,
	`updated_at` datetime DEFAULT NOW() NOT NULL,
	`deleted_at` datetime COMMENT 'paranoid table' DEFAULT NULL
);
