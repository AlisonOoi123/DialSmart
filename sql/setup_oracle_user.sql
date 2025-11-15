-- DialSmart Oracle User Setup Script
-- For Oracle XE 11g
-- Run this script as SYSTEM user

-- Create tablespace for DialSmart data
CREATE TABLESPACE dialsmart_ts
DATAFILE 'dialsmart_data.dbf' SIZE 100M
AUTOEXTEND ON NEXT 10M MAXSIZE 500M;

-- Create DialSmart user
CREATE USER dialsmart_user IDENTIFIED BY dialsmart123
DEFAULT TABLESPACE dialsmart_ts
QUOTA UNLIMITED ON dialsmart_ts;

-- Grant necessary privileges
GRANT CONNECT TO dialsmart_user;
GRANT RESOURCE TO dialsmart_user;
GRANT CREATE SESSION TO dialsmart_user;
GRANT CREATE TABLE TO dialsmart_user;
GRANT CREATE VIEW TO dialsmart_user;
GRANT CREATE SEQUENCE TO dialsmart_user;
GRANT CREATE SYNONYM TO dialsmart_user;

-- Verify user was created
SELECT username, default_tablespace, account_status
FROM dba_users
WHERE username = 'DIALSMART_USER';

-- Show tablespace info
SELECT tablespace_name, file_name, bytes/1024/1024 as size_mb, autoextensible
FROM dba_data_files
WHERE tablespace_name = 'DIALSMART_TS';

-- Success message
SELECT 'User DIALSMART_USER created successfully!' AS status FROM dual;
