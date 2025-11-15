-- Check which phones have missing specifications
-- This will help identify which brands need data updates

SELECT
    b.name AS brand_name,
    COUNT(DISTINCT p.id) AS total_phones,
    COUNT(DISTINCT CASE WHEN ps.screen_size IS NULL THEN p.id END) AS missing_screen_size,
    COUNT(DISTINCT CASE WHEN ps.ram_options IS NULL THEN p.id END) AS missing_ram,
    COUNT(DISTINCT CASE WHEN ps.storage_options IS NULL THEN p.id END) AS missing_storage,
    COUNT(DISTINCT CASE WHEN ps.rear_camera IS NULL THEN p.id END) AS missing_rear_camera,
    COUNT(DISTINCT CASE WHEN ps.battery_capacity IS NULL THEN p.id END) AS missing_battery
FROM phones p
JOIN brands b ON p.brand_id = b.id
LEFT JOIN phone_specifications ps ON p.id = ps.phone_id
WHERE p.is_active = 1
GROUP BY b.name
ORDER BY missing_screen_size DESC;

-- Find specific phones with missing specs
SELECT
    p.id,
    p.model_name,
    b.name AS brand_name,
    CASE WHEN ps.id IS NULL THEN 'No specs record' ELSE 'Has specs record' END AS specs_status,
    ps.screen_size,
    ps.ram_options,
    ps.storage_options,
    ps.rear_camera,
    ps.battery_capacity
FROM phones p
JOIN brands b ON p.brand_id = b.id
LEFT JOIN phone_specifications ps ON p.id = ps.phone_id
WHERE p.is_active = 1
  AND b.name IN ('Apple', 'Honor', 'Google', 'Asus')
  AND (ps.screen_size IS NULL
       OR ps.ram_options IS NULL
       OR ps.storage_options IS NULL
       OR ps.rear_camera IS NULL
       OR ps.battery_capacity IS NULL)
ORDER BY b.name, p.model_name;
