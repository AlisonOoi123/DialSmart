-- Migration: Add admin management columns to users table
-- Date: 2025-11-19
-- Description: Adds columns for secure admin management system

-- Add new columns to users table
ALTER TABLE users ADD (
    force_password_change NUMBER(1) DEFAULT 0,
    created_by_admin_id NUMBER(10),
    last_password_change TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Add foreign key constraint for created_by_admin_id
ALTER TABLE users ADD CONSTRAINT fk_users_created_by_admin
    FOREIGN KEY (created_by_admin_id) REFERENCES users(id);

-- Add comment for documentation
COMMENT ON COLUMN users.force_password_change IS 'Force password change on next login (0=false, 1=true)';
COMMENT ON COLUMN users.created_by_admin_id IS 'ID of admin who created this admin account';
COMMENT ON COLUMN users.last_password_change IS 'Timestamp of last password change';

-- Update existing users to have last_password_change set to their created_at date
UPDATE users SET last_password_change = created_at WHERE last_password_change IS NULL;

COMMIT;
