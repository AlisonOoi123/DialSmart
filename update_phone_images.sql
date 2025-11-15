-- SQL Script to Update Missing Phone Images
-- Generated from fyp_phoneDataset.csv
-- Run this in SQL*Plus

SET SERVEROUTPUT ON;
SET FEEDBACK ON;

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Apple-iPhone-15-Plus.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Apple')
      AND UPPER(p2.model_name) = UPPER('iPhone 15 Plus')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Apple-iPhone-15-Pro-Max_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Apple')
      AND UPPER(p2.model_name) = UPPER('iPhone 15 Pro Max')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Apple-iPhone-15-Pro.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Apple')
      AND UPPER(p2.model_name) = UPPER('iPhone 15 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Apple-iPhone-15.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Apple')
      AND UPPER(p2.model_name) = UPPER('iPhone 15')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Iphone-16-pro-ax.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Apple')
      AND UPPER(p2.model_name) = UPPER('iPhone 16 Pro Max')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Apple-iPhone-16-Plus_2.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Apple')
      AND UPPER(p2.model_name) = UPPER('iPhone 16 Plus')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Apple-iPhone-16-Pro_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Apple')
      AND UPPER(p2.model_name) = UPPER('iPhone 16 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Apple-Iphone-16_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Apple')
      AND UPPER(p2.model_name) = UPPER('iPhone 16')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Apple-iPhone-16e.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Apple')
      AND UPPER(p2.model_name) = UPPER('iPhone 16e')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/17-Air.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Apple')
      AND UPPER(p2.model_name) = UPPER('iPhone 17 Air')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Apple-iPhone-17-Pro-Max.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Apple')
      AND UPPER(p2.model_name) = UPPER('iPhone 17 Pro Max')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Apple-iPhone-17-Pro_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Apple')
      AND UPPER(p2.model_name) = UPPER('iPhone 17 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Apple-iPhone-17.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Apple')
      AND UPPER(p2.model_name) = UPPER('iPhone 17')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/asus-zenfone-10-official_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Asus')
      AND UPPER(p2.model_name) = UPPER('Zenfone 10Z')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/ASUS-Zenfone-11-Ultra-Official.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Asus')
      AND UPPER(p2.model_name) = UPPER('Zenfone 11 Ultra')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Asus-ROG-phone-8-Pro.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Asus')
      AND UPPER(p2.model_name) = UPPER('ROG Phone 8 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Asus-ROG-Phone-8.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Asus')
      AND UPPER(p2.model_name) = UPPER('Asus ROG Phone 8')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Asus-ROG-Phone-9.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Asus')
      AND UPPER(p2.model_name) = UPPER('ROG Phone 9')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Asus-ROG-Phone-9-Pro_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Asus')
      AND UPPER(p2.model_name) = UPPER('ROG Phone 9 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Asus-Zenfone-12-Ultra.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Asus')
      AND UPPER(p2.model_name) = UPPER('Zenfone 12 Ultra')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Asus-ROG-Phone-9-FE_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Asus')
      AND UPPER(p2.model_name) = UPPER('ROG Phone 9 FE')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Google-Pixel-8-Pro.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Google')
      AND UPPER(p2.model_name) = UPPER('Pixel 8 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Google-Pixel-8.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Google')
      AND UPPER(p2.model_name) = UPPER('Pixel 8')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Google-Pixel-9-Pro-XL.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Google')
      AND UPPER(p2.model_name) = UPPER('Pixel 9 Pro XL')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Google-Pixel-9.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Google')
      AND UPPER(p2.model_name) = UPPER('Pixel 9')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Pixel-8a.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Google')
      AND UPPER(p2.model_name) = UPPER('Pixel 8a')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Google-Pixel-9-Pro-Fold.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Google')
      AND UPPER(p2.model_name) = UPPER('Pixel 9 Pro Fold')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Google-Pixel-9-Pro_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Google')
      AND UPPER(p2.model_name) = UPPER('Pixel 9 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Google-Pixel-10-Pro-Fold_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Google')
      AND UPPER(p2.model_name) = UPPER('Pixel 10 Pro Fold')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Google-Pixel-10-Pro-XL_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Google')
      AND UPPER(p2.model_name) = UPPER('Pixel 10 Pro XL')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Google-Pixel-10-Pro_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Google')
      AND UPPER(p2.model_name) = UPPER('Pixel 10 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Google-Pixel-10_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Google')
      AND UPPER(p2.model_name) = UPPER('Pixel 10')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Google-Pixel-9a_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Google')
      AND UPPER(p2.model_name) = UPPER('Pixel 9A')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Honor-X8a-5G.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('X8A 5G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Honor-Play-7T-Pro.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('Honor Play 7T Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/honor-play7t.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('Play 7T')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/honor-x5-plus.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('X5 Plus')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/honor-90-gt.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('Honor 90 GT')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Honor-X7B.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('Honor X7b')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/honor-x8b.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('X8B')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Honor-Magic6-Lite.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('Magic6 Lite')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Honor-X5.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('X5')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/honor-x8a.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('Honor X8A')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Honor-80-Pro-Three-Body-Limited-Edition.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('Honor 80 Pro Three Body Limited Edition')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Honor-80-Pro-Flat-official.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('80 Pro 2023')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Honor-X7a.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('X7A')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Honor-X9A.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('Honor X9A')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Honor-Play-40C.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('Honor Play 40C')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/X6a.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('X6A')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Honor-X50i.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('X50i')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/honor-x50-5g.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('Honor X50')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Honor-90-Lite-official.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('Honor 90 Lite')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Honor-90-Pro.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('90 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Honor-90.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('90')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Honor-X6-5G.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('X6 5G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Honor-Play-40S.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('Honor Play 40S')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Honor-X50i-Plus.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('X50i Plus')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Honor-100-Pro-Official.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('100 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Honor-100-Official.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('100')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Honor-X9b.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('X9b')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Honor-Play-8T.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('Play 8T')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Magic-Vs2.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('Magic Vs2')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Honor-V-Purse.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('V Purse')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Honor-X40-gt-racing.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('X40 GT Racing')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/honor-90-smart-1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('90 Smart')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/honor-x7b-5g.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('X7b 5G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Honor-X60i.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('X60i')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Honor-Magic7-RSR-Porsche-Design.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('Magic7 RSR Porsche Design')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Honor-300-Ultra.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('300 Ultra')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Honor-GT_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('GT')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Honor-300-Pro.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('300 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Honor-300.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('300')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Honor-X50-Pro.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('X50 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Honor-Magic-6-official.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('Magic6')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/honor-magic6-pro_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('Magic6 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Honor-Magic-Vs3.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('Magic Vs3')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Honor-Magic-V3_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('Magic V3')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Honor-X6b.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('X6B')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Honor-Magic-V-Flip-official.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('Magic V Flip')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Honor-Play-60-Plus-1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('Play 60 Plus')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Honor-Magic6-RSR-Porsche-Design-Official.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('Magic6 RSR Porsche Design')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Honor-Magic6-Ultimate.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('Magic6 Ultimate')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Honor-Play-50m-Official.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('Honor Play 50m')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Honor-200-Lite_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('Honor 200 Lite 5G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Honor-200-Pro_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('200 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Honor-200.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('200')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Honor-X9c.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('X9C')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Honor-Magic7_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('Magic7')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Honor-Play9T.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('Play 9T')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Honor-Play9C.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('Play 9C')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Honor-X5b-Plus.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('X5b Plus')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Honor-X5b.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('X5b')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Honor-X60-Pro.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('X60 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Honor-X60_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('Honor X60')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Honor-X7c.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('Honor X7C')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Honor-200-Smart.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('200 Smart')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Honor-X70i.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('X70i')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Honor-Power.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('Power')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Honor-400-Lite.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('400 Lite')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Honor-X60-GT.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('X60 GT')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Honor-GT-Pro.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('GT Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Honor-Play-60.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('Play 60')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Honor-X7d-4G.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('Honor X7D 4G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Honor-Play10C.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('Play 10C')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Honor-Magic-V-Flip-2_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('Magic V Flip 2')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Honor-400-Smart.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('400 Smart')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Honor-X8c.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('X8C')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Honor-Magic7-Lite.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('Magic7 Lite')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Honor-X70.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('X70')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Honor-X6b_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('X6B')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/honor-x6c.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('X6C')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Honor-400-Pro.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('400 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Honor-400.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('400')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Honor-Magic8-Pro.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('Magic8 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Honor-Magic8_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('Magic 8')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Honor-Play10A.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('Play 10A')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Honor-X5c-Plus.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('X5c')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Honor-400-Smart-4G_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('400 Smart 4G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Honor-X9d.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('Honor X9D 5G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Honor-X7d.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('Honor X7D 5G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Honor-X5c-Plus_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Honor')
      AND UPPER(p2.model_name) = UPPER('X5c Plus')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Huawei-Nova-11-Ultra.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Huawei')
      AND UPPER(p2.model_name) = UPPER('Huawei nova 11 Ultra')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Huawei-Enjoy-60X.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Huawei')
      AND UPPER(p2.model_name) = UPPER('Huawei Enjoy 60X')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/huawei-nova-11-Pro.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Huawei')
      AND UPPER(p2.model_name) = UPPER('Huawei nova 11 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/huawei-nova-11-Official.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Huawei')
      AND UPPER(p2.model_name) = UPPER('Huawei nova 11')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Maimang-20.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Huawei')
      AND UPPER(p2.model_name) = UPPER('Maimang 20')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Huawei-P60-Art.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Huawei')
      AND UPPER(p2.model_name) = UPPER('P60 Art')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Huawei-Mate-60-Pro-official.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Huawei')
      AND UPPER(p2.model_name) = UPPER('Mate 60 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Huawei-Enjoy-70.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Huawei')
      AND UPPER(p2.model_name) = UPPER('Enjoy 70')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/huawei-nova-y91.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Huawei')
      AND UPPER(p2.model_name) = UPPER('Nova Y91')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Maimang-A20.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Huawei')
      AND UPPER(p2.model_name) = UPPER('Maimang A20')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Huawei-Nova-10-Youth-Edition.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Huawei')
      AND UPPER(p2.model_name) = UPPER('Nova 10 Youth Edition')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Huawei-Enjoy-60.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Huawei')
      AND UPPER(p2.model_name) = UPPER('Huawei Enjoy 60')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Huawei-Enjoy-60-Pro.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Huawei')
      AND UPPER(p2.model_name) = UPPER('Huawei Enjoy 60 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/huawei-nova-y71.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Huawei')
      AND UPPER(p2.model_name) = UPPER('Nova Y71')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Huawei-Nova-11i.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Huawei')
      AND UPPER(p2.model_name) = UPPER('Nova 11i')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Huawei-Mate-60-Pro-Lezhen-Edition.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Huawei')
      AND UPPER(p2.model_name) = UPPER('Mate 60 Pro Lezhen Edition')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Huawei-nova-11-SE.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Huawei')
      AND UPPER(p2.model_name) = UPPER('Nova 11 SE')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/huawei-mate-60.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Huawei')
      AND UPPER(p2.model_name) = UPPER('Mate 60')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/huawei-mate-x5.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Huawei')
      AND UPPER(p2.model_name) = UPPER('Mate X5')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/huawei-pura-70-pro.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Huawei')
      AND UPPER(p2.model_name) = UPPER('Pura 70 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/huawei-pura-70-red.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Huawei')
      AND UPPER(p2.model_name) = UPPER('Pura 70')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Huawei-Pura-70-Ultra.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Huawei')
      AND UPPER(p2.model_name) = UPPER('Pura 70 Ultra')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/P70-Pro-Plus-1024x576.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Huawei')
      AND UPPER(p2.model_name) = UPPER('Pura 70 Pro Plus')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Huawei-nova-Flip.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Huawei')
      AND UPPER(p2.model_name) = UPPER('Nova Flip')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/huawei-enjoy-70-1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Huawei')
      AND UPPER(p2.model_name) = UPPER('Nova Y72')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Huawei-Enjoy-70z.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Huawei')
      AND UPPER(p2.model_name) = UPPER('Enjoy 70z')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Vivo-Y62-Official.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Huawei')
      AND UPPER(p2.model_name) = UPPER('Nova Y62')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Huawei-Enjoy-70-Pro.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Huawei')
      AND UPPER(p2.model_name) = UPPER('Enjoy 70 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Huawei-Nova-12-Ultra_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Huawei')
      AND UPPER(p2.model_name) = UPPER('Nova 12 Ultra')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Huawei-Nova-12-Lite.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Huawei')
      AND UPPER(p2.model_name) = UPPER('Nova 12 Lite (Vitality Edition)')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Huwei-Nova-12-Pro.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Huawei')
      AND UPPER(p2.model_name) = UPPER('Nova 12 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Huwei-Nova-12.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Huawei')
      AND UPPER(p2.model_name) = UPPER('Nova 12')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Huawei-Nova-12-Lite_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Huawei')
      AND UPPER(p2.model_name) = UPPER('Nova 12s')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Huawei-Pocket-2.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Huawei')
      AND UPPER(p2.model_name) = UPPER('Pocket 2')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Huawei-nova-11-SE_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Huawei')
      AND UPPER(p2.model_name) = UPPER('Huawei Nova 12 SE')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Huawei-nova-12i.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Huawei')
      AND UPPER(p2.model_name) = UPPER('Huawei nova 12i')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Huawei-Enjoy-70s.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Huawei')
      AND UPPER(p2.model_name) = UPPER('Enjoy 70s')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Huawei-Mate-70-RS-Ultimate.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Huawei')
      AND UPPER(p2.model_name) = UPPER('Mate 70 RS Ultimate')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Huawei-Mate-X6.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Huawei')
      AND UPPER(p2.model_name) = UPPER('Mate X6')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Huawei-Mate-70-Pro_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Huawei')
      AND UPPER(p2.model_name) = UPPER('Mate 70 Pro Plus')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Huawei-nova-13-Pro_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Huawei')
      AND UPPER(p2.model_name) = UPPER('Nova 13 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Huawei-nova-13_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Huawei')
      AND UPPER(p2.model_name) = UPPER('Huawei Nova 13')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Huawei-Mate-XT-Ultimate.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Huawei')
      AND UPPER(p2.model_name) = UPPER('Mate XT Ultimate Trifold')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Huawei-Nova-Y72S.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Huawei')
      AND UPPER(p2.model_name) = UPPER('Nova Y72S')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Huawei-Enjoy-70X-Energy.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Huawei')
      AND UPPER(p2.model_name) = UPPER('Enjoy 70X Energy')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Huawei-Enjoy-80.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Huawei')
      AND UPPER(p2.model_name) = UPPER('Enjoy 80')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/huawei-nova-y73.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Huawei')
      AND UPPER(p2.model_name) = UPPER('Nova Y73')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Huawei-nova-13i.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Huawei')
      AND UPPER(p2.model_name) = UPPER('Huawei Nova 13i')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Huawei-Enjoy-70X_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Huawei')
      AND UPPER(p2.model_name) = UPPER('Enjoy 70X')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Huawei-Pura-80.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Huawei')
      AND UPPER(p2.model_name) = UPPER('Pura 80')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Huawei-Pura-80-Ultra.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Huawei')
      AND UPPER(p2.model_name) = UPPER('Pura 80 Ultra')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Huawei-Pura-80-Pro_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Huawei')
      AND UPPER(p2.model_name) = UPPER('Pura 80 Pro Plus')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Huawei-Pura-80-Pro.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Huawei')
      AND UPPER(p2.model_name) = UPPER('Pura 80 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Huawei-Pura-X.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Huawei')
      AND UPPER(p2.model_name) = UPPER('Pura X')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Huawei-Nova-Y63.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Huawei')
      AND UPPER(p2.model_name) = UPPER('Nova Y63')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Huawei-nova-14-Ultra.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Huawei')
      AND UPPER(p2.model_name) = UPPER('Nova 14 Ultra')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Huawei-Nova-14-Pro.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Huawei')
      AND UPPER(p2.model_name) = UPPER('Nova 14 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Huawei-nova-14.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Huawei')
      AND UPPER(p2.model_name) = UPPER('Huawei Nova 14')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Huawei-Mate-70-Air.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Huawei')
      AND UPPER(p2.model_name) = UPPER('Mate 70 Air')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Huawei-nova-14-Lite.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Huawei')
      AND UPPER(p2.model_name) = UPPER('Huawei Nova 14 Lite')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Huawei-nova-Flip-S.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Huawei')
      AND UPPER(p2.model_name) = UPPER('Nova Flip S')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Huawei-nova-14i.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Huawei')
      AND UPPER(p2.model_name) = UPPER('Huawei Nova 14i')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Huawei-Mate-XTs-Ultimate.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Huawei')
      AND UPPER(p2.model_name) = UPPER('Mate XTs Ultimate')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Infinix-GT-10-Pro-official.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Infinix')
      AND UPPER(p2.model_name) = UPPER('GT 10 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Infinix-Hot-40-Pro-official.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Infinix')
      AND UPPER(p2.model_name) = UPPER('Hot 40 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Infinix-Hot-40-Pro_2.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Infinix')
      AND UPPER(p2.model_name) = UPPER('Hot 40i')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Infinix-Smart-8-HD.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Infinix')
      AND UPPER(p2.model_name) = UPPER('Smart 8 HD')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Infinix-Hot-40-Pro-Free-Fire-Editions.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Infinix')
      AND UPPER(p2.model_name) = UPPER('Hot 40 Pro Free Fire Editions')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Infinix-Hot-30-5G.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Infinix')
      AND UPPER(p2.model_name) = UPPER('Hot 30 5G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/infinix-note-30i.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Infinix')
      AND UPPER(p2.model_name) = UPPER('Note 30i')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Infinix-Note-30-VIP.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Infinix')
      AND UPPER(p2.model_name) = UPPER('Note 30 VIP')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Infinix-Note-30-Pro_2.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Infinix')
      AND UPPER(p2.model_name) = UPPER('Note 30 Pro Limited Edition')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Infinix-Hot-30-Play.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Infinix')
      AND UPPER(p2.model_name) = UPPER('Hot 30 Play NFC')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/infinix-note-30-5g.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Infinix')
      AND UPPER(p2.model_name) = UPPER('Note 30 5G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Infinix-Smart-8.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Infinix')
      AND UPPER(p2.model_name) = UPPER('Smart 8')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Infinix-Zero-30-5G-official.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Infinix')
      AND UPPER(p2.model_name) = UPPER('Infinix Zero 30')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/infinix-note-30-vip-racing-edition-official.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Infinix')
      AND UPPER(p2.model_name) = UPPER('Note 30 VIP Racing Edition')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/infinix-gt-20-pro.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Infinix')
      AND UPPER(p2.model_name) = UPPER('GT 20 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Infinix-Note-40X-5G.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Infinix')
      AND UPPER(p2.model_name) = UPPER('Note 40X')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Infinix-Smart-9-HD.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Infinix')
      AND UPPER(p2.model_name) = UPPER('Smart 9 HD')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Infinix-Smart-8-Pro.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Infinix')
      AND UPPER(p2.model_name) = UPPER('Smart 8 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Infinix-smart-8-plus-Official.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Infinix')
      AND UPPER(p2.model_name) = UPPER('Smart 8 Plus')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Infinix-Smart-8-India.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Infinix')
      AND UPPER(p2.model_name) = UPPER('Smart 8 India')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/infinix-note-40-pro-5g.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Infinix')
      AND UPPER(p2.model_name) = UPPER('Infinix Note 40 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Infinix-Note-30-Pro_4.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Infinix')
      AND UPPER(p2.model_name) = UPPER('Infinix Note 40 Pro Plus')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/infinix-note-40-pro-4g.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Infinix')
      AND UPPER(p2.model_name) = UPPER('Note 40 Pro 4G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/infinix-note-40-4g.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Infinix')
      AND UPPER(p2.model_name) = UPPER('Note 40')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Infinix-Note-40-5G.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Infinix')
      AND UPPER(p2.model_name) = UPPER('Note 40 5G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Infinix-Hot-50-Pro-4G_2.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Infinix')
      AND UPPER(p2.model_name) = UPPER('Hot 50 Pro 4G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Infinix-Hot-50-Pro-4G_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Infinix')
      AND UPPER(p2.model_name) = UPPER('Hot 50 Pro Plus 4G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/infinix-hot-50-4g.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Infinix')
      AND UPPER(p2.model_name) = UPPER('Hot 50 4G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Infinix-Note-40S_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Infinix')
      AND UPPER(p2.model_name) = UPPER('Note 40S')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Infinix-Zero-Flip_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Infinix')
      AND UPPER(p2.model_name) = UPPER('Zero Flip')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Infinix-Hot-50i.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Infinix')
      AND UPPER(p2.model_name) = UPPER('Hot 50i')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Infinix-Smart-9.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Infinix')
      AND UPPER(p2.model_name) = UPPER('Smart 9')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Infinix-Hot-50-5G.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Infinix')
      AND UPPER(p2.model_name) = UPPER('Hot 50 5G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Infinix-Zero-40-4G.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Infinix')
      AND UPPER(p2.model_name) = UPPER('Zero 40 4G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Infinix-Zero-40.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Infinix')
      AND UPPER(p2.model_name) = UPPER('Infinix Zero 40 5G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/infinix-gt30-pro_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Infinix')
      AND UPPER(p2.model_name) = UPPER('GT 30 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Infinix-Note-50s_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Infinix')
      AND UPPER(p2.model_name) = UPPER('Note 50s')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Infinix-GT-30_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Infinix')
      AND UPPER(p2.model_name) = UPPER('GT 30')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Infinix-Hot-60i.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Infinix')
      AND UPPER(p2.model_name) = UPPER('Hot 60i')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/infinix-hot-60-pro-plus.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Infinix')
      AND UPPER(p2.model_name) = UPPER('Hot 60 Pro Plus 4G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/infinix-hot-60-pro.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Infinix')
      AND UPPER(p2.model_name) = UPPER('Hot 60 Pro 4G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/infinix-hot60-5g.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Infinix')
      AND UPPER(p2.model_name) = UPPER('Hot 60 5G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Infinix-Smart-10-HD_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Infinix')
      AND UPPER(p2.model_name) = UPPER('Smart 10 HD')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Infinix-Smart-10_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Infinix')
      AND UPPER(p2.model_name) = UPPER('Smart 10')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Infinix-Smart-10-Plus_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Infinix')
      AND UPPER(p2.model_name) = UPPER('Smart 10 Plus')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Infinix-Note-50x.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Infinix')
      AND UPPER(p2.model_name) = UPPER('Note 50x')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Infinix-Note-50-4G.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Infinix')
      AND UPPER(p2.model_name) = UPPER('Note 50 4G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Infinix-Note-50-Pro-4G-1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Infinix')
      AND UPPER(p2.model_name) = UPPER('Note 50 Pro 4G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Oppo-A1-5G.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Oppo')
      AND UPPER(p2.model_name) = UPPER('Oppo A1 5G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Oppo-A59-official.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Oppo')
      AND UPPER(p2.model_name) = UPPER('A59')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/oppo-reno8-t.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Oppo')
      AND UPPER(p2.model_name) = UPPER('Reno 8T 5G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Oppo-Reno-8T-official_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Oppo')
      AND UPPER(p2.model_name) = UPPER('Reno 8T')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Oppo-A78-5G.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Oppo')
      AND UPPER(p2.model_name) = UPPER('A78 5G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Oppo-Reno-10-Pro-Star-Sound-Edition.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Oppo')
      AND UPPER(p2.model_name) = UPPER('Reno10 Pro Star Sound Edition')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Oppo-A1-Vitality-Edition.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Oppo')
      AND UPPER(p2.model_name) = UPPER('Oppo A1 Vitality Edition')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Oppo-Find-X6-Pro.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Oppo')
      AND UPPER(p2.model_name) = UPPER('Find X6 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Oppo-Find-X6.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Oppo')
      AND UPPER(p2.model_name) = UPPER('Find X6')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Oppo-A1x.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Oppo')
      AND UPPER(p2.model_name) = UPPER('A1x 5G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/oppo-f23.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Oppo')
      AND UPPER(p2.model_name) = UPPER('F23')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Oppo-A98_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Oppo')
      AND UPPER(p2.model_name) = UPPER('A98')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/oppo-reno10-pro-plus.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Oppo')
      AND UPPER(p2.model_name) = UPPER('Reno10 Pro Plus')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/oppo-reno10-pro.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Oppo')
      AND UPPER(p2.model_name) = UPPER('Reno10 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/oppo-reno10.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Oppo')
      AND UPPER(p2.model_name) = UPPER('Reno10')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Oppo-a79-5G_2.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Oppo')
      AND UPPER(p2.model_name) = UPPER('A2')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/oppo-a2x.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Oppo')
      AND UPPER(p2.model_name) = UPPER('A2x')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Oppo-Find-N3-Official_2.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Oppo')
      AND UPPER(p2.model_name) = UPPER('Find N3')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Oppo-a79-5G.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Oppo')
      AND UPPER(p2.model_name) = UPPER('A79 5G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/oppo-a38-official.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Oppo')
      AND UPPER(p2.model_name) = UPPER('A38')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Oppo-A2-Pro-official.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Oppo')
      AND UPPER(p2.model_name) = UPPER('A2 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/oppo-find-n3-flip.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Oppo')
      AND UPPER(p2.model_name) = UPPER('Find N3 Flip')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/OPPO-A60-1024x683.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Oppo')
      AND UPPER(p2.model_name) = UPPER('A60 4G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Oppo-A80-5G.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Oppo')
      AND UPPER(p2.model_name) = UPPER('A80 5G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Oppo-A3x.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Oppo')
      AND UPPER(p2.model_name) = UPPER('A3x')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/OPPO-K12x-5G.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Oppo')
      AND UPPER(p2.model_name) = UPPER('K12x 5G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Oppo-A3-4G_13.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Oppo')
      AND UPPER(p2.model_name) = UPPER('A3 4G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Oppo-A3x-4G.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Oppo')
      AND UPPER(p2.model_name) = UPPER('A3x 4G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Oppo-Reno11-F-official.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Oppo')
      AND UPPER(p2.model_name) = UPPER('Reno 11F')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Oppo-Find-X7-Ultra.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Oppo')
      AND UPPER(p2.model_name) = UPPER('Find X7 Ultra')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Oppo-reno11-pro-china_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Oppo')
      AND UPPER(p2.model_name) = UPPER('Reno11 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Oppo-reno11-China_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Oppo')
      AND UPPER(p2.model_name) = UPPER('Reno11')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Oppo-Reno-12F.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Oppo')
      AND UPPER(p2.model_name) = UPPER('Reno 12F')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Oppo-A3.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Oppo')
      AND UPPER(p2.model_name) = UPPER('A3 5G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Oppo-Reno12-Pro_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Oppo')
      AND UPPER(p2.model_name) = UPPER('Reno12 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Oppo-A3-Pro_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Oppo')
      AND UPPER(p2.model_name) = UPPER('F27 Pro Plus')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Oppo-Reno12_2.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Oppo')
      AND UPPER(p2.model_name) = UPPER('Reno12')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Oppo-F25-Pro.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Oppo')
      AND UPPER(p2.model_name) = UPPER('F25 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Oppo-Reno13-China.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Oppo')
      AND UPPER(p2.model_name) = UPPER('Reno13')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Oppo-Reno13-Pro-China.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Oppo')
      AND UPPER(p2.model_name) = UPPER('Reno13 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/oppo-k12-plus.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Oppo')
      AND UPPER(p2.model_name) = UPPER('K12 Plus')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Oppo-Find-X8-Pro_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Oppo')
      AND UPPER(p2.model_name) = UPPER('Find X8 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Oppo-Find-X8_2.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Oppo')
      AND UPPER(p2.model_name) = UPPER('Find X8')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Oppo-K13_2.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Oppo')
      AND UPPER(p2.model_name) = UPPER('K12s')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Oppo-Find-X8s_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Oppo')
      AND UPPER(p2.model_name) = UPPER('Find X8s Plus')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Oppo-Find-X8s.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Oppo')
      AND UPPER(p2.model_name) = UPPER('Find X8s')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/oppo-k13x-5g.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Oppo')
      AND UPPER(p2.model_name) = UPPER('K13x')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Oppo-Find-X8-Ultra_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Oppo')
      AND UPPER(p2.model_name) = UPPER('Find X8 Ultra')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Oppo-K13-Turbo-Pro.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Oppo')
      AND UPPER(p2.model_name) = UPPER('K13 Turbo Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Oppo-K13-Turbo.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Oppo')
      AND UPPER(p2.model_name) = UPPER('K13 Turbo')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Oppo-F29-Pro.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Oppo')
      AND UPPER(p2.model_name) = UPPER('F29 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Oppo-F29.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Oppo')
      AND UPPER(p2.model_name) = UPPER('F29')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Oppo-A5-Pro_2.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Oppo')
      AND UPPER(p2.model_name) = UPPER('A5 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Oppo-A5-Pro-4G.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Oppo')
      AND UPPER(p2.model_name) = UPPER('A5 Pro 4G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Oppo-Reno14-Pro.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Oppo')
      AND UPPER(p2.model_name) = UPPER('Reno14 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Oppo-Reno14.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Oppo')
      AND UPPER(p2.model_name) = UPPER('Reno14')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Oppo-A5x.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Oppo')
      AND UPPER(p2.model_name) = UPPER('A5x')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Oppo-A5.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Oppo')
      AND UPPER(p2.model_name) = UPPER('A5')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Oppo-Reno15-Pro_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Oppo')
      AND UPPER(p2.model_name) = UPPER('Reno15 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Oppo-Reno15_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Oppo')
      AND UPPER(p2.model_name) = UPPER('Reno15')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Oppo-Find-X9-Pro_2.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Oppo')
      AND UPPER(p2.model_name) = UPPER('Find X9 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Oppo-A6-Max.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Oppo')
      AND UPPER(p2.model_name) = UPPER('A6 Max')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Oppo-A6i-5G.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Oppo')
      AND UPPER(p2.model_name) = UPPER('A6i 5G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Oppo-F31-Pro_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Oppo')
      AND UPPER(p2.model_name) = UPPER('F31 Pro Plus')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Oppo-F31-Pro_2.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Oppo')
      AND UPPER(p2.model_name) = UPPER('F31 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Oppo-A6-Pro-4G.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Oppo')
      AND UPPER(p2.model_name) = UPPER('A6 Pro 4G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Oppo-A6-Pro.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Oppo')
      AND UPPER(p2.model_name) = UPPER('A6 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Oppo-A6-GT.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Oppo')
      AND UPPER(p2.model_name) = UPPER('A6 GT')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Oppo-Find-N5_2.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Oppo')
      AND UPPER(p2.model_name) = UPPER('Find N5')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/xiaomi-poco-c51.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Poco')
      AND UPPER(p2.model_name) = UPPER('C51')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Poco-M6-5G.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Poco')
      AND UPPER(p2.model_name) = UPPER('Poco M6')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/xiaomi-poco-x5-pro-5g.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Poco')
      AND UPPER(p2.model_name) = UPPER('Poco X5 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/xiaomi-poco-x5-5g.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Poco')
      AND UPPER(p2.model_name) = UPPER('Poco X5')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Poco-C55.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Poco')
      AND UPPER(p2.model_name) = UPPER('C55')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/POCO-C50.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Poco')
      AND UPPER(p2.model_name) = UPPER('Poco C50')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Poco-F5-Pro.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Poco')
      AND UPPER(p2.model_name) = UPPER('F5 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Poco-F5_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Poco')
      AND UPPER(p2.model_name) = UPPER('Poco F5')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Poco-C65-official.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Poco')
      AND UPPER(p2.model_name) = UPPER('C65')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Poco-M6-Plus.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Poco')
      AND UPPER(p2.model_name) = UPPER('M6 Plus 5G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Poco-F6-Special-Limited-Edition.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Poco')
      AND UPPER(p2.model_name) = UPPER('F6 Deadpool Special Limited Edition')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Poco-C75-5G.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Poco')
      AND UPPER(p2.model_name) = UPPER('C75 5G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Poco-M7-pro-5G.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Poco')
      AND UPPER(p2.model_name) = UPPER('Poco M7 Pro 5G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Poco-M6-Pro-4G.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Poco')
      AND UPPER(p2.model_name) = UPPER('M6 Pro 4G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Poco-X6-Pro-5G-Official.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Poco')
      AND UPPER(p2.model_name) = UPPER('X6 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Poco-X6-5G.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Poco')
      AND UPPER(p2.model_name) = UPPER('Poco X6')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Poco-X6-Neo.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Poco')
      AND UPPER(p2.model_name) = UPPER('X6 Neo')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Poco-C61.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Poco')
      AND UPPER(p2.model_name) = UPPER('Poco C61')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Poco-F6-Pro.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Poco')
      AND UPPER(p2.model_name) = UPPER('F6 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Poco-F6.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Poco')
      AND UPPER(p2.model_name) = UPPER('Poco F6')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Xiaomi-Poco-C75.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Poco')
      AND UPPER(p2.model_name) = UPPER('C75')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Xiaomi-Poco-C71_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Poco')
      AND UPPER(p2.model_name) = UPPER('Poco C71')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/xiaomi-poco-m7-plus.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Poco')
      AND UPPER(p2.model_name) = UPPER('Poco M7 Plus')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/xiaomi-poco-m7-4g.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Poco')
      AND UPPER(p2.model_name) = UPPER('Poco M7 4G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Poco-X7-Iorn-Man-Edition.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Poco')
      AND UPPER(p2.model_name) = UPPER('X7 Pro Iron Man Edition')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Xiaomi-Poco-X7-Pro.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Poco')
      AND UPPER(p2.model_name) = UPPER('X7 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Xiaomi-Poco-X7_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Poco')
      AND UPPER(p2.model_name) = UPPER('Poco X7')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Xiaomi-Poco-F7-Pro.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Poco')
      AND UPPER(p2.model_name) = UPPER('Poco F7 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Xiaomi-Poco-F7-Ultra.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Poco')
      AND UPPER(p2.model_name) = UPPER('Poco F7 Ultra')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Realme-GT-Neo5-SE-official.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('Realme GT Neo5 SE')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Realme-Narzo-N55.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('Realme narzo N55')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/realme-c51.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('C51')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Realme-11x-5G.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('11x')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Realme-V50s_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('Realme V50s')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Realme-V50s.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('Realme V50')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Realme-GT-5-Pro-Official.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('GT5 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Realme-C67-5g.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('C67')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Realme-C67-4G.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('Realme C67')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/realme-v30.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('Realme V30')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Realme-GT-Neo5-240W.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('Realme GT Neo 5 240W')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Realme-GT-Neo5.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('Realme GT Neo 5')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Realme-10-Pro-Coca-cola-Edition-officia.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('Realme 10 Pro Coca-Cola Edition')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Realme-GT-3.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('Realme GT 3')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Realme-Narzo-60.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('Narzo 60')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Realme-Narzo-60-Pro.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('Narzo 60 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Realme-11-4G_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('11 5G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Realme-11-4G-official.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('11 4G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/realme-11.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('11')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Realme-C55-official.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('Realme C55')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/realme-c33-1_2.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('Realme C33 2023')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Realme-10-5G_3.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('Realme 10T 5G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Realme-C55-Rainforest-edition.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('C55 Rainforest edition')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/realme-11-pro-plus.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('11 Pro Plus')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/realme-11-pro.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('11 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Realme-C53-official.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('C53')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Realme-Narzo-60x-official.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('Narzo 60x')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Realme-GT5_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('Realme GT 5 240W')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Realme-GT5.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('Realme GT 5')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/realme-p1-5g.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('P1 5G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/pB97XA4h.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('P1 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Realme-GT-Neo6-SE_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('GT Neo 6 SE')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Realme-12X.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('12X')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/realme-12-lite.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('12 Lite')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/realme-narzo-70x_2.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('Narzo 70x')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/realme-narzo-70-5G.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('Narzo 70 5G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Realme-13.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('13')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Realme-13-Pro-Plus_3.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('13 Pro Plus')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Realme-13-Pro_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('13 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Realme-13-4G.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('13 4G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Realme-V60_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('Realme C63 5G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Realme-Note-60.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('Note 60')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Realme-Narzo-N61.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('Narzo N61')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Realme-Note-60x.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('Note 60x')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Realme-Neo7_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('Neo7')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Realme-Note-50.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('Note 50')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Note-1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('Note 1')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Realme-12-4G.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('Realme 12 4G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Realme-C61-Global.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('Realme C61')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Narzo-N63.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('Narzo N63')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Realme-GT-6_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('GT 6')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Realme-C63.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('Realme C63')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Realme-12-Plus.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('Realme 12 Plus')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Realme-12-pro-plus_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('12 Pro Supreme Edition')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/realme-Narzo-70-Pro.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('Narzo 70 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Realme-GT-6T.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('GT 6T')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Realme-Narzo-N65.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('Narzo N65')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Realme-GT-Neo-6.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('Realme GT Neo 6')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/realme-c75x.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('Realme C75x')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Realme-GT7-Pro_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('GT 7 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Realme-V60-pro.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('Realme V60 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Realme-Narzo-70-Turbo_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('Narzo 70 Turbo 5G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Realme-13-Plus.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('13 Plus')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Realme-P2-Pro_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('P2 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Realme-Narzo-80x_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('Narzo 80x')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Realme-Narzo-80-Pro_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('Narzo 80 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/realme-14t.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('14T')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Realme-P4-Pro.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('P4 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Realme-P4.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('P4')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Realme-P3x.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('P3x')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Realme-P3-Pro_2.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('P3 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Realme-GT7-Pro-Racing.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('GT7 Pro Racing Edition')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Realme-Neo7x.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('Neo7x')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Realme-Neo7-SE.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('Neo7 SE')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Realme-14-Pro_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('14 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Realme-14-Pro.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('14 Pro Plus')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Realme-14x_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('14X')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Realme-Narzo-80-Lite_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('Narzo 80 Lite 5G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/realme-note-70t.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('Note 70T')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Realme-15-Pro.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('15 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Realme-15.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('15')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Realme-Narzo-80-Lite.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('Narzo 80 Lite')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/realme-c71.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('Realme C71')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/realme-C73.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('Realme C73')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Realme-P3-Ultra.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('P3 Ultra')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Realme-P3.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('P3')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Realme-14-Pro-Lite.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('14 Pro Lite')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Realme-14.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('14')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Realme-C75_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('Realme C75 5G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Realme-GT-7T.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('Realme GT 7T')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/realme-gt-7.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('Realme GT 7')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/realme-neo7-turbo.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('Neo7 Turbo')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Realme-C85-Pro.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('Realme C85 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Realme-C85.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('Realme C85')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Realme-15-Lite_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Realme')
      AND UPPER(p2.model_name) = UPPER('15 Lite')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/xiaomi-redmi-note-12-pro_3.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Redmi')
      AND UPPER(p2.model_name) = UPPER('Note 12 Pro (Global)')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Redmi-Note-12-Pro-4G-official.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Redmi')
      AND UPPER(p2.model_name) = UPPER('Redmi Note 12 Pro 4G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Redmi-Note-12S.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Redmi')
      AND UPPER(p2.model_name) = UPPER('Note 12s')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Redmi-12-5G-off.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Redmi')
      AND UPPER(p2.model_name) = UPPER('12 5G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Redmi-13R.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Redmi')
      AND UPPER(p2.model_name) = UPPER('13R')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Redmi-13C-5G-official.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Redmi')
      AND UPPER(p2.model_name) = UPPER('Redmi 13C 5G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Redmi-12C.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Redmi')
      AND UPPER(p2.model_name) = UPPER('Redmi 12C')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Redmi-K60-Pro.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Redmi')
      AND UPPER(p2.model_name) = UPPER('Redmi K60 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Redmi-K60.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Redmi')
      AND UPPER(p2.model_name) = UPPER('Redmi K60')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Redmi-Note-12R.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Redmi')
      AND UPPER(p2.model_name) = UPPER('Note 12R Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/redmi-note-12t-pro-5g.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Redmi')
      AND UPPER(p2.model_name) = UPPER('Note 12T Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/redmi-12-official.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Redmi')
      AND UPPER(p2.model_name) = UPPER('Redmi 12')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/redmi-12R.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Redmi')
      AND UPPER(p2.model_name) = UPPER('Redmi 12R')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/redmi-12R_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Redmi')
      AND UPPER(p2.model_name) = UPPER('Redmi Note 12R')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/xiaomi-redmi-a2-plus.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Redmi')
      AND UPPER(p2.model_name) = UPPER('Redmi A2 Plus')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/redmi-A2_2.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Redmi')
      AND UPPER(p2.model_name) = UPPER('Redmi A2')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Redmi-Note-12-Turbo.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Redmi')
      AND UPPER(p2.model_name) = UPPER('Redmi Note 12 Turbo')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Redmi-Note-12-4G.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Redmi')
      AND UPPER(p2.model_name) = UPPER('Note 12 4G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Redmi-13C.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Redmi')
      AND UPPER(p2.model_name) = UPPER('Redmi 13C')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Redmi-Note-13R-Pro.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Redmi')
      AND UPPER(p2.model_name) = UPPER('Redmi Note 13R Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Redmi-K70-Pro-Lambo-Edition.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Redmi')
      AND UPPER(p2.model_name) = UPPER('Redmi K70 Pro Automobili Lamborghini Squadra Corse')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Redmi-K70e.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Redmi')
      AND UPPER(p2.model_name) = UPPER('Redmi K70E')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Redmi-K70-Pro.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Redmi')
      AND UPPER(p2.model_name) = UPPER('Redmi K70 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Redmi-Note-13-Pro-Plus.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Redmi')
      AND UPPER(p2.model_name) = UPPER('Redmi Note 13 Pro Plus')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Redmi-Note-13-Pro.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Redmi')
      AND UPPER(p2.model_name) = UPPER('Redmi Note 13 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Redmi-Note-13.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Redmi')
      AND UPPER(p2.model_name) = UPPER('Redmi Note 13')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/redmi-turbo-3.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Redmi')
      AND UPPER(p2.model_name) = UPPER('Turbo 3')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Xiaomi-Redmi-14C.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Redmi')
      AND UPPER(p2.model_name) = UPPER('14C')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Xiaomi-Redmi-Note-14_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Redmi')
      AND UPPER(p2.model_name) = UPPER('Redmi Note 14')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/xiaomi-redmi-a3-11.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Redmi')
      AND UPPER(p2.model_name) = UPPER('Redmi A3')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Redmi-Note-13-Pro-5G.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Redmi')
      AND UPPER(p2.model_name) = UPPER('Redmi Note 13 Pro 5G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/redmi-note-13-5g_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Redmi')
      AND UPPER(p2.model_name) = UPPER('Note 13 5G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Redmi-note-13-Pro-4G.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Redmi')
      AND UPPER(p2.model_name) = UPPER('Redmi Note 13 Pro 4G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Redmi-13-5G_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Redmi')
      AND UPPER(p2.model_name) = UPPER('13 5G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Redmi-K70-Ultra_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Redmi')
      AND UPPER(p2.model_name) = UPPER('K70 Ultra')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Redmi-13-4G_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Redmi')
      AND UPPER(p2.model_name) = UPPER('Redmi 13')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Xiaomi-Redmi-Note-13R.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Redmi')
      AND UPPER(p2.model_name) = UPPER('Redmi Note 13R')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Redmi-A3x.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Redmi')
      AND UPPER(p2.model_name) = UPPER('A3x')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Redmi-K80-Pro.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Redmi')
      AND UPPER(p2.model_name) = UPPER('Redmi K80 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Redmi-K80_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Redmi')
      AND UPPER(p2.model_name) = UPPER('Redmi K80')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Xiaomi-Redmi-A3-Pro.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Redmi')
      AND UPPER(p2.model_name) = UPPER('Redmi A3 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Redmi-14R.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Redmi')
      AND UPPER(p2.model_name) = UPPER('14R')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Xiaomi-Redmi-Turbo-4-Pro.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Redmi')
      AND UPPER(p2.model_name) = UPPER('Turbo 4 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Redmi-Note-15R-5G.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Redmi')
      AND UPPER(p2.model_name) = UPPER('Redmi Note 15R')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Xiaomi-Redmi-Note-15-Pro-5G_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Redmi')
      AND UPPER(p2.model_name) = UPPER('Redmi Note 15 Pro Plus')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Xiaomi-Redmi-Note-15-Pro-5G.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Redmi')
      AND UPPER(p2.model_name) = UPPER('Redmi Note 15 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Xiaomi-Redmi-Note-15-5G.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Redmi')
      AND UPPER(p2.model_name) = UPPER('Redmi Note 15')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Xiaomi-Redmi-Note-14-Pro-5G-Global.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Redmi')
      AND UPPER(p2.model_name) = UPPER('Note 14 Pro 5G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Xiaomi-Redmi-Note-14-Pro-4G-Global.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Redmi')
      AND UPPER(p2.model_name) = UPPER('Note 14 Pro 4G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Xiaomi-Redmi-Note-14-5G-Global.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Redmi')
      AND UPPER(p2.model_name) = UPPER('Note 14 5G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Xiaomi-Redmi-Note-14-4G-Global.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Redmi')
      AND UPPER(p2.model_name) = UPPER('Note 14 4G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Xiaomi-Redmi-Turbo-4.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Redmi')
      AND UPPER(p2.model_name) = UPPER('Turbo 4')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Xiaomi-Redmi-Note-14S.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Redmi')
      AND UPPER(p2.model_name) = UPPER('Redmi Note 14S')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Xiaomi-Redmi-13x.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Redmi')
      AND UPPER(p2.model_name) = UPPER('13x')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Xiaomi-Redmi-K90-Pro-Max.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Redmi')
      AND UPPER(p2.model_name) = UPPER('Redmi K90 Pro Max')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Xiaomi-Redmi-K90.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Redmi')
      AND UPPER(p2.model_name) = UPPER('Redmi K90')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Samsung-Galaxy-A24-4G.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Samsung')
      AND UPPER(p2.model_name) = UPPER('Galaxy A24 4G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Samsung-Galaxy-F14-5G.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Samsung')
      AND UPPER(p2.model_name) = UPPER('Galaxy F14 5G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Samsung-Galaxy-Z-Flip5.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Samsung')
      AND UPPER(p2.model_name) = UPPER('Galaxy Z Flip5')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Samsung-s-Galaxy-Z-Fold5.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Samsung')
      AND UPPER(p2.model_name) = UPPER('Galaxy Z Fold5')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Galaxy-F34.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Samsung')
      AND UPPER(p2.model_name) = UPPER('Galaxy F34 5G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/samsung-galaxy-a15.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Samsung')
      AND UPPER(p2.model_name) = UPPER('Galaxy A15 5G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/samsung-galaxy-a15-5g-official.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Samsung')
      AND UPPER(p2.model_name) = UPPER('Galaxy A15 5G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Samsung-Galaxy-A14-5G.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Samsung')
      AND UPPER(p2.model_name) = UPPER('Galaxy A14 5G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Samsung-Galaxy-M34-5G-official_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Samsung')
      AND UPPER(p2.model_name) = UPPER('Galaxy M34 5G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/samsung-galaxy-f54-5g-official.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Samsung')
      AND UPPER(p2.model_name) = UPPER('Galaxy F54')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Samsung-Galaxy-A14-4G.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Samsung')
      AND UPPER(p2.model_name) = UPPER('Galaxy A14')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Samsung-Galaxy-M54.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Samsung')
      AND UPPER(p2.model_name) = UPPER('Galaxy M54 5G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Samsung-Galaxy-M14-5G.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Samsung')
      AND UPPER(p2.model_name) = UPPER('Galaxy M14')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Samsung-Galaxy-A34-5G-Official.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Samsung')
      AND UPPER(p2.model_name) = UPPER('Galaxy A34 5G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Samsung-Galaxy-Jump3-5G.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Samsung')
      AND UPPER(p2.model_name) = UPPER('Galaxy Jump3')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/samsung-galaxy-s23-5g.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Samsung')
      AND UPPER(p2.model_name) = UPPER('Galaxy S23 FE')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Samsung-Galaxy-A05.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Samsung')
      AND UPPER(p2.model_name) = UPPER('Galaxy A05')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Samsung-Galaxy-A05s.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Samsung')
      AND UPPER(p2.model_name) = UPPER('Galaxy A05s')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Samsung-Galaxy-Z-Flip5-Retro.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Samsung')
      AND UPPER(p2.model_name) = UPPER('Galaxy Z Flip 5 Retro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Samsung-Galaxy-C55-orange.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Samsung')
      AND UPPER(p2.model_name) = UPPER('Galaxy C55')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Samsung-Galaxy-F13-official_2.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Samsung')
      AND UPPER(p2.model_name) = UPPER('Galaxy F14')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Samsung-Galaxy-A05_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Samsung')
      AND UPPER(p2.model_name) = UPPER('Galaxy A06')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Samsung-Galaxy-XCover7.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Samsung')
      AND UPPER(p2.model_name) = UPPER('Galaxy Xcover7')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Samsung-Galaxy-S24-Ultra.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Samsung')
      AND UPPER(p2.model_name) = UPPER('Galaxy S24 Ultra')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Samsung-Galaxy-S24-Plus.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Samsung')
      AND UPPER(p2.model_name) = UPPER('Galaxy S24 Plus')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Samsung-Galaxy-S24_3.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Samsung')
      AND UPPER(p2.model_name) = UPPER('Galaxy S24')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Samsung-Galaxy-Z-Fold-6_2.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Samsung')
      AND UPPER(p2.model_name) = UPPER('Galaxy Z Fold 6')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Samsung-Galaxy-Z-Flip6.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Samsung')
      AND UPPER(p2.model_name) = UPPER('Galaxy Z Flip 6')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Samsung-Galaxy-A55.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Samsung')
      AND UPPER(p2.model_name) = UPPER('Galaxy A55')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Samsung-Galaxy-M14-4G.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Samsung')
      AND UPPER(p2.model_name) = UPPER('Galaxy M14 4G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/galaxy-f15-5g-8GB-RAM.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Samsung')
      AND UPPER(p2.model_name) = UPPER('Galaxy F15 5G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Samsung-Galaxy-A35-Official.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Samsung')
      AND UPPER(p2.model_name) = UPPER('Galaxy A35')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/M35-5G.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Samsung')
      AND UPPER(p2.model_name) = UPPER('Galaxy M35 5G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Galaxy-C55.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Samsung')
      AND UPPER(p2.model_name) = UPPER('Galaxy F55')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Samsung-Galaxy-A16-5G_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Samsung')
      AND UPPER(p2.model_name) = UPPER('Galaxy A16 5G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Samsung-Galaxy-A16_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Samsung')
      AND UPPER(p2.model_name) = UPPER('Galaxy A16')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Samsung-Galaxy-Z-Fold-Special.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Samsung')
      AND UPPER(p2.model_name) = UPPER('Galaxy Z Fold Special')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Samsung-Galaxy-M05.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Samsung')
      AND UPPER(p2.model_name) = UPPER('Galaxy M05')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Samsung-Galaxy-F05.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Samsung')
      AND UPPER(p2.model_name) = UPPER('Galaxy F05')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Samsung-Galaxy-M55s_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Samsung')
      AND UPPER(p2.model_name) = UPPER('Galaxy M55s')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Samsung-Galaxy-M56.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Samsung')
      AND UPPER(p2.model_name) = UPPER('Galaxy M56')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Samsung-Galaxy-A07-4G_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Samsung')
      AND UPPER(p2.model_name) = UPPER('Galaxy A07 4G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Samsung-Galaxy-F06-5G.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Samsung')
      AND UPPER(p2.model_name) = UPPER('Galaxy F06 5G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Samsung-Galaxy-A06-5G_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Samsung')
      AND UPPER(p2.model_name) = UPPER('Galaxy A06 5G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/S25.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Samsung')
      AND UPPER(p2.model_name) = UPPER('Galaxy S25')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/S25-Plus.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Samsung')
      AND UPPER(p2.model_name) = UPPER('Galaxy S25 Plus')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Samsung-Galaxy-S25-Ultra_2.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Samsung')
      AND UPPER(p2.model_name) = UPPER('Galaxy S25 Ultra')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Samsung-Galaxy-Z-Flip7_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Samsung')
      AND UPPER(p2.model_name) = UPPER('Galaxy Z Flip 7')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Samsung-Galaxy-Z-Flip7-FE-pictures.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Samsung')
      AND UPPER(p2.model_name) = UPPER('Galaxy Z Flip 7 FE')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/samsung-galaxy-z-fold7.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Samsung')
      AND UPPER(p2.model_name) = UPPER('Galaxy Z Fold 7')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Samsung-Galaxy-F36_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Samsung')
      AND UPPER(p2.model_name) = UPPER('Galaxy F36 5G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Samsung-Galaxy-F16.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Samsung')
      AND UPPER(p2.model_name) = UPPER('Galaxy F16')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Samsung-Galaxy-A56_2.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Samsung')
      AND UPPER(p2.model_name) = UPPER('Galaxy A56')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Samsung-Galaxy-F56.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Samsung')
      AND UPPER(p2.model_name) = UPPER('Galaxy F56')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Samsung-Galaxy-S25-Edge_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Samsung')
      AND UPPER(p2.model_name) = UPPER('Galaxy S25 Slim')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Samsung-Galaxy-F07.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Samsung')
      AND UPPER(p2.model_name) = UPPER('Galaxy F07 5G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Samsung-Galaxy-M17.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Samsung')
      AND UPPER(p2.model_name) = UPPER('Galaxy M17')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Samsung-Galaxy-M07.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Samsung')
      AND UPPER(p2.model_name) = UPPER('Galaxy M07')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Samsung-Galaxy-F17.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Samsung')
      AND UPPER(p2.model_name) = UPPER('Galaxy F17')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Samsung-Galaxy-S25-FE_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Samsung')
      AND UPPER(p2.model_name) = UPPER('Galaxy S25 FE')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Samsung-Galaxy-A17-4G.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Samsung')
      AND UPPER(p2.model_name) = UPPER('Galaxy A17')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/vivo-y100i.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('Y100i 5G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Vvio-Y36i.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('Y36i')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Vivo-Y100i-Power.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('Y100i Power')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Vivo-V30-Lite.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('V30 Lite')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/vivo-y27s.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('Y27s')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Vivo-Y12-2023.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('Y12 4G, Y12 2023')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Vivo-Y17s-official.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('Y17s')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/vivo-t2-global.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('T2')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/vivo-v29e-5g.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('V29E 5G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Vivo-Y55t.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('Y55T')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Vivo-V40-SE.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('V40 SE')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/vivo-t3x-5g.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('T3x 5G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Vivo-X-Fold-3-Pro.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('X Fold3 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/vivo-iqoo-z9-turbo_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('iQOO Z9 Turbo')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Vivo-Y18e.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('Y18e')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/vivo-V30-Lite-4G.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('V30 Lite 4G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Vivo-S19-Pro-1_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('V40 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/vivo-iQOO-Z9s.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('iQOO Z9s')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/vivo-iQOO-Z9s-Pro.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('iQOO Z9s Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/vivo-S20-Pro_2.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('S20 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/vivo-neo9.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('iQOO Neo9 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/iQoo-Z8x_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('Y100T')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Vivo-Y200e-Official.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('Y200e')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Vivo-y28-5G.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('Y28 5G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Vivo-G2.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('G2')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/vivo-Y28s-5G.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('Y28s 5G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/vivo-V40-Lite.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('V40 Lite')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/vivo-Y28s-5G_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('Y37m')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/iQOO-Neo-9S-Pro-Plus.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('iQOO Neo 9s Pro Plus')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/vivo-iQOO-Z9-Lite.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('Z9 Lite')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Vivo-V40-SE-4G.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('V40 SE 4G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Vivo-Y18_5.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('Y18i')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/vVivo-V40_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('V40')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/vivo-T3-Lite-5g.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('T3 Lite 5G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/vivo-Y28-4G.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('Y28 4G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Vivo-Y38_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('Y58 5G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/vivo-V30-Pro.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('V30 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/vivo-v30.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('V30')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Y18.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('Y18')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Vivo-C30-SE.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('V30 SE')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Vivo-X100S-Pro.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('X100s Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/vivo-y200t.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('Y200t')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Vivo-Y200-GT.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('Y200 GT')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/IQOO-Neo-9s-Pro.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('iQOO Neo 9s Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Vivo-Y200-Pro.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('Y200 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Vivo-Y36t.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('Y36t')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Vivo-X100-Ultra.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('X100 Ultra')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/vivo-V30-Lite-4G_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('Y100 4G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Vivo-S19-Pro-1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('S19 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Vivo-S19-1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('S19')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/vivo-V30e.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('V30e')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/vivo-S20.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('S20')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/vivo-Y18t.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('Y18t')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/vivo-X200-Pro.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('X200 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/vivo-X200.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('X200')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Vivo-V40e_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('V40e')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Vivo-X200-Pro-Mini_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('X200 Pro Mini')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/vivo-Y300-Plus.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('Y300 Plus 5G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/vivo-Y19s.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('Y19s')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/vivo-V40-Lite-IDN_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('V40 Lite 5G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Vivo-T3-Ultra-5G_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('T3 Ultra 5G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Vivo-Y37-Pro.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('Y37 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/vivo-T3-Ultra_2.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('T3 Ultra')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Vivo-Y300-Pro-5G.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('Y300 Pro 5G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/vivo-T3-Pro.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('T3 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/vivo-iQOO-Z9-Turbo.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('iQOO Z9 Turbo Plus')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/vivo-V50e.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('V50e')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/vivo-iQOO-Z10x_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('iQOO Z10X')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/vivo-X200s_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('X200s')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/vivo-X200-Ultra.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('X200 Ultra')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/vivo-T4.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('T4')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/vivo-iQOO-Z10_2.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('iQOO Z10')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/vivo-iQOO-Z10-Turbo-Pro.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('iQOO Z10 Turbo Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/vivo-iQOO-Z10-Turbo.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('iQOO Z10 Turbo')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/vivo-T4R.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('T4R')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/vivo-V60_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('V60')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/vivo-iQOO-Z10-Turbo-plus.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('iQOO Z10 Turbo Plus')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/vivo-Y400-5g.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('Y400 5G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/vivo-T4-Pro.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('T4 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/vivo-Y29-4G.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('Y29 4G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/vivo-V50_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('V50')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/vivo-Y200-4G.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('Y200')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/vivo-Y200_2.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('Y200 Plus 5G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/vivo-Y19s-GT.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('Y19s GT')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/vivo-iQOO-Z10R.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('iQOO Z10R')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/vivo-t4-lite.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('T4 Lite')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/vivo-x-fold5.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('X Fold5')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/vivo-Y50-China.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('Y50')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/vivo-Y400-4G.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('Y400 4G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/vivo-iqoo-z10-lite.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('iQOO Z10 Lite')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/vivo-Y19s-Pro.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('Y19s Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/vivo-iqoo-neo-10.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('iQOO Neo10')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Vivo-T4-Ultra_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('T4 Ultra')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/vivo-y400-pro-5g.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('Y400 Pro 5G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/vivo-V50-Lite.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('V60 Lite')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/vivo-V50-Lite-4G.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('V50 Lite 4G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/vivo-T4x.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('T4x')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/vivo-Y29s.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('Y29s 5G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/vivo-iQOO-Neo-10R_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('iQOO Neo10R')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/vivo-Y39.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('Y39')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/vivo-s30_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('S30')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/vivo-s30-pro-mini.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('S30 Pro mini')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/vivo-Y19.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('Y19')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/vivo-Y300-GT.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('Y300 GT')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/vivo-Y500-Pro.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('Y500 Pro 5G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/vivo-Y19s_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('Y19s 5G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/vivo-iQOO-15.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('iQOO 15')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/vivo-V60e_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('V60e')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/vivo-X300-Pro.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('X300 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/vivo-X300.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('X300')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Vivo-Y50i.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('Y50i')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/vivo-V60-Lite-4G.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('V60 Lite 4G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/V60-Lite.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('V60 Lite')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/vivo-Y31-Pro.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('Y31 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/vivo-Y31.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Vivo')
      AND UPPER(p2.model_name) = UPPER('Y31')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Xaomi-Mix-Fold-3.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Xiaomi')
      AND UPPER(p2.model_name) = UPPER('Mix Fold 3')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Xiaomi-Civi-3-Disney-Strawberry-Bear-Edition.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Xiaomi')
      AND UPPER(p2.model_name) = UPPER('Civi 3 Disney Strawberry Bear Edition')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Civi-3-Disney-edition.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Xiaomi')
      AND UPPER(p2.model_name) = UPPER('Civi 3 Disney 100th Anniversary Edition')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Xiaomi-Civi-3.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Xiaomi')
      AND UPPER(p2.model_name) = UPPER('Xiaomi Civi 3')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Xiaomi-Mix-Fold-4.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Xiaomi')
      AND UPPER(p2.model_name) = UPPER('Mix Fold 4')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Xiaomi-Mix-Flip.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Xiaomi')
      AND UPPER(p2.model_name) = UPPER('Mix Flip')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Xiaomi-CIVI-4-Pro.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Xiaomi')
      AND UPPER(p2.model_name) = UPPER('Civi 4 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Xiaomi-Redmi-15.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Xiaomi')
      AND UPPER(p2.model_name) = UPPER('Redmi 15 5G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Xiaomi-Redmi-15-4G.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Xiaomi')
      AND UPPER(p2.model_name) = UPPER('Redmi 15 4G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Xiaomi-15-Ultra_2.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Xiaomi')
      AND UPPER(p2.model_name) = UPPER('15 Ultra')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/xiaomi-redmi-15c-4g-r.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Xiaomi')
      AND UPPER(p2.model_name) = UPPER('Redmi 15C 4G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/xiaomi-poco-f7.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Xiaomi')
      AND UPPER(p2.model_name) = UPPER('Poco F7')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/xiaomi-redmi-k80-ultra_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Xiaomi')
      AND UPPER(p2.model_name) = UPPER('Redmi K80 Ultra')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/xiaomi-mix-flip2.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Xiaomi')
      AND UPPER(p2.model_name) = UPPER('Mix Flip 2')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Xiaomi-17-Pro-Max.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Xiaomi')
      AND UPPER(p2.model_name) = UPPER('17 Pro Max')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Xiaomi-17-Pro.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Xiaomi')
      AND UPPER(p2.model_name) = UPPER('17 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Xiaomi-17.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Xiaomi')
      AND UPPER(p2.model_name) = UPPER('17')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Xiaomi-Redmi-15C_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Xiaomi')
      AND UPPER(p2.model_name) = UPPER('Redmi 15C 5G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Xiaomi-15T-Pro.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Xiaomi')
      AND UPPER(p2.model_name) = UPPER('15T Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Xiaomi-15T_2.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Xiaomi')
      AND UPPER(p2.model_name) = UPPER('15T')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/xiaomi-13-ultra.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Xiaomi')
      AND UPPER(p2.model_name) = UPPER('Xiaomi 13 Ultra')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Xiaomi-CIVI-2-Hello-Kitty-Limited-Edition.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Xiaomi')
      AND UPPER(p2.model_name) = UPPER('Xiaomi Civi 2 Hello Kitty Limited Edition')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Xiaomi-13-Lite.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Xiaomi')
      AND UPPER(p2.model_name) = UPPER('13 Lite')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Xiaomi-14-Pro.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Xiaomi')
      AND UPPER(p2.model_name) = UPPER('14 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Xiaomi-14.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Xiaomi')
      AND UPPER(p2.model_name) = UPPER('14')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Xiaomi-13T-Pro-official.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Xiaomi')
      AND UPPER(p2.model_name) = UPPER('13T Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Xiaomi-13T-official.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Xiaomi')
      AND UPPER(p2.model_name) = UPPER('13T')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Xiaomi-14-Ultra.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Xiaomi')
      AND UPPER(p2.model_name) = UPPER('14 Ultra')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Xiaomi-14-Ultra-Titanium-Special-Edition.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Xiaomi')
      AND UPPER(p2.model_name) = UPPER('14 Ultra Titanium Special Edition')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Xiaomi-15-Pro.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Xiaomi')
      AND UPPER(p2.model_name) = UPPER('15 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Xiaomi-15_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Xiaomi')
      AND UPPER(p2.model_name) = UPPER('15')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Xiaomi-14T_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Xiaomi')
      AND UPPER(p2.model_name) = UPPER('14T')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Xiaomi-14T-Pro_2.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Xiaomi')
      AND UPPER(p2.model_name) = UPPER('14T Pro 5G')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/xiaomi-15s-pro.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Xiaomi')
      AND UPPER(p2.model_name) = UPPER('15S Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

UPDATE phones p
SET p.main_image = 'https://www.mobile57.com/assets/images/product_images/webp/Xiaomi-CIVI-4-Pro_1.webp'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('Xiaomi')
      AND UPPER(p2.model_name) = UPPER('Civi 5 Pro')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);

COMMIT;

-- Total updates attempted: 692

-- Verify the results:
SELECT b.name, COUNT(p.id) as phones_without_images
FROM phones p
JOIN brands b ON p.brand_id = b.id
WHERE (p.main_image IS NULL OR p.main_image = 'N/A' OR p.main_image = '')
GROUP BY b.name
ORDER BY phones_without_images DESC;
