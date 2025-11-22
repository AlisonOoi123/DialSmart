-- Migration: Add website_url column to brands table
-- Date: 2025-11-22
-- Description: Add a website_url field to store brand official website URLs

-- For SQLite
ALTER TABLE brands ADD COLUMN website_url VARCHAR(500);

-- For PostgreSQL, MySQL, or other databases, the same statement should work
-- If using a different database and encountering issues, adjust the data type accordingly
