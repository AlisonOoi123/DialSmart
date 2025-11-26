--------------------------------------------------------------------------------
-- DialSmart: Drop All Tables and Sequences
-- Purpose: Clean the database completely before fresh setup
-- Usage: Run this in SQL*Plus as: @sql/01_drop_all_tables.sql
--------------------------------------------------------------------------------

SET ECHO ON
SET SERVEROUTPUT ON

PROMPT ================================================================================
PROMPT Dropping All DialSmart Tables and Sequences
PROMPT ================================================================================
PROMPT

-- Drop tables in correct order (child tables first due to foreign keys)
PROMPT Dropping child tables first...

DROP TABLE user_preferences CASCADE CONSTRAINTS;
DROP TABLE recommendations CASCADE CONSTRAINTS;
DROP TABLE phone_specifications CASCADE CONSTRAINTS;
DROP TABLE phones CASCADE CONSTRAINTS;
DROP TABLE comparisons CASCADE CONSTRAINTS;
DROP TABLE chat_history CASCADE CONSTRAINTS;
DROP TABLE chat_history_backup CASCADE CONSTRAINTS;
DROP TABLE contact_messages CASCADE CONSTRAINTS;
DROP TABLE audit_logs CASCADE CONSTRAINTS;
DROP TABLE brands CASCADE CONSTRAINTS;
DROP TABLE users CASCADE CONSTRAINTS;
DROP TABLE admins CASCADE CONSTRAINTS;

PROMPT

PROMPT Dropping sequences...

DROP SEQUENCE user_preferences_seq;
DROP SEQUENCE recommendations_seq;
DROP SEQUENCE phone_specifications_seq;
DROP SEQUENCE phones_seq;
DROP SEQUENCE comparisons_seq;
DROP SEQUENCE chat_history_seq;
DROP SEQUENCE contact_messages_seq;
DROP SEQUENCE audit_logs_seq;
DROP SEQUENCE brands_seq;
DROP SEQUENCE users_seq;

PROMPT

PROMPT ================================================================================
PROMPT All tables and sequences dropped successfully!
PROMPT ================================================================================
PROMPT

-- Verify tables are dropped
PROMPT Remaining tables (should be empty):
SELECT table_name FROM user_tables ORDER BY table_name;

PROMPT
PROMPT Remaining sequences (should be empty):
SELECT sequence_name FROM user_sequences ORDER BY sequence_name;
