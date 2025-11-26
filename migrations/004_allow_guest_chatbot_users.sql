-- Step 2a: Add temporary nullable column
ALTER TABLE chat_history ADD user_id_new NUMBER(38) NULL;

-- Step 2b: Copy data from old column to new
UPDATE chat_history SET user_id_new = user_id;
COMMIT;

-- Step 2c: Drop the old NOT NULL constraint and column
ALTER TABLE chat_history DROP CONSTRAINT fk_chat_user;
ALTER TABLE chat_history DROP COLUMN user_id;

-- Step 2d: Rename new column to original name
ALTER TABLE chat_history RENAME COLUMN user_id_new TO user_id;

-- Step 2e: Re-add foreign key constraint (without NOT NULL)
ALTER TABLE chat_history 
ADD CONSTRAINT fk_chat_user 
FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE;

-- Step 2f: Add comment
COMMENT ON COLUMN chat_history.user_id IS 'User ID (NULL for guest/non-logged in users)';

COMMIT;