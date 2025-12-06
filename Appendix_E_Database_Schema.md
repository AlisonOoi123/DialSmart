# Appendix E: Database Schema and ER Diagram

## E.1 Entity-Relationship Diagram

### E.1.1 Complete ER Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      DIALSMART DATABASE SCHEMA                          │
└─────────────────────────────────────────────────────────────────────────┘

┌──────────────────┐
│     BRANDS       │
├──────────────────┤
│ PK id            │
│    name          │◄──────────────┐
│    description   │               │
│    tagline       │               │ 1
│    logo_url      │               │
│    is_active     │               │
│    is_featured   │               │
│    created_at    │               │
│    updated_at    │               │
└──────────────────┘               │
                                   │
                                   │ M
┌──────────────────┐               │
│     PHONES       │───────────────┘
├──────────────────┤
│ PK id            │◄──────────────┬───────────────┬───────────────┬──────────────┐
│ FK brand_id      │               │ M             │ M             │ M            │ M
│    model_name    │               │               │               │              │
│    model_number  │               │               │               │              │
│    price         │               │               │               │              │
│    main_image    │               │               │               │              │
│    gallery_images│               │               │               │              │
│    is_active     │               │               │               │              │
│    availability  │               │               │               │              │
│    release_date  │               │               │               │              │
│    created_at    │               │               │               │              │
│    updated_at    │               │               │               │              │
└──────────────────┘               │               │               │              │
         │ 1                       │               │               │              │
         │                         │               │               │              │
         │ 1                       │               │               │              │
┌────────▼─────────┐               │               │               │              │
│ PHONE_SPECS      │               │               │               │              │
├──────────────────┤               │               │               │              │
│ PK id            │               │               │               │              │
│ FK phone_id      │               │               │               │              │
│    screen_size   │               │               │               │              │
│    screen_res    │               │               │               │              │
│    screen_type   │               │               │               │              │
│    refresh_rate  │               │               │               │              │
│    processor     │               │               │               │              │
│    ram_options   │               │               │               │              │
│    storage_opt   │               │               │               │              │
│    rear_camera   │               │               │               │              │
│    front_camera  │               │               │               │              │
│    battery_cap   │               │               │               │              │
│    charging_sp   │               │               │               │              │
│    has_5g        │               │               │               │              │
│    nfc           │               │               │               │              │
│    fingerprint   │               │               │               │              │
│    water_resist  │               │               │               │              │
│    weight        │               │               │               │              │
│    ...           │               │               │               │              │
└──────────────────┘               │               │               │              │
                                   │               │               │              │
┌──────────────────┐               │               │               │              │
│     USERS        │               │               │               │              │
├──────────────────┤               │               │               │              │
│ PK id            │               │               │               │              │
│    full_name     │◄──────────────┼───────────────┼───────────────┼──────────────┤
│    email         │               │ 1             │ 1             │ 1            │ 1
│    password_hash │               │               │               │              │
│    user_category │               │               │               │              │
│    age_range     │               │               │               │              │
│    is_admin      │               │               │               │              │
│    is_active     │               │               │               │              │
│    created_at    │               │               │               │              │
│    last_active   │               │               │               │              │
└──────────────────┘               │               │               │              │
         │ 1                       │               │               │              │
         │                         │               │               │              │
         │ M                       │               │               │              │
┌────────▼─────────┐               │               │               │              │
│ USER_PREFERENCES │               │               │               │              │
├──────────────────┤               │               │               │              │
│ PK id            │               │               │               │              │
│ FK user_id       │               │               │               │              │
│    min_budget    │               │               │               │              │
│    max_budget    │               │               │               │              │
│    primary_usage │               │               │               │              │
│    important_feat│               │               │               │              │
│    preferred_bra │               │               │               │              │
│    min_ram       │               │               │               │              │
│    min_storage   │               │               │               │              │
│    min_camera    │               │               │               │              │
│    requires_5g   │               │               │               │              │
│    updated_at    │               │               │               │              │
└──────────────────┘               │               │               │              │
                                   │               │               │              │
                    ┌──────────────▼──┐   ┌────────▼──────┐  ┌────▼──────┐  ┌──▼──────────┐
                    │ RECOMMENDATIONS │   │ COMPARISONS   │  │COMPARISONS│  │ CHAT_HISTORY│
                    ├─────────────────┤   ├───────────────┤  │(phone2)   │  ├─────────────┤
                    │ PK id           │   │ PK id         │  │           │  │ PK id       │
                    │ FK user_id      │   │ FK user_id    │  │           │  │ FK user_id  │
                    │ FK phone_id     │   │ FK phone1_id  │  │           │  │    message  │
                    │    match_pct    │   │ FK phone2_id  ├──┘           │  │    response │
                    │    reasoning    │   │    is_saved   │              │  │    msg_type │
                    │    user_criteria│   │    comp_notes │              │  │    session  │
                    │    is_viewed    │   │    created_at │              │  │    intent   │
                    │    is_saved     │   └───────────────┘              │  │    metadata │
                    │    user_rating  │                                  │  │    created  │
                    │    created_at   │                                  │  └─────────────┘
                    └─────────────────┘
```

### E.1.2 Relationship Summary

| Relationship | Type | Foreign Key | Description |
|--------------|------|-------------|-------------|
| Brand → Phone | One-to-Many | `phones.brand_id` | Each brand has multiple phones |
| Phone → PhoneSpecification | One-to-One | `phone_specifications.phone_id` | Each phone has one spec record |
| User → UserPreference | One-to-Many | `user_preferences.user_id` | Each user can have multiple preference records |
| User → Recommendation | One-to-Many | `recommendations.user_id` | Each user has multiple recommendations |
| Phone → Recommendation | One-to-Many | `recommendations.phone_id` | Each phone appears in multiple recommendations |
| User → Comparison | One-to-Many | `comparisons.user_id` | Each user has multiple comparisons |
| Phone → Comparison (phone1) | One-to-Many | `comparisons.phone1_id` | Each phone can be in multiple comparisons as phone1 |
| Phone → Comparison (phone2) | One-to-Many | `comparisons.phone2_id` | Each phone can be in multiple comparisons as phone2 |
| User → ChatHistory | One-to-Many | `chat_history.user_id` | Each user has multiple chat messages |

---

## E.2 Database Tables

### E.2.1 USERS Table

**Table Name:** `users`
**Purpose:** Store user account information and authentication data

| Column Name | Data Type | Constraints | Default | Description |
|-------------|-----------|-------------|---------|-------------|
| `id` | INTEGER | PRIMARY KEY | Auto-increment | Unique user identifier |
| `full_name` | VARCHAR(100) | NOT NULL | - | User's full name |
| `email` | VARCHAR(120) | NOT NULL, UNIQUE, INDEX | - | User email (login credential) |
| `password_hash` | VARCHAR(255) | NOT NULL | - | Hashed password (PBKDF2-SHA256) |
| `user_category` | VARCHAR(50) | NULL | NULL | User type (Student, Professional, etc.) |
| `age_range` | VARCHAR(20) | NULL | NULL | Age range (18-25, 26-35, etc.) |
| `is_admin` | BOOLEAN | NOT NULL | FALSE | Admin flag |
| `is_active` | BOOLEAN | NOT NULL | TRUE | Account active status |
| `created_at` | DATETIME | NOT NULL | CURRENT_TIMESTAMP | Account creation timestamp |
| `last_active` | DATETIME | NOT NULL | CURRENT_TIMESTAMP | Last activity timestamp |

**Indexes:**
- PRIMARY KEY: `id`
- UNIQUE INDEX: `email`
- INDEX: `email` (for login queries)

**Sample Data:**
```sql
INSERT INTO users (full_name, email, password_hash, user_category, is_admin) VALUES
('Test User', 'user@dialsmart.my', 'pbkdf2:sha256:...', 'Working Professional', 0),
('Admin User', 'admin@dialsmart.my', 'pbkdf2:sha256:...', 'Admin', 1);
```

---

### E.2.2 USER_PREFERENCES Table

**Table Name:** `user_preferences`
**Purpose:** Store user preferences for personalized recommendations

| Column Name | Data Type | Constraints | Default | Description |
|-------------|-----------|-------------|---------|-------------|
| `id` | INTEGER | PRIMARY KEY | Auto-increment | Unique preference ID |
| `user_id` | INTEGER | FOREIGN KEY, NOT NULL | - | References `users.id` |
| `min_budget` | INTEGER | NULL | 500 | Minimum budget in RM |
| `max_budget` | INTEGER | NULL | 5000 | Maximum budget in RM |
| `primary_usage` | TEXT | NULL | NULL | Primary phone usage (JSON string) |
| `important_features` | TEXT | NULL | NULL | Important features (JSON string) |
| `preferred_brands` | TEXT | NULL | NULL | Preferred brand IDs (JSON string) |
| `min_ram` | INTEGER | NULL | 4 | Minimum RAM in GB |
| `min_storage` | INTEGER | NULL | 64 | Minimum storage in GB |
| `min_camera` | INTEGER | NULL | 12 | Minimum camera MP |
| `min_battery` | INTEGER | NULL | 3000 | Minimum battery in mAh |
| `requires_5g` | BOOLEAN | NOT NULL | FALSE | Requires 5G support |
| `min_screen_size` | FLOAT | NULL | 5.5 | Minimum screen size in inches |
| `max_screen_size` | FLOAT | NULL | 7.0 | Maximum screen size in inches |
| `updated_at` | DATETIME | NOT NULL | CURRENT_TIMESTAMP | Last update timestamp |

**Foreign Keys:**
- `user_id` REFERENCES `users(id)` ON DELETE CASCADE

**Sample Data:**
```sql
INSERT INTO user_preferences (user_id, min_budget, max_budget, primary_usage, min_ram) VALUES
(1, 1000, 3000, '["Photography", "Social Media"]', 6);
```

---

### E.2.3 BRANDS Table

**Table Name:** `brands`
**Purpose:** Store smartphone brand information

| Column Name | Data Type | Constraints | Default | Description |
|-------------|-----------|-------------|---------|-------------|
| `id` | INTEGER | PRIMARY KEY | Auto-increment | Unique brand identifier |
| `name` | VARCHAR(100) | NOT NULL, UNIQUE, INDEX | - | Brand name (Samsung, Apple, etc.) |
| `description` | TEXT | NULL | NULL | Brand description |
| `tagline` | VARCHAR(200) | NULL | NULL | Brand tagline/slogan |
| `logo_url` | VARCHAR(255) | NULL | NULL | Brand logo image URL |
| `is_active` | BOOLEAN | NOT NULL | TRUE | Active status |
| `is_featured` | BOOLEAN | NOT NULL | FALSE | Featured on homepage |
| `created_at` | DATETIME | NOT NULL | CURRENT_TIMESTAMP | Creation timestamp |
| `updated_at` | DATETIME | NOT NULL | CURRENT_TIMESTAMP | Last update timestamp |

**Indexes:**
- PRIMARY KEY: `id`
- UNIQUE INDEX: `name`

**Sample Data:**
```sql
INSERT INTO brands (name, description, tagline, is_featured) VALUES
('Samsung', 'South Korean multinational conglomerate', 'Inspire the World, Create the Future', 1),
('Apple', 'American technology company', 'Think Different', 1),
('XIAOMI', 'Chinese electronics company', 'Just for fans', 1);
```

---

### E.2.4 PHONES Table

**Table Name:** `phones`
**Purpose:** Store main smartphone information

| Column Name | Data Type | Constraints | Default | Description |
|-------------|-----------|-------------|---------|-------------|
| `id` | INTEGER | PRIMARY KEY | Auto-increment | Unique phone identifier |
| `brand_id` | INTEGER | FOREIGN KEY, NOT NULL | - | References `brands.id` |
| `model_name` | VARCHAR(150) | NOT NULL, INDEX | - | Phone model name |
| `model_number` | VARCHAR(100) | NULL | NULL | Manufacturer model number |
| `price` | FLOAT | NOT NULL, INDEX | - | Price in Malaysian Ringgit (RM) |
| `main_image` | VARCHAR(255) | NULL | NULL | Main product image URL |
| `gallery_images` | TEXT | NULL | NULL | Additional images (JSON string) |
| `is_active` | BOOLEAN | NOT NULL, INDEX | TRUE | Active listing status |
| `availability_status` | VARCHAR(50) | NOT NULL | 'Available' | Available, Out of Stock, Pre-order |
| `release_date` | DATE | NULL | NULL | Phone release date |
| `created_at` | DATETIME | NOT NULL | CURRENT_TIMESTAMP | Record creation timestamp |
| `updated_at` | DATETIME | NOT NULL | CURRENT_TIMESTAMP | Last update timestamp |

**Foreign Keys:**
- `brand_id` REFERENCES `brands(id)` ON DELETE RESTRICT

**Indexes:**
- PRIMARY KEY: `id`
- INDEX: `model_name` (for search queries)
- INDEX: `price` (for price filtering)
- INDEX: `is_active` (for filtering active phones)

**Sample Data:**
```sql
INSERT INTO phones (brand_id, model_name, price, availability_status, release_date) VALUES
(1, 'Samsung Galaxy S23 Ultra', 5299.00, 'Available', '2023-02-01'),
(2, 'iPhone 15 Pro Max', 5999.00, 'Available', '2023-09-22'),
(3, 'Xiaomi 13 Pro', 3499.00, 'Available', '2023-02-26');
```

---

### E.2.5 PHONE_SPECIFICATIONS Table

**Table Name:** `phone_specifications`
**Purpose:** Store detailed phone specifications and features

| Column Name | Data Type | Constraints | Default | Description |
|-------------|-----------|-------------|---------|-------------|
| `id` | INTEGER | PRIMARY KEY | Auto-increment | Unique specification ID |
| `phone_id` | INTEGER | FOREIGN KEY, UNIQUE, NOT NULL | - | References `phones.id` |
| **Display Specifications** |
| `screen_size` | FLOAT | NULL | NULL | Screen size in inches |
| `screen_resolution` | VARCHAR(50) | NULL | NULL | Resolution (e.g., "1080x2400") |
| `screen_type` | VARCHAR(50) | NULL | NULL | Display type (AMOLED, LCD, etc.) |
| `refresh_rate` | INTEGER | NULL | 60 | Screen refresh rate in Hz |
| **Performance Specifications** |
| `processor` | VARCHAR(100) | NULL | NULL | Processor/chipset name |
| `processor_brand` | VARCHAR(50) | NULL | NULL | Processor brand (Qualcomm, etc.) |
| `ram_options` | VARCHAR(50) | NULL | NULL | Available RAM options (e.g., "6GB, 8GB") |
| `storage_options` | VARCHAR(50) | NULL | NULL | Storage options (e.g., "128GB, 256GB") |
| `expandable_storage` | BOOLEAN | NOT NULL | FALSE | Supports microSD card |
| **Camera Specifications** |
| `rear_camera` | VARCHAR(100) | NULL | NULL | Rear camera description |
| `rear_camera_main` | INTEGER | NULL | NULL | Main rear camera megapixels |
| `front_camera` | VARCHAR(50) | NULL | NULL | Front camera description |
| `front_camera_mp` | INTEGER | NULL | NULL | Front camera megapixels |
| `camera_features` | TEXT | NULL | NULL | Camera features (JSON string) |
| **Battery Specifications** |
| `battery_capacity` | INTEGER | NULL | NULL | Battery capacity in mAh |
| `charging_speed` | VARCHAR(50) | NULL | NULL | Charging speed (e.g., "33W Fast Charging") |
| `wireless_charging` | BOOLEAN | NOT NULL | FALSE | Supports wireless charging |
| **Connectivity** |
| `has_5g` | BOOLEAN | NOT NULL, INDEX | FALSE | 5G support |
| `wifi_standard` | VARCHAR(50) | NULL | NULL | WiFi standard (WiFi 6, etc.) |
| `bluetooth_version` | VARCHAR(20) | NULL | NULL | Bluetooth version |
| `nfc` | BOOLEAN | NOT NULL | FALSE | NFC support |
| **Additional Features** |
| `operating_system` | VARCHAR(50) | NULL | NULL | Operating system (Android 13, iOS 17) |
| `fingerprint_sensor` | BOOLEAN | NOT NULL | TRUE | Fingerprint sensor available |
| `face_unlock` | BOOLEAN | NOT NULL | FALSE | Face unlock available |
| `water_resistance` | VARCHAR(20) | NULL | NULL | Water resistance rating (IP68, etc.) |
| `dual_sim` | BOOLEAN | NOT NULL | TRUE | Dual SIM support |
| **Physical Characteristics** |
| `weight` | INTEGER | NULL | NULL | Weight in grams |
| `dimensions` | VARCHAR(50) | NULL | NULL | Dimensions (e.g., "160.5 x 74.8 x 8.4 mm") |
| `colors_available` | VARCHAR(200) | NULL | NULL | Available colors |

**Foreign Keys:**
- `phone_id` REFERENCES `phones(id)` ON DELETE CASCADE

**Indexes:**
- PRIMARY KEY: `id`
- UNIQUE INDEX: `phone_id` (one-to-one relationship)
- INDEX: `has_5g` (for 5G filtering)

**Sample Data:**
```sql
INSERT INTO phone_specifications (phone_id, screen_size, processor, ram_options, rear_camera_main, battery_capacity, has_5g) VALUES
(1, 6.8, 'Snapdragon 8 Gen 2', '8GB, 12GB', 200, 5000, 1);
```

---

### E.2.6 RECOMMENDATIONS Table

**Table Name:** `recommendations`
**Purpose:** Store AI recommendation history and results

| Column Name | Data Type | Constraints | Default | Description |
|-------------|-----------|-------------|---------|-------------|
| `id` | INTEGER | PRIMARY KEY | Auto-increment | Unique recommendation ID |
| `user_id` | INTEGER | FOREIGN KEY, NOT NULL | - | References `users.id` |
| `phone_id` | INTEGER | FOREIGN KEY, NOT NULL | - | References `phones.id` |
| `match_percentage` | FLOAT | NULL | NULL | Match score (0-100) |
| `reasoning` | TEXT | NULL | NULL | Explanation for recommendation |
| `user_criteria` | TEXT | NULL | NULL | User's input criteria (JSON string) |
| `is_viewed` | BOOLEAN | NOT NULL | FALSE | User viewed this recommendation |
| `is_saved` | BOOLEAN | NOT NULL | FALSE | User saved this recommendation |
| `user_rating` | INTEGER | NULL | NULL | User rating (1-5 stars) |
| `created_at` | DATETIME | NOT NULL, INDEX | CURRENT_TIMESTAMP | Recommendation timestamp |

**Foreign Keys:**
- `user_id` REFERENCES `users(id)` ON DELETE CASCADE
- `phone_id` REFERENCES `phones(id)` ON DELETE CASCADE

**Indexes:**
- PRIMARY KEY: `id`
- INDEX: `created_at` (for chronological queries)

**Sample Data:**
```sql
INSERT INTO recommendations (user_id, phone_id, match_percentage, reasoning, user_criteria) VALUES
(1, 1, 92.5, 'Excellent camera performance and battery life matching your requirements',
 '{"budget": {"max": 6000}, "features": ["Camera", "Battery"]}');
```

---

### E.2.7 COMPARISONS Table

**Table Name:** `comparisons`
**Purpose:** Store phone comparison history

| Column Name | Data Type | Constraints | Default | Description |
|-------------|-----------|-------------|---------|-------------|
| `id` | INTEGER | PRIMARY KEY | Auto-increment | Unique comparison ID |
| `user_id` | INTEGER | FOREIGN KEY, NOT NULL | - | References `users.id` |
| `phone1_id` | INTEGER | FOREIGN KEY, NOT NULL | - | First phone (references `phones.id`) |
| `phone2_id` | INTEGER | FOREIGN KEY, NOT NULL | - | Second phone (references `phones.id`) |
| `is_saved` | BOOLEAN | NOT NULL | FALSE | User saved this comparison |
| `comparison_notes` | TEXT | NULL | NULL | User notes on comparison |
| `created_at` | DATETIME | NOT NULL, INDEX | CURRENT_TIMESTAMP | Comparison timestamp |

**Foreign Keys:**
- `user_id` REFERENCES `users(id)` ON DELETE CASCADE
- `phone1_id` REFERENCES `phones(id)` ON DELETE CASCADE
- `phone2_id` REFERENCES `phones(id)` ON DELETE CASCADE

**Indexes:**
- PRIMARY KEY: `id`
- INDEX: `created_at` (for chronological queries)

**Sample Data:**
```sql
INSERT INTO comparisons (user_id, phone1_id, phone2_id, is_saved) VALUES
(1, 1, 2, 1);  -- Comparing Samsung Galaxy S23 Ultra vs iPhone 15 Pro Max
```

---

### E.2.8 CHAT_HISTORY Table

**Table Name:** `chat_history`
**Purpose:** Store chatbot conversation logs

| Column Name | Data Type | Constraints | Default | Description |
|-------------|-----------|-------------|---------|-------------|
| `id` | INTEGER | PRIMARY KEY | Auto-increment | Unique chat message ID |
| `user_id` | INTEGER | FOREIGN KEY, NOT NULL | - | References `users.id` |
| `message` | TEXT | NOT NULL | - | User's message |
| `response` | TEXT | NOT NULL | - | Chatbot's response |
| `message_type` | VARCHAR(20) | NOT NULL | 'text' | Message type (text, recommendation, comparison) |
| `session_id` | VARCHAR(100) | NULL | NULL | Session identifier (groups conversations) |
| `intent` | VARCHAR(100) | NULL | NULL | Detected user intent |
| `metadata` | TEXT | NULL | NULL | Additional context (JSON string) |
| `created_at` | DATETIME | NOT NULL, INDEX | CURRENT_TIMESTAMP | Message timestamp |

**Foreign Keys:**
- `user_id` REFERENCES `users(id)` ON DELETE CASCADE

**Indexes:**
- PRIMARY KEY: `id`
- INDEX: `created_at` (for chronological queries)

**Sample Data:**
```sql
INSERT INTO chat_history (user_id, message, response, intent, session_id) VALUES
(1, 'I need a phone under RM2000 with good camera',
    'I found several great options under RM2000 with excellent cameras...',
    'budget_query', 'session_12345');
```

---

## E.3 Database Constraints and Integrity

### E.3.1 Primary Keys

All tables have an auto-incrementing integer primary key named `id`.

### E.3.2 Foreign Key Constraints

| Table | Foreign Key | References | On Delete |
|-------|-------------|------------|-----------|
| `phones` | `brand_id` | `brands(id)` | RESTRICT |
| `phone_specifications` | `phone_id` | `phones(id)` | CASCADE |
| `user_preferences` | `user_id` | `users(id)` | CASCADE |
| `recommendations` | `user_id` | `users(id)` | CASCADE |
| `recommendations` | `phone_id` | `phones(id)` | CASCADE |
| `comparisons` | `user_id` | `users(id)` | CASCADE |
| `comparisons` | `phone1_id` | `phones(id)` | CASCADE |
| `comparisons` | `phone2_id` | `phones(id)` | CASCADE |
| `chat_history` | `user_id` | `users(id)` | CASCADE |

**Delete Behavior:**
- **CASCADE**: When parent record deleted, child records automatically deleted
- **RESTRICT**: Prevents deletion of parent if child records exist

### E.3.3 Unique Constraints

| Table | Column(s) | Purpose |
|-------|-----------|---------|
| `users` | `email` | One email per account |
| `brands` | `name` | One entry per brand |
| `phone_specifications` | `phone_id` | One spec record per phone |

### E.3.4 Check Constraints (Application Level)

Enforced by application logic:
- `users.email`: Valid email format
- `phones.price`: Must be positive
- `recommendations.match_percentage`: Between 0 and 100
- `recommendations.user_rating`: Between 1 and 5

---

## E.4 Data Types and Storage

### E.4.1 Column Data Types

| Data Type | Usage | Example |
|-----------|-------|---------|
| **INTEGER** | IDs, counts, megapixels | `id`, `battery_capacity` |
| **VARCHAR(n)** | Short text with max length | `email VARCHAR(120)` |
| **TEXT** | Long text, JSON strings | `description`, `user_criteria` |
| **FLOAT** | Decimal numbers | `price`, `screen_size`, `match_percentage` |
| **BOOLEAN** | True/False flags | `is_admin`, `has_5g`, `is_active` |
| **DATE** | Date only | `release_date` |
| **DATETIME** | Date and time | `created_at`, `updated_at` |

### E.4.2 JSON Data Storage

Several columns store JSON data as TEXT strings:

| Table | Column | JSON Structure |
|-------|--------|----------------|
| `user_preferences` | `primary_usage` | `["Photography", "Gaming"]` |
| `user_preferences` | `important_features` | `["Camera", "Battery", "Performance"]` |
| `user_preferences` | `preferred_brands` | `[1, 3, 5]` (brand IDs) |
| `phones` | `gallery_images` | `["/uploads/phone1_img1.jpg", "/uploads/phone1_img2.jpg"]` |
| `phone_specifications` | `camera_features` | `["OIS", "Night Mode", "AI Scene Detection"]` |
| `recommendations` | `user_criteria` | `{"budget": {"max": 3000}, "features": ["Camera"]}` |
| `chat_history` | `metadata` | `{"recommended_phones": [1, 3, 5]}` |

---

## E.5 Database Indexes

### E.5.1 Index Summary

| Table | Index Type | Column(s) | Purpose |
|-------|-----------|-----------|---------|
| `users` | PRIMARY KEY | `id` | Unique user lookup |
| `users` | UNIQUE INDEX | `email` | Login queries, prevent duplicates |
| `brands` | PRIMARY KEY | `id` | Unique brand lookup |
| `brands` | UNIQUE INDEX | `name` | Brand name queries |
| `phones` | PRIMARY KEY | `id` | Unique phone lookup |
| `phones` | INDEX | `model_name` | Search queries |
| `phones` | INDEX | `price` | Price range filtering |
| `phones` | INDEX | `is_active` | Filter active phones |
| `phone_specifications` | PRIMARY KEY | `id` | Unique spec lookup |
| `phone_specifications` | UNIQUE INDEX | `phone_id` | One-to-one enforcement |
| `phone_specifications` | INDEX | `has_5g` | 5G filtering |
| `recommendations` | PRIMARY KEY | `id` | Unique recommendation lookup |
| `recommendations` | INDEX | `created_at` | Chronological sorting |
| `comparisons` | PRIMARY KEY | `id` | Unique comparison lookup |
| `comparisons` | INDEX | `created_at` | Chronological sorting |
| `chat_history` | PRIMARY KEY | `id` | Unique message lookup |
| `chat_history` | INDEX | `created_at` | Chronological sorting |

### E.5.2 Query Performance

**Optimized Queries:**
```sql
-- Fast: Uses email index
SELECT * FROM users WHERE email = 'user@example.com';

-- Fast: Uses price index
SELECT * FROM phones WHERE price BETWEEN 1000 AND 3000;

-- Fast: Uses is_active index + price index
SELECT * FROM phones WHERE is_active = 1 AND price < 2000;

-- Fast: Uses joinedload to avoid N+1
SELECT phones.*, brands.name
FROM phones
JOIN brands ON phones.brand_id = brands.id
WHERE phones.is_active = 1;
```

---

## E.6 Database Size Estimates

### E.6.1 Storage Requirements

**Average Record Sizes:**

| Table | Avg Record Size | 100 Records | 1000 Records |
|-------|----------------|-------------|--------------|
| `users` | 500 bytes | 50 KB | 500 KB |
| `user_preferences` | 800 bytes | 80 KB | 800 KB |
| `brands` | 1 KB | 100 KB | 1 MB |
| `phones` | 1.5 KB | 150 KB | 1.5 MB |
| `phone_specifications` | 3 KB | 300 KB | 3 MB |
| `recommendations` | 2 KB | 200 KB | 2 MB |
| `comparisons` | 500 bytes | 50 KB | 500 KB |
| `chat_history` | 1.5 KB | 150 KB | 1.5 MB |

**Projected Database Size:**

| Scenario | Users | Phones | Total Size |
|----------|-------|--------|------------|
| **Development** | 10 | 50 | ~500 KB |
| **Small Production** | 1,000 | 500 | ~25 MB |
| **Medium Production** | 10,000 | 1,000 | ~100 MB |
| **Large Production** | 100,000 | 5,000 | ~500 MB |

---

## E.7 Database Initialization SQL

### E.7.1 Complete Schema Creation

```sql
-- Create Users table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    user_category VARCHAR(50),
    age_range VARCHAR(20),
    is_admin BOOLEAN NOT NULL DEFAULT 0,
    is_active BOOLEAN NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_active DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_users_email ON users(email);

-- Create Brands table
CREATE TABLE brands (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    tagline VARCHAR(200),
    logo_url VARCHAR(255),
    is_active BOOLEAN NOT NULL DEFAULT 1,
    is_featured BOOLEAN NOT NULL DEFAULT 0,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_brands_name ON brands(name);

-- Create Phones table
CREATE TABLE phones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    brand_id INTEGER NOT NULL,
    model_name VARCHAR(150) NOT NULL,
    model_number VARCHAR(100),
    price FLOAT NOT NULL,
    main_image VARCHAR(255),
    gallery_images TEXT,
    is_active BOOLEAN NOT NULL DEFAULT 1,
    availability_status VARCHAR(50) NOT NULL DEFAULT 'Available',
    release_date DATE,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (brand_id) REFERENCES brands(id)
);
CREATE INDEX idx_phones_model_name ON phones(model_name);
CREATE INDEX idx_phones_price ON phones(price);
CREATE INDEX idx_phones_is_active ON phones(is_active);

-- Create Phone Specifications table
CREATE TABLE phone_specifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    phone_id INTEGER NOT NULL UNIQUE,
    screen_size FLOAT,
    screen_resolution VARCHAR(50),
    screen_type VARCHAR(50),
    refresh_rate INTEGER DEFAULT 60,
    processor VARCHAR(100),
    processor_brand VARCHAR(50),
    ram_options VARCHAR(50),
    storage_options VARCHAR(50),
    expandable_storage BOOLEAN NOT NULL DEFAULT 0,
    rear_camera VARCHAR(100),
    rear_camera_main INTEGER,
    front_camera VARCHAR(50),
    front_camera_mp INTEGER,
    camera_features TEXT,
    battery_capacity INTEGER,
    charging_speed VARCHAR(50),
    wireless_charging BOOLEAN NOT NULL DEFAULT 0,
    has_5g BOOLEAN NOT NULL DEFAULT 0,
    wifi_standard VARCHAR(50),
    bluetooth_version VARCHAR(20),
    nfc BOOLEAN NOT NULL DEFAULT 0,
    operating_system VARCHAR(50),
    fingerprint_sensor BOOLEAN NOT NULL DEFAULT 1,
    face_unlock BOOLEAN NOT NULL DEFAULT 0,
    water_resistance VARCHAR(20),
    dual_sim BOOLEAN NOT NULL DEFAULT 1,
    weight INTEGER,
    dimensions VARCHAR(50),
    colors_available VARCHAR(200),
    FOREIGN KEY (phone_id) REFERENCES phones(id) ON DELETE CASCADE
);
CREATE INDEX idx_phone_specifications_has_5g ON phone_specifications(has_5g);

-- Create User Preferences table
CREATE TABLE user_preferences (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    min_budget INTEGER DEFAULT 500,
    max_budget INTEGER DEFAULT 5000,
    primary_usage TEXT,
    important_features TEXT,
    preferred_brands TEXT,
    min_ram INTEGER DEFAULT 4,
    min_storage INTEGER DEFAULT 64,
    min_camera INTEGER DEFAULT 12,
    min_battery INTEGER DEFAULT 3000,
    requires_5g BOOLEAN NOT NULL DEFAULT 0,
    min_screen_size FLOAT DEFAULT 5.5,
    max_screen_size FLOAT DEFAULT 7.0,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Create Recommendations table
CREATE TABLE recommendations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    phone_id INTEGER NOT NULL,
    match_percentage FLOAT,
    reasoning TEXT,
    user_criteria TEXT,
    is_viewed BOOLEAN NOT NULL DEFAULT 0,
    is_saved BOOLEAN NOT NULL DEFAULT 0,
    user_rating INTEGER,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (phone_id) REFERENCES phones(id) ON DELETE CASCADE
);
CREATE INDEX idx_recommendations_created_at ON recommendations(created_at);

-- Create Comparisons table
CREATE TABLE comparisons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    phone1_id INTEGER NOT NULL,
    phone2_id INTEGER NOT NULL,
    is_saved BOOLEAN NOT NULL DEFAULT 0,
    comparison_notes TEXT,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (phone1_id) REFERENCES phones(id) ON DELETE CASCADE,
    FOREIGN KEY (phone2_id) REFERENCES phones(id) ON DELETE CASCADE
);
CREATE INDEX idx_comparisons_created_at ON comparisons(created_at);

-- Create Chat History table
CREATE TABLE chat_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    message TEXT NOT NULL,
    response TEXT NOT NULL,
    message_type VARCHAR(20) NOT NULL DEFAULT 'text',
    session_id VARCHAR(100),
    intent VARCHAR(100),
    metadata TEXT,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
CREATE INDEX idx_chat_history_created_at ON chat_history(created_at);
```

---

**End of Appendix E**
