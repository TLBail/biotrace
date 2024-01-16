-- CREATE TABLE IF NOT EXISTS `file` (
-- 	`id` int PRIMARY KEY AUTO_INCREMENT,
-- 	`type` ENUM ('log', 'config'),
-- 	`name` varchar(255),
-- 	`content` blob,
-- 	`created_at` date,
-- 	`updated_at` date,
-- 	`deleted_at` date COMMENT 'paranoid table'
-- );

USE Biotrace;

INSERT INTO file (type, name, content, created_at, updated_at, deleted_at) VALUES
('log', 'test_log1', 'dGVzdA==', now(), now(), NULL),
('config', 'test_config1','IyBUaGlzIGlzIGEgY29tbWVudA0KW2dlbmVyYWxdDQojIFRoZSBuYW1lIG9mIHRoZSB3ZWJkeW4NCm5hbWUgPSAiVGVzdCBjb25maWciDQojIFRoZSBpcCBhZGRyZXNzIG9mIHRoZSB3ZWJkeW4NCmlwID0gIg0KIyBUaGlzIGlzIGEgY29tbWVudA0KW2dlbmVyYWxdDQojIFRoZSBuYW1lIG9mIHRoZSB3ZWJkeW4NCm5hbWUgPSAid2ViZHluIg0KIyBUaGUgaXAgYWRkcmVzcyBvZiB0aGUgd2ViZHluDQppcCA9ICINCiMgVGhpcyBpcyBhIGNvbW1lbnQNCltnZW5lcmFsXQ0KIyBUaGUgbmFtZSBvZiB0aGUgd2ViZHluDQpuYW1lID0gIndlYmR5biINCiMgVGhlIGlwIGFkZHJlc3Mgb2YgdGhlIHdlYmR5bg0KaXAgPSAiDQojIFRoaXMgaXMgYSBjb21tZW50DQpbZ2VuZXJhbF0NCiMgVGhlIG5hbWUgb2YgdGhlIHdlYmR5bg0KbmFtZSA9ICJ3ZWJkeW4iDQojIFRoZSBpcCBhZGRyZXNzIG9mIHRoZSB3ZWJkeW4NCmlwID0gIg0KIyBUaGlzIGlzIGEgY29tbWVudA0KW2dlbmVyYWxdDQojIFRoZSBuYW1lIG9mIHRoZSB3ZWJkeW4NCm5hbWUgPSAid2ViZHluIg0KIyBUaGUgaXAgYWRkcmVzcyBvZiB0aGUgd2ViZHluDQppcCA9ICINCiMgVGhpcyBpcyBhIGNvbW1lbnQNCltnZW5lcmFsXQ0KIyBUaGUgbmFtZSBvZiB0aGUgd2ViZHluDQpuYW1lID0gIndlYmR5biINCiMgVGhlIGlwIGFkZHJlc3Mgb2YgdGhlIHdlYmR5bg0KaXAgPSAiDQojIFRoaXMgaXMgYSBjb21tZW50DQpbZ2VuZXJhbF0NCiMgVGhlIG5hbWUgb2YgdGhlIHdlYmR5bg0KbmFtZSA9ICJ3ZWJkeW4iDQojIFRoZSBpcCBhZGRyZXNzIG9mIHRoZSB3ZWJkeW4NCmlwID0gIg0KIyBUaGlzIGlzIGEgY29tbWVudA0KW2dlbmVyYWxdDQojIFRoZSBuYW1lIG9mIHRoZSB3ZWJkeW4NCm5hbWUgPSAid2ViZHluIg0KIyBUaGUgaXAgYWRkcmVzcyBvZiB0aGUgd2ViZHluDQppcCA9ICINCiMgVGhpcyBpcyBhIGNvbW1lbnQNCltnZW5lcmFsXQ0KIyBUaGUgbmFtZSBvZiB0aGUgd2ViZHluDQpuYW1lID0gIndlYmR5biINCiMgVGhlIGlwIGFkZHJlc3Mgb2YgdGhlIHdlYmR5bg0KaXAgPSAi', now(), now(), NULL),
('log', 'test_log2', 'aGVsbG8=', now(), now(), NULL),
('config', 'test_config2','aGVsbG8=', now(), now(), NULL),
('config', 'test_config3','d29ybGQ=', now(), now(), NULL);