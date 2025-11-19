--------------------------------------------------------------------------------
-- DialSmart: Complete Database Setup Script
-- Date: 2025-11-19
-- Version: 2.0 (Includes ALL tables)
--
-- INSTRUCTIONS:
-- 1. Open SQL*Plus: sqlplus ds_user/dsuser123@localhost:1521/orclpdb
-- 2. Run: @complete_database_setup.sql
-- 3. Wait for completion
--------------------------------------------------------------------------------

SET ECHO ON
SET FEEDBACK ON
SET SERVEROUTPUT ON

PROMPT ================================================================================
PROMPT DialSmart Complete Database Setup
PROMPT ================================================================================
PROMPT WARNING: This will DELETE all existing data!
PROMPT Press Ctrl+C to cancel, or Enter to continue...
PAUSE

PROMPT
PROMPT ================================================================================
PROMPT Step 1: Dropping existing objects...
PROMPT ================================================================================

-- Drop tables in correct order
BEGIN
    FOR t IN (SELECT table_name FROM user_tables ORDER BY table_name) LOOP
        EXECUTE IMMEDIATE 'DROP TABLE ' || t.table_name || ' CASCADE CONSTRAINTS';
        DBMS_OUTPUT.PUT_LINE('✓ Dropped ' || t.table_name);
    END LOOP;
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('Error dropping tables: ' || SQLERRM);
END;
/

-- Drop sequences
BEGIN
    FOR s IN (SELECT sequence_name FROM user_sequences) LOOP
        EXECUTE IMMEDIATE 'DROP SEQUENCE ' || s.sequence_name;
    END LOOP;
    DBMS_OUTPUT.PUT_LINE('✓ Dropped all sequences');
EXCEPTION
    WHEN OTHERS THEN NULL;
END;
/

PROMPT
PROMPT ================================================================================
PROMPT Step 2: Creating sequences...
PROMPT ================================================================================

CREATE SEQUENCE users_seq START WITH 1 INCREMENT BY 1 NOCACHE;
CREATE SEQUENCE admins_seq START WITH 1 INCREMENT BY 1 NOCACHE;
CREATE SEQUENCE brands_seq START WITH 1 INCREMENT BY 1 NOCACHE;
CREATE SEQUENCE phones_seq START WITH 1 INCREMENT BY 1 NOCACHE;
CREATE SEQUENCE phone_specifications_seq START WITH 1 INCREMENT BY 1 NOCACHE;
CREATE SEQUENCE comparisons_seq START WITH 1 INCREMENT BY 1 NOCACHE;
CREATE SEQUENCE recommendations_seq START WITH 1 INCREMENT BY 1 NOCACHE;
CREATE SEQUENCE chat_history_seq START WITH 1 INCREMENT BY 1 NOCACHE;
CREATE SEQUENCE user_preferences_seq START WITH 1 INCREMENT BY 1 NOCACHE;
CREATE SEQUENCE contact_messages_seq START WITH 1 INCREMENT BY 1 NOCACHE;
CREATE SEQUENCE audit_logs_seq START WITH 1 INCREMENT BY 1 NOCACHE;

PROMPT ✓ Created all sequences

PROMPT
PROMPT ================================================================================
PROMPT Step 3: Creating tables...
PROMPT ================================================================================

-- 1. USERS Table
CREATE TABLE users (
    id NUMBER(38) PRIMARY KEY,
    full_name VARCHAR2(100 CHAR) NOT NULL,
    email VARCHAR2(120 CHAR) NOT NULL UNIQUE,
    password_hash VARCHAR2(255 CHAR) NOT NULL,
    user_category VARCHAR2(50 CHAR),
    age_range VARCHAR2(20 CHAR),
    is_admin NUMBER(38) DEFAULT 0,
    is_active NUMBER(38) DEFAULT 1,
    created_at DATE DEFAULT SYSDATE,
    last_active DATE,
    email_verified NUMBER(1) DEFAULT 0,
    email_verification_token VARCHAR2(255),
    email_verification_sent_at TIMESTAMP(6),
    password_reset_token VARCHAR2(100),
    password_reset_sent_at TIMESTAMP(6),
    force_password_change NUMBER(1) DEFAULT 0,
    created_by_admin_id NUMBER(10),
    last_password_change TIMESTAMP(6)
);

COMMENT ON TABLE users IS 'User accounts for regular users and administrators';
PROMPT ✓ Created users table

-- 2. ADMINS Table (Separate admin management)
CREATE TABLE admins (
    id NUMBER(38) PRIMARY KEY,
    user_id NUMBER(38) UNIQUE,
    admin_level VARCHAR2(50 CHAR) DEFAULT 'STANDARD',
    permissions CLOB,
    created_at DATE DEFAULT SYSDATE,
    last_login DATE,
    CONSTRAINT fk_admin_user FOREIGN KEY (user_id) 
        REFERENCES users(id) ON DELETE CASCADE
);

COMMENT ON TABLE admins IS 'Admin-specific settings and permissions';
PROMPT ✓ Created admins table

-- 3. BRANDS Table
CREATE TABLE brands (
    id NUMBER(38) PRIMARY KEY,
    name VARCHAR2(100 CHAR) NOT NULL UNIQUE,
    logo_url VARCHAR2(500 CHAR),
    description VARCHAR2(1000 CHAR),
    country VARCHAR2(50 CHAR),
    website VARCHAR2(255 CHAR),
    is_active NUMBER(38) DEFAULT 1,
    display_order NUMBER(38) DEFAULT 0,
    created_at DATE DEFAULT SYSDATE
);

COMMENT ON TABLE brands IS 'Smartphone brands';
PROMPT ✓ Created brands table

-- 4. PHONES Table
CREATE TABLE phones (
    id NUMBER(38) PRIMARY KEY,
    brand_id NUMBER(38) NOT NULL,
    model_name VARCHAR2(150 CHAR) NOT NULL,
    price NUMBER(10,2),
    main_image VARCHAR2(500 CHAR),
    gallery_images CLOB,
    release_date DATE,
    availability_status VARCHAR2(50 CHAR) DEFAULT 'Available',
    is_active NUMBER(38) DEFAULT 1,
    created_at DATE DEFAULT SYSDATE,
    updated_at DATE,
    CONSTRAINT fk_phone_brand FOREIGN KEY (brand_id) 
        REFERENCES brands(id) ON DELETE CASCADE
);

COMMENT ON TABLE phones IS 'Smartphone models';
CREATE INDEX idx_phone_brand ON phones(brand_id);
CREATE INDEX idx_phone_price ON phones(price);
PROMPT ✓ Created phones table

-- 5. PHONE_SPECIFICATIONS Table
CREATE TABLE phone_specifications (
    id NUMBER(38) PRIMARY KEY,
    phone_id NUMBER(38) NOT NULL,
    screen_size FLOAT(126),
    screen_resolution VARCHAR2(350 CHAR),
    screen_type VARCHAR2(350 CHAR),
    display_type VARCHAR2(350 CHAR),
    refresh_rate NUMBER(38),
    ppi NUMBER(38),
    multitouch VARCHAR2(350 CHAR),
    protection VARCHAR2(350 CHAR),
    processor VARCHAR2(350 CHAR),
    chipset VARCHAR2(350 CHAR),
    cpu VARCHAR2(350 CHAR),
    gpu VARCHAR2(350 CHAR),
    processor_brand VARCHAR2(350 CHAR),
    ram_options VARCHAR2(350 CHAR),
    storage_options VARCHAR2(350 CHAR),
    expandable_storage NUMBER(38),
    card_slot VARCHAR2(350 CHAR),
    rear_camera VARCHAR2(500 CHAR),
    rear_camera_main NUMBER(38),
    front_camera VARCHAR2(200 CHAR),
    front_camera_mp NUMBER(38),
    camera_features CLOB,
    flash VARCHAR2(350 CHAR),
    video_recording VARCHAR2(350 CHAR),
    battery_capacity NUMBER(38),
    battery VARCHAR2(350 CHAR),
    charging_speed VARCHAR2(350 CHAR),
    fast_charging VARCHAR2(350 CHAR),
    wireless_charging VARCHAR2(350 CHAR),
    removable_battery VARCHAR2(350 CHAR),
    sim VARCHAR2(350 CHAR),
    technology VARCHAR2(350 CHAR),
    network_5g VARCHAR2(500 CHAR),
    network_4g VARCHAR2(500 CHAR),
    network_3g VARCHAR2(300 CHAR),
    network_2g VARCHAR2(300 CHAR),
    network_speed VARCHAR2(350 CHAR),
    has_5g NUMBER(38),
    wifi_standard VARCHAR2(350 CHAR),
    bluetooth_version VARCHAR2(350 CHAR),
    gps VARCHAR2(350 CHAR),
    nfc VARCHAR2(350 CHAR),
    usb VARCHAR2(350 CHAR),
    audio_jack VARCHAR2(350 CHAR),
    radio VARCHAR2(350 CHAR),
    operating_system VARCHAR2(350 CHAR),
    weight VARCHAR2(350 CHAR),
    dimensions VARCHAR2(350 CHAR),
    colors_available VARCHAR2(350 CHAR),
    body_material VARCHAR2(300 CHAR),
    fingerprint_sensor NUMBER(38),
    face_unlock NUMBER(38),
    water_resistance VARCHAR2(350 CHAR),
    dual_sim NUMBER(38),
    sensors CLOB,
    product_url VARCHAR2(500 CHAR),
    CONSTRAINT fk_spec_phone FOREIGN KEY (phone_id) 
        REFERENCES phones(id) ON DELETE CASCADE
);

COMMENT ON TABLE phone_specifications IS 'Detailed phone specifications';
CREATE INDEX idx_spec_phone ON phone_specifications(phone_id);
PROMPT ✓ Created phone_specifications table

-- 6. USER_PREFERENCES Table
CREATE TABLE user_preferences (
    id NUMBER(38) PRIMARY KEY,
    user_id NUMBER(38) NOT NULL,
    preferred_brands VARCHAR2(500 CHAR),
    min_budget NUMBER(10,2),
    max_budget NUMBER(10,2),
    preferred_ram VARCHAR2(50 CHAR),
    preferred_storage VARCHAR2(50 CHAR),
    preferred_camera VARCHAR2(50 CHAR),
    preferred_battery VARCHAR2(50 CHAR),
    prefer_5g NUMBER(1) DEFAULT 0,
    usage_type VARCHAR2(100 CHAR),
    created_at DATE DEFAULT SYSDATE,
    updated_at DATE,
    CONSTRAINT fk_pref_user FOREIGN KEY (user_id) 
        REFERENCES users(id) ON DELETE CASCADE
);

COMMENT ON TABLE user_preferences IS 'User phone preferences for recommendations';
PROMPT ✓ Created user_preferences table

-- 7. COMPARISONS Table
CREATE TABLE comparisons (
    id NUMBER(38) PRIMARY KEY,
    user_id NUMBER(38),
    phone1_id NUMBER(38) NOT NULL,
    phone2_id NUMBER(38) NOT NULL,
    comparison_name VARCHAR2(200 CHAR),
    created_at DATE DEFAULT SYSDATE,
    CONSTRAINT fk_comparison_user FOREIGN KEY (user_id) 
        REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_comparison_phone1 FOREIGN KEY (phone1_id) 
        REFERENCES phones(id) ON DELETE CASCADE,
    CONSTRAINT fk_comparison_phone2 FOREIGN KEY (phone2_id) 
        REFERENCES phones(id) ON DELETE CASCADE
);

COMMENT ON TABLE comparisons IS 'User phone comparisons (NULL user_id for guests)';
PROMPT ✓ Created comparisons table

-- 8. RECOMMENDATIONS Table
CREATE TABLE recommendations (
    id NUMBER(38) PRIMARY KEY,
    user_id NUMBER(38),
    phone_id NUMBER(38) NOT NULL,
    recommendation_type VARCHAR2(50 CHAR),
    score FLOAT(126),
    reason CLOB,
    created_at DATE DEFAULT SYSDATE,
    user_feedback VARCHAR2(500 CHAR),
    CONSTRAINT fk_rec_user FOREIGN KEY (user_id) 
        REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_rec_phone FOREIGN KEY (phone_id) 
        REFERENCES phones(id) ON DELETE CASCADE
);

COMMENT ON TABLE recommendations IS 'AI recommendations (NULL user_id for guests)';
PROMPT ✓ Created recommendations table

-- 9. CHAT_HISTORY Table
CREATE TABLE chat_history (
    id NUMBER(38) PRIMARY KEY,
    user_id NUMBER(38),
    message CLOB NOT NULL,
    response CLOB NOT NULL,
    message_type VARCHAR2(20 CHAR),
    session_id VARCHAR2(100 CHAR),
    intent VARCHAR2(100 CHAR),
    chat_metadata CLOB,
    created_at DATE DEFAULT SYSDATE,
    CONSTRAINT fk_chat_user FOREIGN KEY (user_id) 
        REFERENCES users(id) ON DELETE CASCADE
);

COMMENT ON TABLE chat_history IS 'Chatbot conversations (NULL user_id for guests)';
CREATE INDEX idx_chat_user ON chat_history(user_id);
CREATE INDEX idx_chat_session ON chat_history(session_id);
PROMPT ✓ Created chat_history table

-- 10. CONTACT_MESSAGES Table
CREATE TABLE contact_messages (
    id NUMBER(38) PRIMARY KEY,
    user_id NUMBER(38),
    name VARCHAR2(100 CHAR) NOT NULL,
    email VARCHAR2(120 CHAR) NOT NULL,
    subject VARCHAR2(200 CHAR),
    message CLOB NOT NULL,
    status VARCHAR2(50 CHAR) DEFAULT 'NEW',
    admin_reply CLOB,
    replied_at DATE,
    replied_by NUMBER(38),
    created_at DATE DEFAULT SYSDATE,
    CONSTRAINT fk_contact_user FOREIGN KEY (user_id) 
        REFERENCES users(id) ON DELETE SET NULL,
    CONSTRAINT fk_contact_admin FOREIGN KEY (replied_by) 
        REFERENCES users(id) ON DELETE SET NULL
);

COMMENT ON TABLE contact_messages IS 'Contact form submissions and admin replies';
PROMPT ✓ Created contact_messages table

-- 11. AUDIT_LOGS Table
CREATE TABLE audit_logs (
    id NUMBER(38) PRIMARY KEY,
    user_id NUMBER(38),
    action VARCHAR2(100 CHAR) NOT NULL,
    table_name VARCHAR2(50 CHAR),
    record_id NUMBER(38),
    old_values CLOB,
    new_values CLOB,
    ip_address VARCHAR2(50 CHAR),
    user_agent VARCHAR2(500 CHAR),
    created_at DATE DEFAULT SYSDATE,
    CONSTRAINT fk_audit_user FOREIGN KEY (user_id) 
        REFERENCES users(id) ON DELETE SET NULL
);

COMMENT ON TABLE audit_logs IS 'System audit trail for admin actions';
CREATE INDEX idx_audit_user ON audit_logs(user_id);
CREATE INDEX idx_audit_action ON audit_logs(action);
CREATE INDEX idx_audit_created ON audit_logs(created_at);
PROMPT ✓ Created audit_logs table

PROMPT
PROMPT ================================================================================
PROMPT Step 4: Inserting initial data...
PROMPT ================================================================================

-- Insert Brands
INSERT INTO brands (id, name, country, is_active, display_order) 
VALUES (brands_seq.NEXTVAL, 'Apple', 'USA', 1, 1);
INSERT INTO brands (id, name, country, is_active, display_order) 
VALUES (brands_seq.NEXTVAL, 'Samsung', 'South Korea', 1, 2);
INSERT INTO brands (id, name, country, is_active, display_order) 
VALUES (brands_seq.NEXTVAL, 'XIAOMI', 'China', 1, 3);
INSERT INTO brands (id, name, country, is_active, display_order) 
VALUES (brands_seq.NEXTVAL, 'Huawei', 'China', 1, 4);
INSERT INTO brands (id, name, country, is_active, display_order) 
VALUES (brands_seq.NEXTVAL, 'Oppo', 'China', 1, 5);
INSERT INTO brands (id, name, country, is_active, display_order) 
VALUES (brands_seq.NEXTVAL, 'Vivo', 'China', 1, 6);
INSERT INTO brands (id, name, country, is_active, display_order) 
VALUES (brands_seq.NEXTVAL, 'Realme', 'China', 1, 7);
INSERT INTO brands (id, name, country, is_active, display_order) 
VALUES (brands_seq.NEXTVAL, 'Honor', 'China', 1, 8);
INSERT INTO brands (id, name, country, is_active, display_order) 
VALUES (brands_seq.NEXTVAL, 'Nokia', 'Finland', 1, 9);
INSERT INTO brands (id, name, country, is_active, display_order) 
VALUES (brands_seq.NEXTVAL, 'Lenovo', 'China', 1, 10);

PROMPT ✓ Inserted 10 brands

-- Insert Default Admin
-- Password: admin123
INSERT INTO users (
    id, full_name, email, password_hash, 
    user_category, is_admin, is_active, email_verified
) VALUES (
    users_seq.NEXTVAL,
    'Administrator',
    'admin@dialsmart.my',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5sDkiO9.LVppu',
    'Worker',
    1,
    1,
    1
);

PROMPT ✓ Created admin user
PROMPT   Email: admin@dialsmart.my
PROMPT   Password: admin123
PROMPT   ⚠️  CHANGE PASSWORD AFTER FIRST LOGIN!

COMMIT;

PROMPT
PROMPT ================================================================================
PROMPT ✅ SETUP COMPLETE!
PROMPT ================================================================================
PROMPT
PROMPT Database contains 11 tables:
PROMPT 1. users (1 admin user)
PROMPT 2. admins
PROMPT 3. brands (10 brands)
PROMPT 4. phones
PROMPT 5. phone_specifications
PROMPT 6. user_preferences
PROMPT 7. comparisons
PROMPT 8. recommendations
PROMPT 9. chat_history
PROMPT 10. contact_messages
PROMPT 11. audit_logs
PROMPT
PROMPT Next Steps:
PROMPT 1. Import phone data: python import_phones_from_csv.py
PROMPT 2. Start Flask: python run.py
PROMPT 3. Login: admin@dialsmart.my / admin123
PROMPT
PROMPT ================================================================================