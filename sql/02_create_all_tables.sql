--------------------------------------------------------------------------------
-- DialSmart: Create All Database Tables
-- Purpose: Create complete database structure from scratch
-- Usage: Run this in SQL*Plus as: @sql/02_create_all_tables.sql
--------------------------------------------------------------------------------

SET ECHO ON
SET SERVEROUTPUT ON

PROMPT ================================================================================
PROMPT Creating DialSmart Database Tables
PROMPT ================================================================================
PROMPT

-- =============================================================================
-- 1. USERS Table (Parent table - referenced by many tables)
-- =============================================================================

PROMPT Creating USERS table...

CREATE TABLE users (
    id NUMBER(38) NOT NULL,
    full_name VARCHAR2(100 CHAR) NOT NULL,
    email VARCHAR2(120 CHAR) NOT NULL,
    password_hash VARCHAR2(255 CHAR) NOT NULL,
    user_category VARCHAR2(50 CHAR),
    age_range VARCHAR2(20 CHAR),
    is_admin NUMBER(38) DEFAULT 0,
    is_active NUMBER(38) DEFAULT 1,
    created_at DATE DEFAULT SYSDATE,
    last_active DATE DEFAULT SYSDATE,
    email_verified NUMBER(1) DEFAULT 0,
    email_verification_token VARCHAR2(255),
    email_verification_sent_at TIMESTAMP(6),
    password_reset_token VARCHAR2(100),
    password_reset_sent_at TIMESTAMP(6),
    force_password_change NUMBER(1) DEFAULT 0,
    created_by_admin_id NUMBER(10),
    last_password_change TIMESTAMP(6),
    CONSTRAINT users_pk PRIMARY KEY (id),
    CONSTRAINT users_email_unique UNIQUE (email),
    CONSTRAINT fk_users_created_by_admin FOREIGN KEY (created_by_admin_id) REFERENCES users(id)
);

CREATE SEQUENCE users_seq START WITH 1 INCREMENT BY 1;

PROMPT Users table created.
PROMPT

-- =============================================================================
-- 2. BRANDS Table (Parent table - referenced by phones)
-- =============================================================================

PROMPT Creating BRANDS table...

CREATE TABLE brands (
    id NUMBER(38) NOT NULL,
    name VARCHAR2(100 CHAR) NOT NULL,
    description CLOB,
    tagline VARCHAR2(200 CHAR),
    logo_url VARCHAR2(255 CHAR),
    is_active NUMBER(38) DEFAULT 1,
    is_featured NUMBER(38) DEFAULT 0,
    created_at DATE DEFAULT SYSDATE,
    updated_at DATE DEFAULT SYSDATE,
    CONSTRAINT brands_pk PRIMARY KEY (id),
    CONSTRAINT brands_name_unique UNIQUE (name)
);

CREATE SEQUENCE brands_seq START WITH 1 INCREMENT BY 1;

PROMPT Brands table created.
PROMPT

-- =============================================================================
-- 3. PHONES Table (Parent table - referenced by specifications, comparisons, etc.)
-- =============================================================================

PROMPT Creating PHONES table...

CREATE TABLE phones (
    id NUMBER(38) NOT NULL,
    brand_id NUMBER(38) NOT NULL,
    model_name VARCHAR2(150 CHAR) NOT NULL,
    model_number VARCHAR2(100 CHAR),
    price FLOAT(126) NOT NULL,
    main_image VARCHAR2(255 CHAR),
    gallery_images CLOB,
    is_active NUMBER(38) DEFAULT 1,
    availability_status VARCHAR2(50 CHAR) DEFAULT 'In Stock',
    release_date DATE,
    created_at DATE DEFAULT SYSDATE,
    updated_at DATE DEFAULT SYSDATE,
    CONSTRAINT phones_pk PRIMARY KEY (id),
    CONSTRAINT phones_brand_fk FOREIGN KEY (brand_id) REFERENCES brands(id)
);

CREATE SEQUENCE phones_seq START WITH 1 INCREMENT BY 1;

PROMPT Phones table created.
PROMPT

-- =============================================================================
-- 4. PHONE_SPECIFICATIONS Table (Child of phones)
-- =============================================================================

PROMPT Creating PHONE_SPECIFICATIONS table...

CREATE TABLE phone_specifications (
    id NUMBER(38) NOT NULL,
    phone_id NUMBER(38) NOT NULL,

    -- Display Specifications
    screen_size FLOAT(126),
    screen_resolution VARCHAR2(350),
    screen_type VARCHAR2(350),
    display_type VARCHAR2(350),
    refresh_rate NUMBER(38),
    ppi NUMBER(38),
    multitouch VARCHAR2(350),
    protection VARCHAR2(350),

    -- Processor Specifications
    processor VARCHAR2(350),
    chipset VARCHAR2(350),
    cpu VARCHAR2(350),
    gpu VARCHAR2(350),
    processor_brand VARCHAR2(350),

    -- Memory Specifications
    ram_options VARCHAR2(350),
    storage_options VARCHAR2(350),
    expandable_storage NUMBER(38) DEFAULT 0,
    card_slot VARCHAR2(350),

    -- Camera Specifications
    rear_camera VARCHAR2(500),
    rear_camera_main NUMBER(38),
    front_camera VARCHAR2(200),
    front_camera_mp NUMBER(38),
    camera_features CLOB,
    flash VARCHAR2(350),
    video_recording VARCHAR2(350),

    -- Battery Specifications
    battery_capacity NUMBER(38),
    battery VARCHAR2(350),
    charging_speed VARCHAR2(350),
    fast_charging VARCHAR2(350),
    wireless_charging VARCHAR2(350),
    removable_battery VARCHAR2(350),

    -- Network Specifications
    sim VARCHAR2(350),
    technology VARCHAR2(350),
    network_5g VARCHAR2(500),
    network_4g VARCHAR2(500),
    network_3g VARCHAR2(300),
    network_2g VARCHAR2(300),
    network_speed VARCHAR2(350),
    has_5g NUMBER(38) DEFAULT 0,

    -- Connectivity Specifications
    wifi_standard VARCHAR2(350),
    bluetooth_version VARCHAR2(350),
    gps VARCHAR2(350),
    nfc VARCHAR2(350),
    usb VARCHAR2(350),
    audio_jack VARCHAR2(350),
    radio VARCHAR2(350),

    -- Software & Build
    operating_system VARCHAR2(350),
    weight VARCHAR2(350),
    dimensions VARCHAR2(350),
    colors_available VARCHAR2(350),
    body_material VARCHAR2(300),

    -- Security & Features
    fingerprint_sensor NUMBER(38) DEFAULT 0,
    face_unlock NUMBER(38) DEFAULT 0,
    water_resistance VARCHAR2(350),
    dual_sim NUMBER(38) DEFAULT 0,
    sensors CLOB,

    -- Additional
    product_url VARCHAR2(500 CHAR),

    CONSTRAINT phone_specs_pk PRIMARY KEY (id),
    CONSTRAINT phone_specs_phone_fk FOREIGN KEY (phone_id) REFERENCES phones(id) ON DELETE CASCADE,
    CONSTRAINT phone_specs_phone_unique UNIQUE (phone_id)
);

CREATE SEQUENCE phone_specifications_seq START WITH 1 INCREMENT BY 1;

PROMPT Phone specifications table created.
PROMPT

-- =============================================================================
-- 5. COMPARISONS Table (Child of users and phones)
-- =============================================================================

PROMPT Creating COMPARISONS table...

CREATE TABLE comparisons (
    id NUMBER(38) NOT NULL,
    user_id NUMBER(38) NOT NULL,
    phone1_id NUMBER(38) NOT NULL,
    phone2_id NUMBER(38) NOT NULL,
    is_saved NUMBER(38) DEFAULT 0,
    comparison_notes CLOB,
    created_at DATE DEFAULT SYSDATE,
    CONSTRAINT comparisons_pk PRIMARY KEY (id),
    CONSTRAINT comparisons_user_fk FOREIGN KEY (user_id) REFERENCES users(id),
    CONSTRAINT comparisons_phone1_fk FOREIGN KEY (phone1_id) REFERENCES phones(id),
    CONSTRAINT comparisons_phone2_fk FOREIGN KEY (phone2_id) REFERENCES phones(id)
);

CREATE SEQUENCE comparisons_seq START WITH 1 INCREMENT BY 1;

PROMPT Comparisons table created.
PROMPT

-- =============================================================================
-- 6. RECOMMENDATIONS Table (Child of users and phones)
-- =============================================================================

PROMPT Creating RECOMMENDATIONS table...

CREATE TABLE recommendations (
    id NUMBER(38) NOT NULL,
    user_id NUMBER(38) NOT NULL,
    phone_id NUMBER(38) NOT NULL,
    match_percentage FLOAT(126),
    reasoning CLOB,
    user_criteria CLOB,
    is_viewed NUMBER(38) DEFAULT 0,
    is_saved NUMBER(38) DEFAULT 0,
    user_rating NUMBER(38),
    created_at DATE DEFAULT SYSDATE,
    CONSTRAINT recommendations_pk PRIMARY KEY (id),
    CONSTRAINT recommendations_user_fk FOREIGN KEY (user_id) REFERENCES users(id),
    CONSTRAINT recommendations_phone_fk FOREIGN KEY (phone_id) REFERENCES phones(id)
);

CREATE SEQUENCE recommendations_seq START WITH 1 INCREMENT BY 1;

PROMPT Recommendations table created.
PROMPT

-- =============================================================================
-- 7. USER_PREFERENCES Table (Child of users)
-- =============================================================================

PROMPT Creating USER_PREFERENCES table...

CREATE TABLE user_preferences (
    id NUMBER(38) NOT NULL,
    user_id NUMBER(38) NOT NULL,
    min_budget NUMBER(38),
    max_budget NUMBER(38),
    primary_usage CLOB,
    important_features CLOB,
    preferred_brands CLOB,
    min_ram NUMBER(38),
    min_storage NUMBER(38),
    min_camera NUMBER(38),
    min_battery NUMBER(38),
    requires_5g NUMBER(38) DEFAULT 0,
    min_screen_size FLOAT(126),
    max_screen_size FLOAT(126),
    updated_at DATE DEFAULT SYSDATE,
    CONSTRAINT user_prefs_pk PRIMARY KEY (id),
    CONSTRAINT user_prefs_user_fk FOREIGN KEY (user_id) REFERENCES users(id),
    CONSTRAINT user_prefs_user_unique UNIQUE (user_id)
);

CREATE SEQUENCE user_preferences_seq START WITH 1 INCREMENT BY 1;

PROMPT User preferences table created.
PROMPT

-- =============================================================================
-- 8. CHAT_HISTORY Table (Child of users - nullable for guest users)
-- =============================================================================

PROMPT Creating CHAT_HISTORY table...

CREATE TABLE chat_history (
    id NUMBER(38) NOT NULL,
    user_id NUMBER(38),  -- Nullable for guest users
    message CLOB NOT NULL,
    response CLOB NOT NULL,
    message_type VARCHAR2(20 CHAR) DEFAULT 'text',
    session_id VARCHAR2(100 CHAR),
    intent VARCHAR2(100 CHAR),
    chat_metadata CLOB,
    created_at DATE DEFAULT SYSDATE,
    CONSTRAINT chat_history_pk PRIMARY KEY (id),
    CONSTRAINT fk_chat_user FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE SEQUENCE chat_history_seq START WITH 1 INCREMENT BY 1;

PROMPT Chat history table created.
PROMPT

-- =============================================================================
-- 9. CONTACT_MESSAGES Table (Child of users - nullable)
-- =============================================================================

PROMPT Creating CONTACT_MESSAGES table...

CREATE TABLE contact_messages (
    id NUMBER(38) NOT NULL,
    user_id NUMBER(38),  -- Nullable for non-logged-in users
    name VARCHAR2(100 CHAR) NOT NULL,
    email VARCHAR2(150 CHAR) NOT NULL,
    subject VARCHAR2(200 CHAR),
    message CLOB NOT NULL,
    is_read NUMBER(38) DEFAULT 0,
    is_replied NUMBER(38) DEFAULT 0,
    admin_notes CLOB,
    created_at DATE DEFAULT SYSDATE,
    read_at DATE,
    replied_at DATE,
    CONSTRAINT contact_messages_pk PRIMARY KEY (id),
    CONSTRAINT contact_user_fk FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE SEQUENCE contact_messages_seq START WITH 1 INCREMENT BY 1;

PROMPT Contact messages table created.
PROMPT

-- =============================================================================
-- 10. AUDIT_LOGS Table (Child of users)
-- =============================================================================

PROMPT Creating AUDIT_LOGS table...

CREATE TABLE audit_logs (
    id NUMBER(38) NOT NULL,
    user_id NUMBER(38),
    target_user_id NUMBER(38),
    action_type VARCHAR2(100 CHAR) NOT NULL,
    description CLOB,
    ip_address VARCHAR2(50 CHAR),
    user_agent VARCHAR2(255 CHAR),
    created_at DATE DEFAULT SYSDATE,
    chat_metadata CLOB,
    CONSTRAINT audit_logs_pk PRIMARY KEY (id),
    CONSTRAINT audit_user_fk FOREIGN KEY (user_id) REFERENCES users(id),
    CONSTRAINT audit_target_user_fk FOREIGN KEY (target_user_id) REFERENCES users(id)
);

CREATE SEQUENCE audit_logs_seq START WITH 1 INCREMENT BY 1;

PROMPT Audit logs table created.
PROMPT

-- =============================================================================
-- 11. ADMINS Table (Independent - legacy table, may not be used)
-- =============================================================================

PROMPT Creating ADMINS table...

CREATE TABLE admins (
    id NUMBER(38) NOT NULL,
    admin_id VARCHAR2(20 CHAR) NOT NULL,
    username VARCHAR2(50 CHAR) NOT NULL,
    email VARCHAR2(100 CHAR) NOT NULL,
    password_hash VARCHAR2(255 CHAR) NOT NULL,
    role VARCHAR2(50 CHAR),
    created_at DATE DEFAULT SYSDATE,
    last_activity DATE DEFAULT SYSDATE,
    is_active NUMBER(38) DEFAULT 1,
    CONSTRAINT admins_pk PRIMARY KEY (id),
    CONSTRAINT admins_email_unique UNIQUE (email),
    CONSTRAINT admins_username_unique UNIQUE (username)
);

PROMPT Admins table created (legacy - may not be used).
PROMPT

-- =============================================================================
-- Create Indexes for Performance
-- =============================================================================

PROMPT Creating indexes for better performance...

-- Users indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_is_admin ON users(is_admin);

-- Phones indexes
CREATE INDEX idx_phones_brand ON phones(brand_id);
CREATE INDEX idx_phones_price ON phones(price);
CREATE INDEX idx_phones_active ON phones(is_active);

-- Phone specifications indexes
CREATE INDEX idx_specs_phone ON phone_specifications(phone_id);
CREATE INDEX idx_specs_ram ON phone_specifications(ram_options);
CREATE INDEX idx_specs_storage ON phone_specifications(storage_options);

-- Chat history indexes
CREATE INDEX idx_chat_user ON chat_history(user_id);
CREATE INDEX idx_chat_session ON chat_history(session_id);

-- Comparisons indexes
CREATE INDEX idx_comp_user ON comparisons(user_id);

-- Recommendations indexes
CREATE INDEX idx_rec_user ON recommendations(user_id);

PROMPT Indexes created.
PROMPT

PROMPT ================================================================================
PROMPT All tables created successfully!
PROMPT ================================================================================
PROMPT

-- Verify tables created
PROMPT Verifying tables:
SELECT table_name FROM user_tables ORDER BY table_name;

PROMPT
PROMPT Verifying sequences:
SELECT sequence_name FROM user_sequences ORDER BY sequence_name;

PROMPT
PROMPT Setup complete! Ready to import data.
PROMPT
