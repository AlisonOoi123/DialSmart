--------------------------------------------------------------------------------
-- DialSmart: Complete Database Structure Documentation
-- Generated: 2025-11-19
-- This script describes ALL tables in the database
--------------------------------------------------------------------------------

SET LINESIZE 200
SET PAGESIZE 1000
SET LONG 10000

PROMPT ================================================================================
PROMPT DialSmart Database - Complete Table Structure
PROMPT ================================================================================
PROMPT
PROMPT Total Tables: 12
PROMPT

PROMPT ================================================================================
PROMPT 1. ADMINS Table
PROMPT ================================================================================
DESC admins;

PROMPT ================================================================================
PROMPT 2. AUDIT_LOGS Table
PROMPT ================================================================================
DESC audit_logs;

PROMPT ================================================================================
PROMPT 3. BRANDS Table
PROMPT ================================================================================
DESC brands;

PROMPT ================================================================================
PROMPT 4. CHAT_HISTORY Table
PROMPT ================================================================================
DESC chat_history;

PROMPT ================================================================================
PROMPT 5. CHAT_HISTORY_BACKUP Table (Backup - Can be dropped)
PROMPT ================================================================================
DESC chat_history_backup;

PROMPT ================================================================================
PROMPT 6. COMPARISONS Table
PROMPT ================================================================================
DESC comparisons;

PROMPT ================================================================================
PROMPT 7. CONTACT_MESSAGES Table
PROMPT ================================================================================
DESC contact_messages;

PROMPT ================================================================================
PROMPT 8. PHONES Table
PROMPT ================================================================================
DESC phones;

PROMPT ================================================================================
PROMPT 9. PHONE_SPECIFICATIONS Table
PROMPT ================================================================================
DESC phone_specifications;

PROMPT ================================================================================
PROMPT 10. RECOMMENDATIONS Table
PROMPT ================================================================================
DESC recommendations;

PROMPT ================================================================================
PROMPT 11. USERS Table
PROMPT ================================================================================
DESC users;

PROMPT ================================================================================
PROMPT 12. USER_PREFERENCES Table
PROMPT ================================================================================
DESC user_preferences;

PROMPT
PROMPT ================================================================================
PROMPT Table Relationships (Foreign Keys)
PROMPT ================================================================================

SELECT 
    c.table_name,
    c.constraint_name,
    cc.column_name,
    r.table_name as references_table,
    rc.column_name as references_column
FROM user_constraints c
JOIN user_cons_columns cc ON c.constraint_name = cc.constraint_name
LEFT JOIN user_constraints r ON c.r_constraint_name = r.constraint_name
LEFT JOIN user_cons_columns rc ON r.constraint_name = rc.constraint_name
WHERE c.constraint_type = 'R'
ORDER BY c.table_name, c.constraint_name;

PROMPT
PROMPT ================================================================================
PROMPT Data Counts
PROMPT ================================================================================

SELECT 'ADMINS' as table_name, COUNT(*) as row_count FROM admins
UNION ALL SELECT 'AUDIT_LOGS', COUNT(*) FROM audit_logs
UNION ALL SELECT 'BRANDS', COUNT(*) FROM brands
UNION ALL SELECT 'CHAT_HISTORY', COUNT(*) FROM chat_history
UNION ALL SELECT 'CHAT_HISTORY_BACKUP', COUNT(*) FROM chat_history_backup
UNION ALL SELECT 'COMPARISONS', COUNT(*) FROM comparisons
UNION ALL SELECT 'CONTACT_MESSAGES', COUNT(*) FROM contact_messages
UNION ALL SELECT 'PHONES', COUNT(*) FROM phones
UNION ALL SELECT 'PHONE_SPECIFICATIONS', COUNT(*) FROM phone_specifications
UNION ALL SELECT 'RECOMMENDATIONS', COUNT(*) FROM recommendations
UNION ALL SELECT 'USERS', COUNT(*) FROM users
UNION ALL SELECT 'USER_PREFERENCES', COUNT(*) FROM user_preferences;

PROMPT
PROMPT ================================================================================
PROMPT Sequences
PROMPT ================================================================================

SELECT sequence_name, last_number, increment_by
FROM user_sequences
ORDER BY sequence_name;