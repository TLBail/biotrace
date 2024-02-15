DELIMITER //

CREATE TRIGGER file_insert_update_trigger
AFTER INSERT OR UPDATE ON file
FOR EACH ROW
BEGIN
    DECLARE X_rows INT;
    SET X_rows = 10; -- Change this to the desired number of rows

    IF NEW.deletedAt IS NULL THEN
        -- Count the total number of rows where deletedAt is null
        SET @total_null_rows = (SELECT COUNT(*) FROM file WHERE deletedAt IS NULL);

        IF @total_null_rows > X_rows THEN
            -- Update the oldest row with deletedAt not null
            UPDATE file
            SET deletedAt = NOW()
            WHERE deletedAt IS NOT NULL
            ORDER BY createdAt
            LIMIT 1;
        ELSE
            -- Update the youngest row with deletedAt not null and set it to NULL
            UPDATE file
            SET deletedAt = NULL
            WHERE deletedAt IS NOT NULL
            ORDER BY createdAt DESC
            LIMIT 1;
        END IF;
    END IF;
END //