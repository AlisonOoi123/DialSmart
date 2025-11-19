-- Migration: Allow guest users to use chatbot
-- Date: 2025-11-19
-- Description: Change chat_history.user_id to nullable to allow guest (non-logged in) users

-- Modify user_id column to allow NULL values for guest users
ALTER TABLE chat_history MODIFY (user_id NUMBER(10) NULL);

-- Add comment for documentation
COMMENT ON COLUMN chat_history.user_id IS 'User ID (NULL for guest/non-logged in users)';

COMMIT;
