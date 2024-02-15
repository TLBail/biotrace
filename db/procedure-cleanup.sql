DELIMITER //

CREATE PROCEDURE daily_file_cleanup(IN X_days INT)
BEGIN
    UPDATE file
    SET deletedAt = NOW()
    WHERE deletedAt IS NOT NULL
      AND createdAt < NOW() - INTERVAL X_days DAY;
END //

CREATE EVENT IF NOT EXISTS daily_cleanup_event
ON SCHEDULE EVERY 1 DAY
DO
BEGIN
    CALL daily_file_cleanup(10);
END //

DELIMITER ;