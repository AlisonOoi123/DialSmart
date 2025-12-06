# Appendix A: User Guide

## A.1 Login Credentials for All User Roles

The following table lists all user accounts available for testing the DialSmart system:

| User Role | Email | Password | Purpose |
|-----------|-------|----------|---------|
| **Regular User (Test)** | user@dialsmart.my | password123 | Testing standard user features |
| **Regular User (Sample)** | ahmad@gmail.com | SecurePass123! | Sample user for testing scenarios |
| **Admin** | admin@dialsmart.my | admin123 | Admin panel access and management |
| **Super Admin** | superadmin@dialsmart.my | superadmin123 | Full system access including admin creation |
| **Guest User** | - | - | No login required for browsing and contact form |

**Note:** These credentials are for development and testing purposes only. In production, create new secure credentials using `flask create-admin` command.

---

## A.2 User Interface Walkthrough

This section provides detailed screenshots and explanations for each major page and functionality in the DialSmart system.

### A.2.1 Landing Page (Homepage)

**URL:** `http://localhost:5000/`

**Purpose:** First page users see when visiting DialSmart. Showcases featured brands and latest phones.

**Key Features:**
- **Navigation Bar:**
  - DialSmart logo (left) - Click to return home
  - Browse Phones - Navigate to phone catalog
  - Recommendations - Get AI recommendations (requires login)
  - Compare - Compare phones side-by-side
  - Chatbot - AI assistant button
  - Login/Register - User authentication (right side)

- **Hero Section:**
  - Welcome message: "Find Your Perfect Smartphone"
  - Subtitle: "AI-powered recommendations tailored for Malaysian users"
  - "Get Started" button - Leads to recommendation wizard

- **Featured Brands Section:**
  - Displays brand logos (Samsung, Apple, Xiaomi, Huawei, etc.)
  - Click on brand to see phones from that brand
  - Responsive grid layout (5 columns on desktop, 3 on tablet, 2 on mobile)

- **Latest Phones Section:**
  - Shows 6 most recently added phones
  - Each phone card shows:
    - Phone image
    - Model name
    - Brand name
    - Price in RM (Malaysian Ringgit)
    - "View Details" button

- **Footer:**
  - Contact information: support@dialsmart.my, +60 3-1234 5678
  - Quick links: About Us, Contact, Privacy Policy
  - Copyright notice

**Screenshot Description:**
*(In actual appendix, insert screenshot here)*
- Full-width landing page showing hero banner
- Featured brands with logos in grid
- Latest phones displayed as cards
- Navigation bar at top with all menu items

---

### A.2.2 User Registration Page

**URL:** `http://localhost:5000/auth/register`

**Purpose:** Allow new users to create an account.

**Form Fields:**
1. **Full Name** (Required)
   - Text input
   - Example: "Ahmad bin Abdullah"

2. **Email Address** (Required)
   - Email input with validation
   - Example: "ahmad@gmail.com"
   - Must be unique (not already registered)

3. **Password** (Required)
   - Password input (masked)
   - Minimum 8 characters
   - Should include letters and numbers

4. **Confirm Password** (Required)
   - Must match password field

5. **User Category** (Optional)
   - Dropdown selection:
     - Student
     - Working Professional
     - Business Owner
     - Retiree
     - Other

6. **Age Range** (Optional)
   - Dropdown selection:
     - 18-25
     - 26-35
     - 36-45
     - 46-55
     - 56+

**Buttons:**
- **Register** - Submit registration form
- **Already have an account? Login** - Link to login page

**Validation Messages:**
- "All fields are required" - If any required field is empty
- "Passwords do not match" - If password and confirm password differ
- "Email already registered" - If email exists in database
- "Please enter a valid email address" - If email format is invalid

**Screenshot Description:**
*(In actual appendix, insert screenshot here)*
- Registration form with all fields
- Submit button at bottom
- Link to login page for existing users

---

### A.2.3 User Login Page

**URL:** `http://localhost:5000/auth/login`

**Purpose:** Authenticate registered users to access personalized features.

**Form Fields:**
1. **Email Address** (Required)
   - Email input
   - Example: "user@dialsmart.my"

2. **Password** (Required)
   - Password input (masked)

3. **Remember Me** (Optional)
   - Checkbox
   - Keeps user logged in for 7 days

**Buttons:**
- **Login** - Submit login credentials
- **Forgot Password?** - Link to password reset
- **Don't have an account? Register** - Link to registration

**Error Messages:**
- "Invalid email or password" - If credentials don't match
- "Your account has been suspended. Please contact support." - If account is inactive
- "Please enter your email and password" - If fields are empty

**Success:**
- Regular users redirected to `/dashboard`
- Admin users redirected to `/admin/dashboard`

**Screenshot Description:**
*(In actual appendix, insert screenshot here)*
- Login form with email and password
- Remember me checkbox
- Forgot password link
- Register link for new users

---

### A.2.4 User Dashboard

**URL:** `http://localhost:5000/dashboard` (Requires login)

**Purpose:** Central hub for user's personalized data and quick access to features.

**Dashboard Widgets:**

1. **Welcome Section**
   - Displays: "Welcome back, [User Name]!"
   - Last login date/time

2. **Quick Stats Cards**
   - **Total Recommendations:** Count of AI recommendations received
   - **Saved Comparisons:** Count of saved phone comparisons
   - **Preferences Set:** Status indicator (Yes/No)

3. **Recent Recommendations Section**
   - Shows last 5 recommendations
   - Each entry displays:
     - Recommended phone model
     - Match score (percentage)
     - Date of recommendation
     - "View Details" button
   - "View All History" button at bottom

4. **Saved Comparisons Section**
   - Shows last 5 saved comparisons
   - Each entry displays:
     - Phone 1 vs Phone 2 names
     - Comparison date
     - "View Comparison" button
   - "View All Comparisons" button at bottom

5. **Quick Actions Section**
   - **Get New Recommendations** button
   - **Browse Phones** button
   - **Update Preferences** button
   - **Chat with AI** button

6. **User Preferences Summary**
   - Budget range: RM X - RM Y
   - Primary usage: [Gaming/Photography/etc.]
   - Preferred brands: [Samsung, Apple, etc.]
   - "Edit Preferences" link

**Screenshot Description:**
*(In actual appendix, insert screenshot here)*
- Dashboard with all widgets visible
- Recent recommendations list
- Saved comparisons section
- Quick action buttons

---

### A.2.5 AI Recommendation Wizard

**URL:** `http://localhost:5000/recommendation/wizard`

**Purpose:** Step-by-step guided process to get personalized phone recommendations.

**Wizard Steps:**

**Step 1: Budget Range**
- Question: "What is your budget for a new smartphone?"
- Input: Dual range slider
  - Minimum: RM 500
  - Maximum: RM 10,000
- Display: Current selection (e.g., "RM 1,500 - RM 3,000")
- "Next" button

**Step 2: Primary Usage**
- Question: "What will you primarily use your phone for?"
- Options (multi-select checkboxes):
  - ☐ Gaming
  - ☐ Photography/Videography
  - ☐ Business/Work
  - ☐ Social Media
  - ☐ Entertainment (Videos/Music)
  - ☐ General Use
- "Back" and "Next" buttons

**Step 3: Important Features**
- Question: "Which features are most important to you?"
- Options (multi-select checkboxes):
  - ☐ 5G Connectivity
  - ☐ High RAM (8GB+)
  - ☐ Large Battery (4500mAh+)
  - ☐ Fast Charging
  - ☐ High Resolution Camera
  - ☐ Water Resistance
  - ☐ Dual SIM
  - ☐ Wireless Charging
- "Back" and "Next" buttons

**Step 4: Brand Preferences**
- Question: "Do you prefer any specific brands?"
- Options (multi-select checkboxes):
  - ☐ Samsung
  - ☐ Apple
  - ☐ Xiaomi
  - ☐ Huawei
  - ☐ Oppo
  - ☐ Vivo
  - ☐ Realme
  - ☐ OnePlus
  - ☐ No Preference
- "Back" and "Get Recommendations" buttons

**Step 5: Results**
- Displays 3-5 recommended phones
- Each recommendation shows:
  - Phone image
  - Model name and brand
  - Price in RM
  - **Match Score:** XX% (with colored progress bar)
  - **Why this phone:** Brief reasoning (e.g., "Excellent camera within your budget, supports 5G")
  - Key specifications:
    - RAM/Storage
    - Main Camera MP
    - Battery Capacity
    - 5G Support
  - "View Full Details" button
  - "Compare" button
- "Start Over" button
- "Save Recommendations" button

**Screenshot Description:**
*(In actual appendix, insert screenshots for each step)*
1. Budget selection slider
2. Primary usage selection
3. Important features checkboxes
4. Brand preferences
5. Recommendation results with match scores

---

### A.2.6 Browse Phones Page

**URL:** `http://localhost:5000/browse`

**Purpose:** Browse all available phones with filtering and sorting options.

**Filter Panel (Left Sidebar):**

1. **Brand Filter**
   - Checkboxes for each brand:
     - ☐ Samsung
     - ☐ Apple
     - ☐ Xiaomi
     - ☐ Huawei
     - ☐ Oppo
     - ☐ Vivo
     - ☐ Realme
     - ☐ Others
   - "Apply" button

2. **Price Range**
   - Min: [Input field] RM
   - Max: [Input field] RM
   - "Apply" button

3. **Specifications**
   - **5G Support:** ☐ Yes
   - **Minimum RAM:** Dropdown (4GB, 6GB, 8GB, 12GB)
   - **Minimum Storage:** Dropdown (64GB, 128GB, 256GB, 512GB)
   - **Minimum Battery:** Input (mAh)
   - "Apply Filters" button

4. **Clear All Filters** button

**Main Content Area:**

1. **Results Summary**
   - "Showing X phones" or "No phones match your criteria"

2. **Sort Options (Top Right)**
   - Dropdown:
     - Newest First (default)
     - Price: Low to High
     - Price: High to Low
     - Name: A-Z
     - Name: Z-A

3. **View Toggle**
   - Grid view (default) - 4 columns on desktop
   - List view - Full-width cards

4. **Items Per Page**
   - Dropdown: 12, 24, 48 items per page

5. **Phone Grid/List**
   - **Grid View:** Each phone card shows:
     - Phone image (hover for quick view)
     - Model name
     - Brand
     - Price (RM)
     - Key specs (RAM/Storage, Camera)
     - "View Details" button
     - "Compare" checkbox

   - **List View:** Horizontal cards with:
     - Phone image (left)
     - Model name, brand, price
     - Full specifications listed
     - "View Details" and "Add to Compare" buttons

6. **Pagination**
   - Previous | 1 2 3 ... 10 | Next
   - "Go to page" input

**Screenshot Description:**
*(In actual appendix, insert screenshot here)*
- Browse page with filter sidebar on left
- Phone grid in main area
- Sort and view options at top
- Pagination at bottom

---

### A.2.7 Phone Comparison Page

**URL:** `http://localhost:5000/compare`

**Purpose:** Compare two phones side-by-side with detailed specifications.

**Phone Selection Section:**

1. **Phone 1 Selector**
   - Search box: "Search for first phone..."
   - Autocomplete suggestions as you type
   - Selected phone displays:
     - Phone image
     - Model name
     - Brand
     - Price
     - "Change" button

2. **VS** indicator (center)

3. **Phone 2 Selector**
   - Search box: "Search for second phone..."
   - Same features as Phone 1 selector

4. **Compare Button**
   - Large blue button
   - Only enabled when both phones selected

**Comparison Table:**

Displays side-by-side comparison with winner indicators (✓ highlighted in green):

| Category | Phone 1 | Phone 2 |
|----------|---------|---------|
| **Price** | RM 5,299 ✓ | RM 5,999 |
| **Brand** | Samsung | Apple |
| **Display** | | |
| - Screen Size | 6.8" ✓ | 6.7" |
| - Resolution | 1440x3088 | 1290x2796 |
| - Screen Type | Dynamic AMOLED 2X | LTPO Super Retina XDR |
| - Refresh Rate | 120Hz | 120Hz |
| **Performance** | | |
| - Processor | Snapdragon 8 Gen 2 | A17 Pro ✓ |
| - RAM | 8GB, 12GB ✓ | 8GB |
| - Storage | 256GB, 512GB, 1TB ✓ | 256GB, 512GB, 1TB ✓ |
| **Camera** | | |
| - Rear Camera | 200MP ✓ + 10MP + 10MP + 12MP | 48MP + 12MP + 12MP |
| - Front Camera | 12MP | 12MP |
| **Battery** | | |
| - Capacity | 5000mAh ✓ | 4441mAh |
| - Charging | 45W Fast Charging | 27W Fast Charging |
| - Wireless Charging | Yes ✓ | Yes ✓ |
| **Connectivity** | | |
| - 5G | Yes ✓ | Yes ✓ |
| - WiFi | WiFi 6E | WiFi 6E |
| - NFC | Yes ✓ | Yes ✓ |
| **Other Features** | | |
| - OS | Android 13 | iOS 17 ✓ |
| - Fingerprint | In-display ✓ | No |
| - Face Unlock | Yes ✓ | Yes ✓ |
| - Water Resistance | IP68 ✓ | IP68 ✓ |
| - Weight | 234g | 221g ✓ |

**Overall Winner Section:**
- **Winner:** [Phone Name]
- **Score:** X out of 15 categories
- Brief explanation: "This phone won in price, display size, camera, and battery categories"

**Action Buttons:**
- **Save Comparison** - Save to comparison history
- **Start New Comparison** - Clear and compare different phones
- **Share** - Generate shareable link

**Screenshot Description:**
*(In actual appendix, insert screenshot here)*
- Phone selection at top
- Full comparison table
- Winner indicators highlighted
- Overall winner announcement
- Action buttons at bottom

---

### A.2.8 Chatbot Interface

**URL:** Accessible from any page via floating button (bottom right)

**Purpose:** Interactive AI assistant for phone recommendations and queries.

**Chat Window Components:**

1. **Header**
   - "DialSmart AI Assistant"
   - Minimize button
   - Close button

2. **Chat History Area**
   - Displays conversation messages
   - **System Messages** (left side, gray bubble):
     - "Hello! I'm DialSmart AI Assistant. How can I help you find the perfect smartphone?"
   - **User Messages** (right side, blue bubble):
     - User's typed messages
   - **AI Responses** (left side, white bubble):
     - Text responses
     - Phone recommendations (as cards)
     - Quick reply buttons

3. **Quick Reply Buttons** (when applicable)
   - "Find a phone"
   - "Budget options"
   - "Popular brands"
   - "Compare phones"

4. **Input Area**
   - Text input field: "Type your message..."
   - Send button (paper plane icon)
   - Character count (optional)

**Sample Conversations:**

**Example 1: Budget Query**
- **User:** "I'm looking for a phone under RM2000"
- **AI:** "Here are the top phones within RM500 - RM2000:

  📱 Samsung Galaxy A54 - RM1,899.00
  📱 Xiaomi 12T - RM1,799.00
  📱 Realme GT Neo 3 - RM1,699.00

  Would you like more details about any of these?"

**Example 2: Usage-Based Query**
- **User:** "Best phone for gaming"
- **AI:** "For gaming, I recommend phones with high RAM and refresh rate. Here are the best options:

  📱 ASUS ROG Phone 7 - RM4,299.00
  - ✨ 90% match
  - 16GB RAM, 165Hz display

  📱 Xiaomi Black Shark 5 Pro - RM3,499.00
  - ✨ 85% match
  - 12GB RAM, 144Hz display"

**Example 3: Brand Query**
- **User:** "Show me Samsung phones"
- **AI:** "Here are popular Samsung phones:

  📱 Samsung Galaxy S23 Ultra - RM5,299.00
  📱 Samsung Galaxy S23 - RM3,899.00
  📱 Samsung Galaxy A54 - RM1,899.00

  Which price range interests you?"

**Example 4: Help Query**
- **User:** "What can you do?"
- **AI:** "I can help you with:

  📱 Find phone recommendations based on your needs
  💰 Search phones within your budget
  🔍 Compare different phone models
  📊 Get detailed specifications
  🏷️ Browse phones by brand

  Just ask me anything!"

**Screenshot Description:**
*(In actual appendix, insert screenshot here)*
- Chatbot window with conversation history
- User and AI message bubbles
- Quick reply buttons
- Input field at bottom

---

### A.2.9 User Profile Page

**URL:** `http://localhost:5000/profile` (Requires login)

**Purpose:** View and update user profile information.

**Profile Information Section:**

1. **Personal Details**
   - **Full Name:** [Editable text field]
   - **Email:** [Display only, cannot be changed]
   - **User Category:** [Dropdown: Student, Working Professional, etc.]
   - **Age Range:** [Dropdown: 18-25, 26-35, etc.]
   - **Member Since:** [Display only, e.g., "January 2024"]
   - **Last Active:** [Display only, e.g., "2 hours ago"]

2. **Update Profile Button**

**Change Password Section:**

1. **Current Password:** [Password input, required]
2. **New Password:** [Password input, minimum 8 characters]
3. **Confirm New Password:** [Password input, must match]
4. **Change Password Button**

**Account Statistics:**
- Total Recommendations Received: XX
- Total Comparisons Made: XX
- Chatbot Conversations: XX
- Account Status: Active ✓

**Validation Messages:**
- "Profile updated successfully" (success)
- "Current password is incorrect" (error)
- "New passwords do not match" (error)
- "Password changed successfully" (success)

**Screenshot Description:**
*(In actual appendix, insert screenshot here)*
- Profile form with all fields
- Change password section
- Account statistics
- Update buttons

---

### A.2.10 User Preferences Page

**URL:** `http://localhost:5000/preferences` (Requires login)

**Purpose:** Set and update phone preference criteria for better recommendations.

**Preference Categories:**

**1. Budget Range**
- **Minimum Budget:** Slider or input (RM 500 - RM 10,000)
- **Maximum Budget:** Slider or input (RM 500 - RM 10,000)
- Visual: Dual-handle range slider
- Display: "RM 1,000 - RM 3,000"

**2. Technical Specifications**
- **Minimum RAM:** Dropdown (4GB, 6GB, 8GB, 12GB, 16GB)
- **Minimum Storage:** Dropdown (64GB, 128GB, 256GB, 512GB, 1TB)
- **Minimum Camera (MP):** Input field
- **Minimum Battery (mAh):** Input field
- **5G Required:** Checkbox ☐ Yes

**3. Display Preferences**
- **Minimum Screen Size:** Dropdown (5.5", 6.0", 6.5", 6.7", 7.0")
- **Maximum Screen Size:** Dropdown (5.5" - 7.0")
- **Preferred Screen Type:** Checkboxes
  - ☐ AMOLED
  - ☐ LCD
  - ☐ OLED
  - ☐ No Preference

**4. Primary Usage** (Multi-select)
- ☐ Gaming
- ☐ Photography/Videography
- ☐ Business/Work
- ☐ Social Media
- ☐ Entertainment
- ☐ General Use

**5. Important Features** (Multi-select)
- ☐ Fast Charging
- ☐ Wireless Charging
- ☐ Water Resistance
- ☐ Dual SIM
- ☐ Fingerprint Sensor
- ☐ Face Unlock
- ☐ NFC
- ☐ Expandable Storage

**6. Brand Preferences** (Multi-select)
- ☐ Samsung
- ☐ Apple
- ☐ Xiaomi
- ☐ Huawei
- ☐ Oppo
- ☐ Vivo
- ☐ Realme
- ☐ OnePlus
- ☐ Others

**Action Buttons:**
- **Save Preferences** - Save and redirect to dashboard
- **Reset to Default** - Clear all preferences
- **Cancel** - Return to dashboard without saving

**Success Messages:**
- "Preferences updated successfully! Your recommendations will reflect these changes."

**Screenshot Description:**
*(In actual appendix, insert screenshot here)*
- Preferences form with all categories
- Sliders, dropdowns, and checkboxes
- Save and reset buttons

---

### A.2.11 Admin Dashboard

**URL:** `http://localhost:5000/admin/dashboard` (Admin login required)

**Purpose:** Overview of system statistics and admin management tools.

**Admin Navigation (Sidebar):**
- Dashboard (home icon)
- Manage Phones
- Manage Brands
- Manage Users
- System Logs
- Contact Requests (NEW)
- Settings

**Dashboard Statistics Cards:**

1. **Total Users**
   - Number: XXX
   - Icon: Users icon
   - Trend: "+15 this week"

2. **Total Phones**
   - Number: XXX
   - Icon: Phone icon
   - Status: "X active, Y inactive"

3. **Total Brands**
   - Number: XX
   - Icon: Brand icon

4. **Today's Recommendations**
   - Number: XX
   - Icon: Star icon

**Charts and Graphs:**

1. **Recommendation Activity (Line Chart)**
   - Last 7 days
   - Shows daily recommendation count

2. **Popular Brands (Pie Chart)**
   - Shows distribution of phone views by brand

3. **User Growth (Area Chart)**
   - Last 30 days
   - New user registrations

**Recent Activity Tables:**

1. **Recent Users (Last 5)**
   - Name
   - Email
   - Registration Date
   - Status (Active/Inactive)
   - Actions: View | Suspend/Activate

2. **Popular Phones (Top 5)**
   - Phone Model
   - Brand
   - Times Recommended
   - Times Compared
   - Last Viewed

**Quick Actions:**
- ➕ Add New Phone
- ➕ Add New Brand
- 👥 View All Users
- 📊 View Full Logs
- ✉️ View Contact Requests

**Screenshot Description:**
*(In actual appendix, insert screenshot here)*
- Admin dashboard with statistics cards
- Charts showing system activity
- Recent activity tables
- Quick action buttons

---

### A.2.12 Phone Management (Admin)

**URL:** `http://localhost:5000/admin/phones`

**Purpose:** Admin CRUD operations for managing phone listings.

**Phone List View:**

**Header Actions:**
- Search box: "Search phones..."
- Filter by brand dropdown
- "Add New Phone" button (prominent, green)

**Phone Table:**
Columns:
- Image (thumbnail)
- Model Name
- Brand
- Price (RM)
- Status (Active/Inactive badge)
- Added Date
- Actions (Edit | Delete buttons)

**Pagination:**
- Showing X-Y of Z phones
- 20 phones per page
- Previous | 1 2 3 | Next

**Add/Edit Phone Form:**

**Basic Information:**
1. **Model Name:** [Text input, required]
2. **Brand:** [Dropdown, required]
3. **Price (RM):** [Number input, required]
4. **Model Number:** [Text input, optional]
5. **Availability Status:** [Dropdown: Available, Out of Stock, Coming Soon]
6. **Main Image:** [File upload, accepts JPG/PNG]

**Display Specifications:**
7. **Screen Size (inches):** [Number input]
8. **Resolution:** [Text input, e.g., "1440x3088"]
9. **Screen Type:** [Text input, e.g., "AMOLED"]
10. **Refresh Rate (Hz):** [Number input]

**Performance Specifications:**
11. **Processor:** [Text input]
12. **Processor Brand:** [Text input]
13. **RAM Options:** [Text input, e.g., "8GB, 12GB"]
14. **Storage Options:** [Text input, e.g., "256GB, 512GB"]
15. **Expandable Storage:** [Checkbox]

**Camera Specifications:**
16. **Rear Camera:** [Text input, e.g., "50MP + 12MP + 5MP"]
17. **Rear Camera Main (MP):** [Number input]
18. **Front Camera:** [Text input, e.g., "32MP"]
19. **Front Camera (MP):** [Number input]

**Battery & Charging:**
20. **Battery Capacity (mAh):** [Number input]
21. **Charging Speed:** [Text input, e.g., "45W Fast Charging"]
22. **Wireless Charging:** [Checkbox]

**Connectivity:**
23. **5G Support:** [Checkbox]
24. **WiFi Standard:** [Text input, e.g., "WiFi 6E"]
25. **Bluetooth Version:** [Text input, e.g., "5.3"]
26. **NFC:** [Checkbox]

**Other Features:**
27. **Operating System:** [Text input, e.g., "Android 13"]
28. **Fingerprint Sensor:** [Checkbox]
29. **Face Unlock:** [Checkbox]
30. **Water Resistance:** [Text input, e.g., "IP68"]
31. **Dual SIM:** [Checkbox]
32. **Weight (grams):** [Number input]
33. **Dimensions:** [Text input, e.g., "163.4 x 78.1 x 8.9 mm"]
34. **Available Colors:** [Text input, e.g., "Black, White, Green"]

**Action Buttons:**
- **Save Phone** (Create new or Update existing)
- **Cancel** (Return to phone list)

**Delete Confirmation Dialog:**
- "Are you sure you want to delete this phone? This action cannot be undone."
- Cancel | Confirm Delete buttons

**Screenshot Description:**
*(In actual appendix, insert screenshots here)*
1. Phone list table with all phones
2. Add phone form (page 1 - basic info)
3. Add phone form (page 2 - specifications)
4. Edit phone form with data pre-filled
5. Delete confirmation dialog

---

### A.2.13 Brand Management (Admin)

**URL:** `http://localhost:5000/admin/brands`

**Purpose:** Manage smartphone brands in the system.

**Brand List View:**

**Header:**
- "Add New Brand" button

**Brand Table:**
Columns:
- Logo (image thumbnail)
- Brand Name
- Description (truncated)
- Phone Count (number of phones with this brand)
- Featured (Yes/No badge)
- Status (Active/Inactive)
- Actions (Edit | Delete)

**Add/Edit Brand Form:**

1. **Brand Name:** [Text input, required]
2. **Description:** [Textarea, optional]
3. **Tagline:** [Text input, optional]
4. **Brand Logo:** [File upload, JPG/PNG]
5. **Featured Brand:** [Checkbox] - "Display on homepage"
6. **Active Status:** [Checkbox] - "Brand is active"

**Action Buttons:**
- Save Brand
- Cancel

**Validation:**
- Cannot delete brand if it has associated phones
- Duplicate brand names not allowed

**Screenshot Description:**
*(In actual appendix, insert screenshot here)*
- Brand list with logos
- Add/Edit brand form
- Logo upload preview

---

### A.2.14 User Management (Admin)

**URL:** `http://localhost:5000/admin/users`

**Purpose:** View and manage registered users.

**User List View:**

**Filters:**
- Search: "Search by name or email..."
- User Type: Dropdown (All, Student, Working Professional, etc.)

**User Table:**
Columns:
- Full Name
- Email
- User Category
- Registration Date
- Last Active
- Status (Active/Suspended badge)
- Admin (Yes/No badge)
- Actions (View | Suspend/Activate)

**User Details Page:**

**User Information:**
- Full Name
- Email Address
- User Category
- Age Range
- Registration Date
- Last Active
- Account Status
- Total Logins

**User Activity:**
- **Recommendations:** XX total
  - List of recent recommendations
- **Comparisons:** XX total
  - List of recent comparisons
- **Chatbot Sessions:** XX total
- **Contact Submissions:** XX total

**User Preferences:**
- Budget Range
- Primary Usage
- Preferred Brands
- Important Features

**Actions:**
- **Suspend Account** button (red) - Deactivates user and sends email
- **Activate Account** button (green) - Reactivates user
- **View Full Activity** button

**Suspend Confirmation:**
- "Are you sure you want to suspend this user account? They will be notified via email."
- Optional reason field
- Cancel | Confirm Suspend

**Screenshot Description:**
*(In actual appendix, insert screenshot here)*
1. User list table
2. User details page with activity
3. Suspend confirmation dialog

---

### A.2.15 System Logs (Admin)

**URL:** `http://localhost:5000/admin/logs`

**Purpose:** Monitor system activity and user actions.

**Log Filters:**

1. **Date Range:**
   - From: [Date picker]
   - To: [Date picker]

2. **User:** [Dropdown: All Users, or select specific user]

3. **Action Type:** [Dropdown]
   - All Actions
   - User Registration
   - User Login
   - Recommendation Request
   - Phone Comparison
   - Chatbot Interaction
   - Admin Actions

4. **Search:** "Search in logs..."

5. **Apply Filters** button

**Log Table:**
Columns:
- Timestamp (Date & Time)
- User (Name/Email)
- Action Type
- Details (brief description)
- IP Address (optional)
- View Details (expand icon)

**Expanded Log Entry:**
- Full details of the action
- Request parameters
- Response status
- Duration (if applicable)

**Export Options:**
- **Export to CSV** button
- **Export to PDF** button
- Date range for export

**Pagination:**
- 50 logs per page
- Previous | 1 2 3 ... | Next

**Screenshot Description:**
*(In actual appendix, insert screenshot here)*
- System logs table with filters
- Expanded log entry showing details
- Export options

---

### A.2.16 Contact Form & Admin Reply

**URL (User):** `http://localhost:5000/contact`
**URL (Admin):** `http://localhost:5000/admin/contacts`

**Purpose:** Allow users to submit inquiries and admins to reply via email.

**User Contact Form:**

**Form Fields:**
1. **Your Name:** [Text input, required]
2. **Your Email:** [Email input, required]
3. **Subject:** [Text input, required]
4. **Message:** [Textarea, required, min 10 characters]

**Submit Button:** "Send Message"

**Success Message:**
- "Thank you for contacting us. We will get back to you soon."
- Auto-acknowledgment email sent to user

**Admin Contact Management:**

**Contact Requests List:**

**Filters:**
- Status: [All, Pending, Replied]
- Date Range: [From - To]

**Table:**
Columns:
- Date Submitted
- Name
- Email
- Subject (truncated)
- Status (Pending/Replied badge)
- Actions (View | Reply)

**View Contact Request:**

**Request Details:**
- From: [Name] ([Email])
- Date: [Timestamp]
- Subject: [Subject line]
- Message: [Full message text]
- Status: Pending/Replied

**Reply Section:**
- **Reply Message:** [Textarea]
- **Send Reply** button

**Reply Process:**
1. Admin writes reply message
2. Clicks "Send Reply"
3. System sends email from support@dialsmart.my to user
4. Email includes:
   - Admin's reply
   - Original message quoted
   - Support contact information
5. Request status changed to "Replied"
6. Reply saved in database

**Screenshot Description:**
*(In actual appendix, insert screenshot here)*
1. User contact form
2. Admin contact requests list
3. View request with reply form
4. Replied status indicator

---

## A.3 Function Reference Guide

### A.3.1 Common Actions

**How to Get Phone Recommendations:**
1. Click "Get Recommendations" button on dashboard or navigation
2. Complete the recommendation wizard (4 steps)
3. View recommended phones with match scores
4. Click "View Full Details" to see complete specifications
5. Optionally save recommendations to history

**How to Compare Phones:**
1. Navigate to "Compare" page
2. Search for first phone in Phone 1 selector
3. Search for second phone in Phone 2 selector
4. Click "Compare" button
5. Review side-by-side comparison table
6. Click "Save Comparison" to save to history

**How to Use Chatbot:**
1. Click chatbot icon (bottom right corner)
2. Type your question in the message box
3. Press Enter or click Send button
4. Read AI response
5. Click quick reply buttons if available
6. Continue conversation as needed

**How to Browse Phones:**
1. Click "Browse Phones" in navigation
2. Use filters in left sidebar to narrow down options
3. Select brands, set price range, choose specifications
4. Click "Apply Filters"
5. Sort results using dropdown (price, name, date)
6. Click on phone card to view details

**How to Update Preferences:**
1. Navigate to Dashboard
2. Click "Update Preferences" or go to /preferences
3. Adjust budget sliders
4. Select primary usage and features
5. Choose preferred brands
6. Click "Save Preferences"
7. Future recommendations will use these preferences

**How to Change Password:**
1. Go to Profile page (/profile)
2. Enter current password
3. Enter new password (minimum 8 characters)
4. Confirm new password
5. Click "Change Password"
6. Success message appears
7. Use new password for next login

**How to View Recommendation History:**
1. Go to Dashboard
2. Scroll to "Recent Recommendations" section
3. Click "View All History"
4. Browse all past recommendations
5. Click on any recommendation to see details
6. Filter by date range if needed

**How to Logout:**
1. Click username in top-right navigation
2. Select "Logout" from dropdown menu
3. Redirected to homepage
4. Session ended

---

### A.3.2 Admin Actions

**How to Add a New Phone:**
1. Login as admin
2. Go to Admin Dashboard
3. Click "Manage Phones" in sidebar
4. Click "Add New Phone" button
5. Fill in all required fields (name, brand, price)
6. Upload phone image
7. Enter all specifications (display, camera, battery, etc.)
8. Click "Save Phone"
9. Phone added to database and appears in browse

**How to Edit Phone Information:**
1. Go to Manage Phones
2. Find phone in list (use search if needed)
3. Click "Edit" button
4. Modify desired fields
5. Upload new image if needed
6. Click "Update Phone"
7. Changes saved and reflected immediately

**How to Delete a Phone:**
1. Go to Manage Phones
2. Click "Delete" button on phone row
3. Read confirmation dialog
4. Click "Confirm Delete" to proceed
5. Phone removed from database
6. Phone no longer appears in recommendations or browse

**How to Suspend/Activate User:**
1. Go to Manage Users
2. Search for user by name or email
3. Click user name to view details
4. Click "Suspend Account" button
5. Optionally enter reason
6. Confirm action
7. User account suspended, email notification sent
8. To reactivate: Click "Activate Account" button

**How to Reply to Contact Request:**
1. Go to Admin Dashboard
2. Click "Contact Requests" in sidebar
3. Find pending request in list
4. Click "View" or "Reply" button
5. Read user's message
6. Type reply in message box
7. Click "Send Reply"
8. Email sent to user from support@dialsmart.my
9. Status changed to "Replied"

**How to View System Logs:**
1. Go to Admin Dashboard
2. Click "System Logs" in sidebar
3. Apply filters (date range, user, action type)
4. Click "Apply Filters"
5. Review log entries in table
6. Click expand icon to see full details
7. Export to CSV/PDF if needed

**How to Create New Admin (Super Admin Only):**
1. Login as Super Admin
2. Go to Manage Users
3. Click "Create New Admin" button (only visible to Super Admin)
4. Enter admin details (name, email, password)
5. Select admin level
6. Click "Create Admin"
7. New admin account created
8. Welcome email sent with credentials

---

## A.4 Troubleshooting Guide

### A.4.1 Common User Issues

**Cannot Login:**
- **Issue:** "Invalid email or password" error
- **Solution:**
  1. Verify email is correct
  2. Check Caps Lock is off
  3. Try "Forgot Password" to reset
  4. Ensure account is not suspended (contact admin)

**Forgot Password:**
- **Issue:** Cannot remember password
- **Solution:**
  1. Click "Forgot Password" on login page
  2. Enter registered email
  3. Check inbox for password reset email
  4. Click reset link in email
  5. Enter new password
  6. Confirm new password
  7. Login with new password

**No Recommendations Showing:**
- **Issue:** "No phones match your criteria"
- **Solution:**
  1. Adjust budget range (make it wider)
  2. Remove some feature requirements
  3. Clear brand preferences
  4. Reset filters and try again
  5. Contact admin if issue persists

**Chatbot Not Responding:**
- **Issue:** Chatbot window won't open or send messages
- **Solution:**
  1. Refresh the page
  2. Clear browser cache
  3. Try a different browser
  4. Check internet connection
  5. Contact admin if issue continues

**Cannot Save Comparison:**
- **Issue:** "Save Comparison" button doesn't work
- **Solution:**
  1. Ensure you are logged in
  2. Refresh the page
  3. Try comparing again
  4. Check browser console for errors
  5. Report to admin if problem persists

### A.4.2 Admin Issues

**Cannot Upload Phone Image:**
- **Issue:** Image upload fails
- **Solution:**
  1. Check file size (must be under 16MB)
  2. Verify file type (JPG, PNG only)
  3. Rename file (remove special characters)
  4. Try smaller image
  5. Check server disk space

**User Suspension Email Not Sent:**
- **Issue:** User not receiving suspension notification
- **Solution:**
  1. Verify email service is configured
  2. Check user's email address is correct
  3. Ask user to check spam folder
  4. Review system logs for email errors
  5. Configure email settings in config.py

**Cannot Delete Brand:**
- **Issue:** "Cannot delete brand with existing phones" error
- **Solution:**
  1. This is by design to maintain data integrity
  2. First, reassign or delete all phones with this brand
  3. Then delete the brand
  4. Or mark brand as "Inactive" instead

---

## A.5 Tips and Best Practices

### A.5.1 For Users

1. **Set Your Preferences First:**
   - Complete your preferences before getting recommendations
   - This improves recommendation accuracy
   - Update preferences when your needs change

2. **Use the Chatbot for Quick Queries:**
   - Faster than browsing manually
   - Natural language makes it easy
   - Can ask follow-up questions

3. **Save Important Comparisons:**
   - Keep track of phones you're considering
   - Easy to review later
   - Share with friends/family for advice

4. **Check Match Scores:**
   - Higher scores = better match for your needs
   - Read the reasoning for each recommendation
   - Don't just focus on brand names

5. **Update Your Preferences Regularly:**
   - As your budget changes
   - When new features become important
   - After reading reviews or getting feedback

### A.5.2 For Administrators

1. **Keep Phone Data Updated:**
   - Add new models regularly
   - Update prices when they change
   - Mark out-of-stock phones as unavailable

2. **Monitor System Logs:**
   - Check for unusual activity daily
   - Identify popular phones and brands
   - Track user engagement

3. **Respond to Contact Requests Promptly:**
   - Reply within 24 hours
   - Provide helpful, detailed responses
   - Mark as "Replied" after sending

4. **Review User Activity:**
   - Identify and suspend spam accounts
   - Understand user preferences and behavior
   - Make data-driven decisions for content

5. **Regular Database Maintenance:**
   - Remove duplicate entries
   - Archive old data
   - Optimize database performance

---

**End of Appendix A: User Guide**
