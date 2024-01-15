CREATE DATABASE IF NOT EXISTS Biotrace;

USE Biotrace;


CREATE TABLE IF NOT EXISTS`file` (
	`id` int PRIMARY KEY AUTO_INCREMENT,
	`type` ENUM ('log', 'config'),
	`nom` varchar(255),
	`content` blob,
	`created_at` date,
	`updated_at` date,
	`deleted_at` date COMMENT 'paranoid table'
);