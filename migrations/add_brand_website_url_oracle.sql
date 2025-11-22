-- Migration for Oracle Database: Add website_url column to brands table
-- Date: 2025-11-22
-- Description: Add a website_url field to store brand official website URLs

-- Add the column
ALTER TABLE brands ADD website_url VARCHAR2(500);

-- Commit the change
COMMIT;

-- Verify the column was added
DESC brands;

-- Optional: Update common brands with their website URLs
-- Uncomment and run these if you want to populate sample data
/*
UPDATE brands SET website_url = 'https://www.apple.com' WHERE UPPER(name) = 'APPLE';
UPDATE brands SET website_url = 'https://www.samsung.com' WHERE UPPER(name) = 'SAMSUNG';
UPDATE brands SET website_url = 'https://www.huawei.com' WHERE UPPER(name) = 'HUAWEI';
UPDATE brands SET website_url = 'https://www.mi.com' WHERE UPPER(name) = 'XIAOMI';
UPDATE brands SET website_url = 'https://www.nokia.com' WHERE UPPER(name) = 'NOKIA';
UPDATE brands SET website_url = 'https://www.oppo.com' WHERE UPPER(name) = 'OPPO';
UPDATE brands SET website_url = 'https://www.vivo.com' WHERE UPPER(name) = 'VIVO';
UPDATE brands SET website_url = 'https://www.realme.com' WHERE UPPER(name) IN ('REALME', 'REALME');
UPDATE brands SET website_url = 'https://www.oneplus.com' WHERE UPPER(name) = 'ONEPLUS';
UPDATE brands SET website_url = 'https://store.google.com' WHERE UPPER(name) = 'GOOGLE';
UPDATE brands SET website_url = 'https://www.motorola.com' WHERE UPPER(name) = 'MOTOROLA';
UPDATE brands SET website_url = 'https://www.sony.com' WHERE UPPER(name) = 'SONY';
UPDATE brands SET website_url = 'https://www.lg.com' WHERE UPPER(name) = 'LG';
UPDATE brands SET website_url = 'https://www.hihonor.com' WHERE UPPER(name) = 'HONOR';
UPDATE brands SET website_url = 'https://www.lenovo.com' WHERE UPPER(name) = 'LENOVO';
UPDATE brands SET website_url = 'https://www.asus.com' WHERE UPPER(name) = 'ASUS';
UPDATE brands SET website_url = 'https://www.htc.com' WHERE UPPER(name) = 'HTC';
UPDATE brands SET website_url = 'https://www.blackberry.com' WHERE UPPER(name) = 'BLACKBERRY';
COMMIT;

-- Verify the updates
SELECT name, website_url FROM brands WHERE website_url IS NOT NULL;
*/
