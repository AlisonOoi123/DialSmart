-- Update Oracle Column Sizes for Camera Specifications
-- Run this in SQL*Plus as ds_user to fix CSV import errors
--
-- Connect: sqlplus ds_user/dsuser123@localhost:1521/orclpdb

-- Increase rear_camera column size (200 -> 500 chars)
ALTER TABLE phone_specifications MODIFY rear_camera VARCHAR2(500);

-- Increase front_camera column size (100 -> 200 chars)
ALTER TABLE phone_specifications MODIFY front_camera VARCHAR2(200);

-- Verify column changes
SELECT column_name, data_type, data_length, nullable
FROM user_tab_columns
WHERE table_name = 'PHONE_SPECIFICATIONS'
AND column_name IN ('REAR_CAMERA', 'FRONT_CAMERA')
ORDER BY column_name;

-- Success message
SELECT 'Column sizes updated successfully!' AS status FROM dual;
