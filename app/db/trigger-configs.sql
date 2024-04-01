USE Biotrace;

DELIMITER //

CREATE OR REPLACE PROCEDURE update_file_trigger_logic()
BEGIN
    DECLARE X_rows INT;
    SET X_rows = 10; -- Change this to the desired number of rows

    IF NEW.deleted_at IS NULL THEN
        -- Count the total number of rows where deletedAt is null
        SET @total_null_rows = (SELECT COUNT(*) FROM file WHERE deleted_at IS NULL);

        IF @total_null_rows > X_rows THEN
            -- Update the oldest row with deletedAt not null
            UPDATE file
            SET deleted_at = NOW()
            WHERE deleted_at IS NOT NULL
            ORDER BY createdAt
            LIMIT 1;
        ELSE
            -- Update the youngest row with deletedAt not null and set it to NULL
            UPDATE file
            SET deleted_at = NULL
            WHERE deleted_at IS NOT NULL
            ORDER BY createdAt DESC
            LIMIT 1;
        END IF;
    END IF;
END//

CREATE TRIGGER file_insert_trigger
AFTER INSERT ON file
FOR EACH ROW
BEGIN
    CALL update_file_trigger_logic();
END//

CREATE TRIGGER file_update_trigger
AFTER UPDATE ON file
FOR EACH ROW
BEGIN
    CALL update_file_trigger_logic();
END//

DELIMITER ;