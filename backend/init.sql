DELIMITER $$

DROP PROCEDURE IF EXISTS `initialize_database`$$
CREATE PROCEDURE initialize_database()
BEGIN
    -- Create the book table if it doesn't exist
    CREATE TABLE IF NOT EXISTS book (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        author VARCHAR(255) NOT NULL,
        read_status BOOLEAN DEFAULT FALSE
    );

    -- Check if the column already exists
    IF NOT EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_name = 'book' AND column_name = 'year'
    ) THEN
        -- Add the 'year' column to the 'book' table
      	ALTER TABLE book ADD COLUMN year INT;
    END IF;
END$$

DELIMITER ;
CALL initialize_database();
DROP PROCEDURE IF EXISTS `initialize_database`;
