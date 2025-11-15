-- Update Oracle Column Sizes for Phone Specifications
-- Run this in SQL*Plus as ds_user to fix CSV import errors
--
-- Connect: sqlplus ds_user/dsuser123@localhost:1521/orclpdb

-- Display specifications
ALTER TABLE phone_specifications MODIFY screen_resolution VARCHAR2(150);
ALTER TABLE phone_specifications MODIFY screen_type VARCHAR2(200);
ALTER TABLE phone_specifications MODIFY protection VARCHAR2(200);

-- Camera specifications
ALTER TABLE phone_specifications MODIFY rear_camera VARCHAR2(500);
ALTER TABLE phone_specifications MODIFY front_camera VARCHAR2(200);

-- Network and Connectivity
ALTER TABLE phone_specifications MODIFY sim VARCHAR2(150);
ALTER TABLE phone_specifications MODIFY network_4g VARCHAR2(250);

-- Physical characteristics
ALTER TABLE phone_specifications MODIFY body_material VARCHAR2(300);

-- Verify all column changes
SELECT column_name, data_type, data_length, nullable
FROM user_tab_columns
WHERE table_name = 'PHONE_SPECIFICATIONS'
AND column_name IN ('SCREEN_RESOLUTION', 'SCREEN_TYPE', 'PROTECTION',
                     'REAR_CAMERA', 'FRONT_CAMERA',
                     'SIM', 'NETWORK_4G', 'BODY_MATERIAL')
ORDER BY column_name;

-- Success message
SELECT 'All column sizes updated successfully!' AS status FROM dual;
