# Appendix C: Operation Document

## C.1 Running the Application

### C.1.1 Starting the Application

#### Method 1: Using Python Directly

**Step 1: Open Terminal/Command Prompt**
- Windows: Press `Win + R`, type `cmd`, press Enter
- macOS: Press `Cmd + Space`, type `Terminal`, press Enter
- Linux: Press `Ctrl + Alt + T`

**Step 2: Navigate to Project Directory**
```bash
cd /path/to/DialSmart
```

**Step 3: Activate Virtual Environment**

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

**Expected Result:** Terminal prompt shows `(venv)` prefix

**Step 4: Run Application**
```bash
python run.py
```

**Expected Output:**
```
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
```

**Step 5: Access Application**
- Open web browser
- Navigate to: `http://localhost:5000`

#### Method 2: Using Flask CLI

**Step 1-3:** Same as Method 1

**Step 4: Set Flask Environment Variables**

**Windows:**
```bash
set FLASK_APP=run.py
set FLASK_ENV=development
flask run
```

**macOS/Linux:**
```bash
export FLASK_APP=run.py
export FLASK_ENV=development
flask run
```

**Step 5:** Access at `http://localhost:5000`

### C.1.2 Stopping the Application

**Method 1: Keyboard Interrupt**
- Press `Ctrl + C` in the terminal

**Expected Output:**
```
^C
 * Detected change, restarting
 * Shutting down...
```

**Method 2: Close Terminal**
- Close the terminal window (not recommended)

### C.1.3 Running on Different Port

**If port 5000 is already in use:**

**Windows:**
```bash
set FLASK_RUN_PORT=8000
python run.py
```

**macOS/Linux:**
```bash
export FLASK_RUN_PORT=8000
python run.py
```

Or directly:
```bash
flask run --port 8000
```

**Access at:** `http://localhost:8000`

### C.1.4 Running in Production Mode

**Using Gunicorn (Linux/macOS):**

**Step 1: Install Gunicorn**
```bash
pip install gunicorn
```

**Step 2: Run Application**
```bash
gunicorn -w 4 -b 0.0.0.0:8000 run:app
```

**Parameters:**
- `-w 4`: 4 worker processes
- `-b 0.0.0.0:8000`: Bind to all interfaces on port 8000

### C.1.5 Troubleshooting Startup Issues

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| `Port already in use` | Change port or kill process using port |
| `Database not found` | Run `flask init-db` |
| `Permission denied` | Run with appropriate permissions or use sudo (Linux) |
| `Virtual environment not activated` | Activate venv before running |

---

## C.2 User Operations

### C.2.1 User Registration

**Objective:** Create a new user account

**Prerequisites:** None

**Steps:**

1. **Navigate to Registration Page**
   - Open browser to `http://localhost:5000`
   - Click **"Register"** button in navigation bar
   - Or directly visit `http://localhost:5000/register`

2. **Fill Registration Form**
   - **Full Name:** Enter your full name (e.g., "John Doe")
   - **Email:** Enter valid email address (e.g., "john@example.com")
   - **Password:** Enter password (minimum 8 characters)
   - **Confirm Password:** Re-enter the same password

3. **Submit Form**
   - Click **"Create Account"** button

4. **Verify Success**
   - **Success Message:** "Account created successfully! Please log in."
   - **Redirect:** Automatically redirected to login page

**Validation Rules:**
- Name: Required, 2-100 characters
- Email: Valid email format, unique in system
- Password: Minimum 8 characters
- Confirm Password: Must match password

**Error Handling:**
- **Email already exists:** "Email already registered. Please use a different email or log in."
- **Passwords don't match:** "Passwords do not match."
- **Invalid email:** "Please enter a valid email address."

### C.2.2 User Login

**Objective:** Access user account

**Prerequisites:** Valid user account

**Steps:**

1. **Navigate to Login Page**
   - Click **"Login"** in navigation bar
   - Or visit `http://localhost:5000/login`

2. **Enter Credentials**
   - **Email:** Your registered email
   - **Password:** Your account password

3. **Optional: Remember Me**
   - Check **"Remember Me"** to stay logged in for 7 days

4. **Submit Login**
   - Click **"Login"** button

5. **Verify Success**
   - **Success Message:** "Welcome back, [Your Name]!"
   - **Redirect:** Dashboard page
   - **Navigation:** "Dashboard" and "Logout" options appear

**Error Handling:**
- **Invalid credentials:** "Invalid email or password."
- **Account suspended:** "Your account has been suspended. Please contact administrator."

**Test Credentials (Development):**
- Email: `user@dialsmart.my`
- Password: `password123`

### C.2.3 Getting AI Recommendations

**Objective:** Get personalized phone recommendations using AI

**Prerequisites:** User logged in

**Steps:**

1. **Navigate to Recommendation Wizard**
   - From Dashboard, click **"Get AI Recommendation"**
   - Or click **"Recommendations"** in navigation
   - URL: `http://localhost:5000/recommendation`

2. **Step 1: Budget Selection**
   - Select your budget range:
     - **Budget:** RM 0 - RM 1,000
     - **Mid-Range:** RM 1,000 - RM 2,000
     - **Upper Mid:** RM 2,000 - RM 3,000
     - **Premium:** RM 3,000+
   - Click **"Next"**

3. **Step 2: Primary Usage**
   - Select main usage purpose:
     - Gaming
     - Photography
     - Business/Productivity
     - Social Media
     - General Use
   - Select up to 3 options
   - Click **"Next"**

4. **Step 3: Feature Priorities**
   - Rank features by importance (1-5 scale):
     - Battery Life
     - Camera Quality
     - Performance (Speed)
     - Display Quality
     - Storage Capacity
     - 5G Connectivity
   - Click **"Next"**

5. **Step 4: Brand Preferences**
   - Select preferred brands (optional):
     - Samsung, Apple, Huawei, XIAOMI, Nokia, etc.
   - Select **"No Preference"** for all brands
   - Click **"Next"**

6. **Step 5: Technical Requirements**
   - **Minimum RAM:** Select from dropdown (4GB, 6GB, 8GB, 12GB)
   - **Minimum Storage:** Select (64GB, 128GB, 256GB, 512GB)
   - **5G Required:** Check if needed
   - **Camera Quality:** Minimum MP requirement
   - Click **"Get Recommendations"**

7. **View Results**
   - **Top 5 Recommendations** displayed
   - Each phone shows:
     - Match Score (percentage)
     - Price
     - Key specifications
     - Reason for recommendation
   - Click **"View Details"** to see full specs
   - Click **"Compare"** to compare with other phones

8. **Save Recommendation**
   - Recommendation automatically saved to history
   - Access from Dashboard → "Recommendation History"

**Expected Processing Time:** 2-3 seconds

### C.2.4 Using Chatbot

**Objective:** Get phone recommendations through conversational AI

**Prerequisites:** User logged in

**Steps:**

1. **Access Chatbot**
   - Click **"Chatbot"** in navigation
   - Or click chatbot icon in bottom right corner
   - URL: `http://localhost:5000/chatbot`

2. **Start Conversation**
   - Type message in input field
   - Click **"Send"** or press Enter

3. **Example Conversations**

   **Example 1: Budget Query**
   ```
   User: I need a phone under RM2000
   Bot: I found several great options under RM2000! Here are my top recommendations:
        1. XIAOMI Redmi Note 12 Pro - RM1,299
        2. Samsung Galaxy A54 - RM1,899
        Would you like more details about any of these phones?
   ```

   **Example 2: Feature-Specific**
   ```
   User: Show me phones with good camera for photography
   Bot: For photography, I recommend these phones with excellent cameras:
        1. iPhone 14 Pro - 48MP Triple Camera
        2. Samsung Galaxy S23 Ultra - 200MP Quad Camera
        What's your budget range?
   ```

   **Example 3: Comparison Request**
   ```
   User: Compare iPhone 14 vs Samsung S23
   Bot: Here's a quick comparison:
        [Comparison table displayed]
        Would you like a detailed side-by-side comparison?
   ```

4. **Follow Chatbot Prompts**
   - Answer clarifying questions
   - Provide budget, usage, preferences
   - Click on recommended phones for details

5. **View Chat History**
   - All conversations saved automatically
   - Access from Dashboard → "Chat History"

**Chatbot Capabilities:**
- Understand natural language queries
- Detect budget constraints (e.g., "under RM2000", "below 1500")
- Identify feature requirements (e.g., "good camera", "long battery")
- Provide recommendations with reasoning
- Compare phones on request
- Answer FAQ about phones

### C.2.5 Browsing Phones

**Objective:** Explore available phones with filters

**Prerequisites:** None (can be accessed without login)

**Steps:**

1. **Navigate to Browse Page**
   - Click **"Browse Phones"** in navigation
   - URL: `http://localhost:5000/phones/browse`

2. **View Phone Grid**
   - Phones displayed in grid layout (12 per page)
   - Each card shows:
     - Phone image
     - Model name
     - Brand
     - Price
     - Key specs (RAM, Storage, Camera)
     - "View Details" button

3. **Apply Filters**

   **Price Filter:**
   - Move price range slider
   - Min: RM 0, Max: RM 10,000
   - Phones update in real-time

   **Brand Filter:**
   - Check brand checkboxes
   - Multiple selection allowed
   - Click "Apply Filters"

   **Features Filter:**
   - **5G Support:** Check to show only 5G phones
   - **Wireless Charging:** Check to filter
   - **NFC:** Check to filter
   - **Fingerprint Sensor:** Check to filter

   **Specifications Filter:**
   - **RAM:** Select minimum (4GB, 6GB, 8GB, 12GB)
   - **Storage:** Select minimum (64GB, 128GB, 256GB)
   - **Battery:** Enter minimum mAh
   - **Camera:** Enter minimum MP

4. **Sort Results**
   - Sort by:
     - Price: Low to High
     - Price: High to Low
     - Newest First
     - Most Popular
     - Highest Rated

5. **Pagination**
   - Navigate between pages using pagination controls
   - Shows 12 phones per page

6. **View Phone Details**
   - Click **"View Details"** on any phone
   - See full specifications and features

### C.2.6 Comparing Phones

**Objective:** Side-by-side comparison of two phones

**Prerequisites:** User logged in (to save comparison)

**Steps:**

1. **Navigate to Comparison Page**
   - **Method 1:** Click **"Compare Phones"** in navigation
   - **Method 2:** From Browse page, select two phones and click "Compare"
   - **Method 3:** From phone details page, click "Add to Compare"
   - URL: `http://localhost:5000/phones/compare`

2. **Select First Phone**
   - Click **"Select Phone 1"** dropdown
   - Search or scroll to find phone
   - Click to select

3. **Select Second Phone**
   - Click **"Select Phone 2"** dropdown
   - Choose second phone

4. **View Comparison Table**
   - Detailed comparison shows:
     - **Basic Info:** Brand, model, price
     - **Display:** Screen size, resolution, type, refresh rate
     - **Performance:** Processor, RAM, storage options
     - **Camera:** Rear camera, front camera, video specs
     - **Battery:** Capacity, charging speed, wireless charging
     - **Connectivity:** 5G, Wi-Fi, Bluetooth, NFC
     - **Features:** OS, fingerprint, water resistance
     - **Physical:** Weight, dimensions

5. **Interpret Results**
   - **Winner indicators:** Green highlight shows better value
   - **Price comparison:** Lower price highlighted
   - **Feature comparison:** Better specs highlighted
   - **Overall winner:** Displayed at top with score

6. **Save Comparison**
   - Click **"Save Comparison"** button
   - Comparison saved to history
   - Access from Dashboard → "Saved Comparisons"

7. **Share or Print**
   - Click **"Print Comparison"** to print
   - Or use browser print function (Ctrl+P)

### C.2.7 Managing User Profile

**Objective:** Update user account information

**Prerequisites:** User logged in

**Steps:**

1. **Access Profile Page**
   - Click username in top-right corner
   - Select **"Profile"** from dropdown
   - URL: `http://localhost:5000/profile`

2. **Edit Profile Information**
   - **Full Name:** Update name
   - **Email:** Update email (requires verification)
   - **Phone Number:** Add/update phone
   - **Location:** Add city/state in Malaysia

3. **Change Password**
   - Click **"Change Password"** section
   - **Current Password:** Enter current password
   - **New Password:** Enter new password (min 8 characters)
   - **Confirm New Password:** Re-enter new password
   - Click **"Update Password"**

4. **Upload Profile Picture**
   - Click **"Choose File"**
   - Select image (PNG, JPG, GIF, max 5MB)
   - Click **"Upload"**
   - Image displays as profile avatar

5. **Save Changes**
   - Click **"Save Profile"** button
   - **Success Message:** "Profile updated successfully!"

### C.2.8 Managing User Preferences

**Objective:** Set default preferences for recommendations

**Prerequisites:** User logged in

**Steps:**

1. **Access Preferences Page**
   - From Dashboard, click **"Preferences"**
   - Or navigate to `http://localhost:5000/preferences`

2. **Set Default Budget**
   - Select default budget range
   - Used for quick recommendations

3. **Set Primary Usage**
   - Select main phone usage
   - Gaming, Photography, Business, etc.

4. **Feature Priorities**
   - Rank importance of:
     - Battery Life
     - Camera
     - Performance
     - Display
     - Storage
   - Use slider or number input (1-5)

5. **Brand Preferences**
   - Select favorite brands
   - System will prioritize these in recommendations

6. **Notification Settings**
   - **Email notifications:** Check to enable
   - **New phone alerts:** Get notified of new models
   - **Price drop alerts:** Notified when saved phones drop in price

7. **Save Preferences**
   - Click **"Save Preferences"**
   - **Success Message:** "Preferences saved successfully!"
   - Used automatically in future recommendations

### C.2.9 Using Contact Form

**Objective:** Send inquiry or feedback to administrators

**Prerequisites:** None (available to all users)

**Steps:**

1. **Navigate to Contact Page**
   - Click **"Contact Us"** in footer
   - URL: `http://localhost:5000/contact`

2. **Fill Contact Form**
   - **Your Name:** Enter full name
   - **Email:** Your email address
   - **Subject:** Brief subject line
   - **Category:** Select type
     - General Inquiry
     - Technical Support
     - Feedback
     - Report Issue
     - Feature Request
   - **Message:** Detailed message (max 1000 characters)

3. **Optional: Attach Screenshot**
   - Click **"Attach File"** (optional)
   - Upload screenshot of issue (if applicable)

4. **Submit Form**
   - Click **"Send Message"**
   - **Success Message:** "Your message has been sent. We'll respond within 24 hours."

5. **Receive Admin Reply**
   - Admin reviews message in admin panel
   - Admin sends reply via email
   - Reply received at provided email address

### C.2.10 Viewing Recommendation History

**Objective:** Review past AI recommendations

**Prerequisites:** User logged in

**Steps:**

1. **Access History**
   - From Dashboard, click **"Recommendation History"**
   - URL: `http://localhost:5000/history`

2. **View Past Recommendations**
   - Table displays:
     - Date and time
     - Criteria used (budget, usage, features)
     - Top recommended phones
     - Match scores

3. **Filter History**
   - Filter by date range
   - Filter by budget range
   - Filter by phone brand

4. **Repeat Recommendation**
   - Click **"Use These Criteria Again"**
   - Wizard pre-filled with previous criteria
   - Make adjustments if needed
   - Generate new recommendations

5. **Export History**
   - Click **"Export to PDF"**
   - Download history as PDF report

---

## C.3 Admin Operations

### C.3.1 Admin Login

**Objective:** Access admin panel

**Prerequisites:** Admin or Super Admin account

**Steps:**

1. **Navigate to Login Page**
   - Visit `http://localhost:5000/login`

2. **Enter Admin Credentials**
   - **Email:** Admin email (e.g., `admin@dialsmart.my`)
   - **Password:** Admin password

3. **Login**
   - Click **"Login"** button

4. **Access Admin Panel**
   - After login, click **"Admin Panel"** in navigation
   - Or visit `http://localhost:5000/admin`

**Admin Test Credentials:**
- Email: `admin@dialsmart.my`
- Password: `admin123`

**Super Admin Test Credentials:**
- Email: `superadmin@dialsmart.my`
- Password: `superadmin123`

### C.3.2 Managing Phones

**Objective:** Add, edit, or delete phone listings

**Prerequisites:** Admin logged in

#### C.3.2.1 Adding New Phone

**Steps:**

1. **Navigate to Phone Management**
   - Admin Panel → **"Manage Phones"**
   - Click **"Add New Phone"** button

2. **Fill Basic Information**
   - **Brand:** Select from dropdown
   - **Model Name:** Enter full model name
   - **Price (RM):** Enter price in Malaysian Ringgit
   - **Description:** Brief description (optional)

3. **Upload Phone Image**
   - Click **"Choose File"**
   - Select product image (PNG/JPG, max 5MB)
   - **Recommended:** 800x800px, white background

4. **Enter Specifications**

   **Display:**
   - Screen Size (inches)
   - Resolution (e.g., 1080x2400)
   - Display Type (AMOLED, LCD, etc.)
   - Refresh Rate (Hz)

   **Performance:**
   - Processor/Chipset
   - RAM Options (e.g., "6GB, 8GB")
   - Storage Options (e.g., "128GB, 256GB")

   **Camera:**
   - Rear Camera (e.g., "50MP + 12MP + 5MP")
   - Main Camera MP (numeric)
   - Front Camera (e.g., "32MP")
   - Front Camera MP (numeric)
   - Video Recording (e.g., "4K@30fps")

   **Battery:**
   - Battery Capacity (mAh)
   - Charging Speed (W)
   - Wireless Charging (Yes/No checkbox)

   **Connectivity:**
   - 5G Support (checkbox)
   - Wi-Fi (e.g., "Wi-Fi 6")
   - Bluetooth Version
   - NFC (checkbox)

   **Other Features:**
   - Operating System
   - Fingerprint Sensor (checkbox)
   - Water Resistance (e.g., "IP68")
   - Weight (grams)

5. **Set Availability**
   - Check **"Active"** to make phone visible
   - Uncheck to hide from users

6. **Save Phone**
   - Click **"Add Phone"** button
   - **Success Message:** "Phone added successfully!"
   - Redirected to phone list

#### C.3.2.2 Editing Phone

**Steps:**

1. **Find Phone**
   - Admin Panel → **"Manage Phones"**
   - Use search or scroll to find phone
   - Click **"Edit"** button

2. **Modify Information**
   - Update any field as needed
   - Change image (optional)
   - Update specifications

3. **Save Changes**
   - Click **"Update Phone"**
   - **Success Message:** "Phone updated successfully!"

#### C.3.2.3 Deleting Phone

**Steps:**

1. **Find Phone**
   - Admin Panel → **"Manage Phones"**
   - Locate phone to delete

2. **Delete Phone**
   - Click **"Delete"** button
   - **Confirmation Dialog:** "Are you sure you want to delete this phone?"
   - Click **"Confirm"**

3. **Verify Deletion**
   - **Success Message:** "Phone deleted successfully!"
   - Phone removed from list

**Note:** Deletion is permanent and cannot be undone.

#### C.3.2.4 Bulk Operations

**Deactivating Multiple Phones:**

1. **Select Phones**
   - Check checkboxes next to phones

2. **Choose Action**
   - Select **"Deactivate"** from dropdown
   - Click **"Apply"**

3. **Confirm**
   - **Success Message:** "5 phones deactivated successfully!"

### C.3.3 Managing Brands

**Objective:** Add or edit smartphone brands

**Prerequisites:** Admin logged in

#### C.3.3.1 Adding New Brand

**Steps:**

1. **Navigate to Brand Management**
   - Admin Panel → **"Manage Brands"**
   - Click **"Add New Brand"**

2. **Fill Brand Information**
   - **Brand Name:** Enter brand name (e.g., "XIAOMI")
   - **Description:** Brief description
   - **Website:** Official website URL
   - **Country of Origin:** Select country

3. **Upload Brand Logo**
   - Click **"Choose File"**
   - Select logo image
   - **Recommended:** 200x200px, transparent background

4. **Save Brand**
   - Click **"Add Brand"**
   - **Success Message:** "Brand added successfully!"

#### C.3.3.2 Editing Brand

**Steps:**

1. **Find Brand**
   - Locate brand in list
   - Click **"Edit"**

2. **Update Information**
   - Modify name, description, or logo

3. **Save Changes**
   - Click **"Update Brand"**

### C.3.4 Managing Users

**Objective:** View and manage user accounts

**Prerequisites:** Admin logged in

#### C.3.4.1 Viewing User List

**Steps:**

1. **Navigate to User Management**
   - Admin Panel → **"Manage Users"**

2. **View User Information**
   - Table displays:
     - User ID
     - Name
     - Email
     - Registration Date
     - Last Login
     - Status (Active/Suspended)
     - Role (User/Admin)

3. **Search Users**
   - Use search box to find by name or email

4. **Filter Users**
   - Filter by status (Active/Suspended)
   - Filter by role (User/Admin)
   - Filter by registration date

#### C.3.4.2 Viewing User Details

**Steps:**

1. **Select User**
   - Click **"View Details"** on user row

2. **View User Activity**
   - Profile information
   - Recommendation history (count)
   - Comparison history (count)
   - Chat history (count)
   - Last activity

#### C.3.4.3 Suspending User Account

**Steps:**

1. **Find User**
   - Locate user in user list

2. **Suspend Account**
   - Click **"Suspend"** button
   - **Confirmation:** "Are you sure you want to suspend this user?"
   - Click **"Confirm"**

3. **Email Notification Sent**
   - System automatically sends suspension email to user
   - Email includes:
     - Suspension notice
     - Reason (if provided)
     - Contact information for appeals

4. **Verify Suspension**
   - User status changes to "Suspended"
   - User cannot login
   - **Success Message:** "User suspended. Notification email sent."

#### C.3.4.4 Reactivating User Account

**Steps:**

1. **Find Suspended User**
   - Filter by status: "Suspended"

2. **Reactivate**
   - Click **"Reactivate"** button
   - **Confirmation:** "Reactivate this user account?"
   - Click **"Confirm"**

3. **Email Notification**
   - Reactivation email sent to user
   - User can login again

4. **Verify Reactivation**
   - Status changes to "Active"
   - **Success Message:** "User reactivated. Notification email sent."

### C.3.5 Creating New Admin (Super Admin Only)

**Objective:** Create new admin user

**Prerequisites:** Super Admin logged in

**Steps:**

1. **Navigate to Admin Management**
   - Admin Panel → **"Manage Admins"**
   - Click **"Create New Admin"**

2. **Fill Admin Information**
   - **Name:** Admin's full name
   - **Email:** Admin email address
   - **Password:** Temporary password (min 8 characters)
   - **Role:** Select role
     - **Admin:** Standard admin privileges
     - **Super Admin:** Full system access

3. **Set Permissions** (Optional)
   - Phone Management
   - Brand Management
   - User Management
   - System Logs Access

4. **Create Admin**
   - Click **"Create Admin"**
   - **Success Message:** "Admin created successfully!"

5. **Notify New Admin**
   - Email sent to new admin with:
     - Login credentials
     - First-time login instructions
     - Security recommendations

### C.3.6 Viewing System Logs

**Objective:** Monitor system activity and user actions

**Prerequisites:** Admin logged in

**Steps:**

1. **Access System Logs**
   - Admin Panel → **"System Logs"**

2. **View Log Entries**
   - Table displays:
     - Timestamp
     - User
     - Action Type
     - Details
     - IP Address

3. **Filter Logs**
   - **By Date Range:** Select start and end dates
   - **By Action Type:**
     - User Login/Logout
     - Recommendation Generated
     - Phone Added/Edited/Deleted
     - User Registered
     - Admin Action
     - Error/Warning
   - **By User:** Select specific user

4. **Export Logs**
   - Click **"Export to CSV"**
   - Download log file for analysis

5. **View Recommendation History**
   - Filter logs by "Recommendation Generated"
   - See all AI recommendations with criteria and results

### C.3.7 Replying to Contact Form Messages

**Objective:** Respond to user inquiries via email

**Prerequisites:** Admin logged in

**Steps:**

1. **Access Contact Messages**
   - Admin Panel → **"Contact Messages"**
   - Or **"Messages"** tab

2. **View Message List**
   - Table shows:
     - Date received
     - From (name and email)
     - Subject
     - Category
     - Status (New/Replied)

3. **Open Message**
   - Click on message row to view details
   - See full message content and user info

4. **Compose Reply**
   - Click **"Reply"** button
   - **To:** Auto-filled with user's email
   - **Subject:** Auto-filled with "Re: [original subject]"
   - **Message:** Type response

5. **Send Reply**
   - Click **"Send Reply"**
   - **Email sent** to user's email address
   - **Success Message:** "Reply sent successfully!"

6. **Mark as Resolved**
   - Message status changes to "Replied"
   - Can add internal notes for tracking

### C.3.8 Viewing Analytics Dashboard

**Objective:** Monitor system usage and statistics

**Prerequisites:** Admin logged in

**Steps:**

1. **Access Dashboard**
   - Admin Panel → **"Analytics"**
   - Or admin homepage

2. **View Key Metrics**
   - **Total Users:** Count of registered users
   - **Total Phones:** Number of phone listings
   - **Recommendations Today:** AI recommendations generated today
   - **Active Users:** Users active in last 24 hours

3. **View Charts**
   - **User Registration Trend:** Line chart over time
   - **Popular Brands:** Bar chart of most searched brands
   - **Price Range Distribution:** Pie chart of user budgets
   - **Recommendation Activity:** Activity over last 30 days

4. **View Top Phones**
   - Most viewed phones
   - Most recommended phones
   - Most compared phones

5. **Export Reports**
   - Click **"Generate Report"**
   - Select date range
   - Click **"Download PDF"**

---

## C.4 Database Maintenance Operations

### C.4.1 Backup Database

**Objective:** Create database backup

**Prerequisites:** Terminal access

**Steps:**

**Development (SQLite):**
```bash
cd /home/user/DialSmart
cp dialsmart.db backups/dialsmart_backup_$(date +%Y%m%d_%H%M%S).db
```

**Production (PostgreSQL):**
```bash
pg_dump -U username dialsmart_db > backup_$(date +%Y%m%d).sql
```

### C.4.2 Restore Database

**Development (SQLite):**
```bash
cp backups/dialsmart_backup_20240101.db dialsmart.db
```

**Production (PostgreSQL):**
```bash
psql -U username dialsmart_db < backup_20240101.sql
```

### C.4.3 Clear All Data

**Warning:** This permanently deletes all data!

```bash
flask shell
>>> from app import db
>>> db.drop_all()
>>> db.create_all()
>>> exit()
```

Or simply:
```bash
rm dialsmart.db
flask init-db
```

### C.4.4 Seed Fresh Data

```bash
flask seed-data
```

---

## C.5 Troubleshooting Common Operations

### C.5.1 Login Issues

| Problem | Solution |
|---------|----------|
| "Invalid email or password" | Verify credentials, check caps lock |
| "Account suspended" | Contact admin at admin@dialsmart.my |
| Session expired | Login again |
| Cannot access admin panel | Verify admin role with super admin |

### C.5.2 Recommendation Issues

| Problem | Solution |
|---------|----------|
| No recommendations returned | Adjust criteria (loosen budget/requirements) |
| Recommendations loading slowly | Check internet connection, wait up to 5 seconds |
| Error in wizard | Refresh page and start over |
| Preferences not saving | Ensure logged in, check form validation |

### C.5.3 File Upload Issues

| Problem | Solution |
|---------|----------|
| "File too large" | Reduce file size to under 16MB |
| "Invalid file type" | Use PNG, JPG, JPEG, or GIF formats only |
| Upload fails | Check internet connection, try smaller file |
| Image not displaying | Clear browser cache, check file path |

### C.5.4 Admin Panel Issues

| Problem | Solution |
|---------|----------|
| Cannot access admin panel | Verify admin role, login as admin |
| Changes not saving | Check form validation, ensure required fields filled |
| Bulk operations fail | Reduce number of items, try one at a time |
| Email notifications not sent | Check email configuration in config.py |

---

**End of Appendix C**
