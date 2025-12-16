-- Add Status column to Shelfloc table to track availability
USE datatech;

-- Add Status column (Available, Sold, Reserved, etc.)
ALTER TABLE Shelfloc ADD COLUMN Status VARCHAR(50) DEFAULT 'Available';

-- Set all existing shelf locations to Available
UPDATE Shelfloc SET Status = 'Available';

-- Verify the changes
SELECT * FROM Shelfloc;
