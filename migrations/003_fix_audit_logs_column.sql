-- Migration: Fix audit_logs column name mismatch
-- Date: 2025-11-19
-- Description: Rename chat_metadata to extra_data to match Python model

-- Rename column from chat_metadata to extra_data
ALTER TABLE audit_logs RENAME COLUMN chat_metadata TO extra_data;

-- Update comment
COMMENT ON COLUMN audit_logs.extra_data IS 'Additional data stored as JSON';

COMMIT;
