USE Biotrace;

CREATE USER IF NOT EXISTS 'dev' @'localhost' IDENTIFIED BY 'dev';

GRANT ALL PRIVILEGES ON Biotrace.* TO 'dev' @'localhost';