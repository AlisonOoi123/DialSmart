-- Populate brand website URLs for Oracle Database
-- Run this AFTER running add_brand_website_url_oracle.sql

-- Update all required smartphone brands with their official website URLs
-- Priority Brands (as specified by user)
UPDATE brands SET website_url = 'https://www.apple.com' WHERE UPPER(name) = 'APPLE';
UPDATE brands SET website_url = 'https://www.asus.com' WHERE UPPER(name) = 'ASUS';
UPDATE brands SET website_url = 'https://store.google.com' WHERE UPPER(name) = 'GOOGLE';
UPDATE brands SET website_url = 'https://www.hihonor.com' WHERE UPPER(name) = 'HONOR';
UPDATE brands SET website_url = 'https://www.huawei.com' WHERE UPPER(name) = 'HUAWEI';
UPDATE brands SET website_url = 'https://www.infinixmobility.com' WHERE UPPER(name) = 'INFINIX';
UPDATE brands SET website_url = 'https://www.oppo.com' WHERE UPPER(name) = 'OPPO';
UPDATE brands SET website_url = 'https://www.poco.net' WHERE UPPER(name) = 'POCO';
UPDATE brands SET website_url = 'https://www.mi.com/redmi' WHERE UPPER(name) = 'REDMI';
UPDATE brands SET website_url = 'https://www.realme.com' WHERE UPPER(name) = 'REALME';
UPDATE brands SET website_url = 'https://www.samsung.com' WHERE UPPER(name) = 'SAMSUNG';
UPDATE brands SET website_url = 'https://www.vivo.com' WHERE UPPER(name) = 'VIVO';
UPDATE brands SET website_url = 'https://www.mi.com' WHERE UPPER(name) = 'XIAOMI';

-- Additional Common Brands
UPDATE brands SET website_url = 'https://www.oneplus.com' WHERE UPPER(name) = 'ONEPLUS';
UPDATE brands SET website_url = 'https://www.nokia.com' WHERE UPPER(name) = 'NOKIA';
UPDATE brands SET website_url = 'https://www.motorola.com' WHERE UPPER(name) = 'MOTOROLA';
UPDATE brands SET website_url = 'https://www.sony.com' WHERE UPPER(name) = 'SONY';
UPDATE brands SET website_url = 'https://www.lg.com' WHERE UPPER(name) = 'LG';
UPDATE brands SET website_url = 'https://www.lenovo.com' WHERE UPPER(name) = 'LENOVO';
UPDATE brands SET website_url = 'https://www.htc.com' WHERE UPPER(name) = 'HTC';
UPDATE brands SET website_url = 'https://www.blackberry.com' WHERE UPPER(name) = 'BLACKBERRY';
UPDATE brands SET website_url = 'https://www.tecno-mobile.com' WHERE UPPER(name) = 'TECNO';

COMMIT;

-- Display the updated brands
SELECT name, website_url FROM brands WHERE website_url IS NOT NULL ORDER BY name;

-- Show row count
SELECT COUNT(*) as "Brands with URLs" FROM brands WHERE website_url IS NOT NULL;
