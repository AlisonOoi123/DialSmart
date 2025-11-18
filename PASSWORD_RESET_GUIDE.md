# Password Reset & Management System

Complete guide for password management features in DialSmart.

---

## ✅ Features Implemented

### 1. **Forgot Password with Email Verification**
- Verifies email is registered before sending reset link
- Redirects unregistered emails to registration page
- Sends secure password reset email with 1-hour expiry token
- Token-based password reset with validation

### 2. **Password Change in Profile**
- Both user and admin profiles have password change functionality
- Requires current password verification
- Validates new password strength
- Located at `/profile` for users and admins

### 3. **Secure Password Reset Flow**
- One-time use tokens
- 1-hour token expiry for security
- Password strength validation on reset
- Clear user feedback at each step

---

## 🔄 User Flow

### Flow 1: User Forgot Password (Email Registered)

```
1. User clicks "Forgot Password" on login page
   ↓
2. User enters email address
   ↓
3. System checks if email is registered
   ↓
4. Email IS registered:
   - System sends password reset email
   - Email contains secure reset link (expires in 1 hour)
   - User redirected to login with success message
   ↓
5. User checks email and clicks reset link
   ↓
6. User lands on reset password page
   ↓
7. User enters new password (with strength validation)
   ↓
8. Password reset successful
   ↓
9. User redirected to login page
```

### Flow 2: User Forgot Password (Email NOT Registered)

```
1. User clicks "Forgot Password" on login page
   ↓
2. User enters email address
   ↓
3. System checks if email is registered
   ↓
4. Email NOT registered:
   - Flash message: "This email is not registered. Please register for an account first."
   - User redirected to registration page
   ↓
5. User registers new account
```

### Flow 3: Change Password in Profile

```
1. User/Admin logs in
   ↓
2. User/Admin navigates to profile page
   ↓
3. In password section:
   - Enter current password
   - Enter new password (must meet strength requirements)
   - Confirm new password
   ↓
4. Submit form
   ↓
5. System validates:
   - Current password is correct
   - New password meets requirements
   - Passwords match
   ↓
6. Password updated successfully
```

---

## 🔒 Security Features

### Password Strength Requirements

All passwords (including reset passwords) must meet:
- ✅ Minimum 8 characters
- ✅ At least one uppercase letter (A-Z)
- ✅ At least one lowercase letter (a-z)
- ✅ At least one number (0-9)
- ✅ At least one special character (!@#$%^&*()_+-=[]{}|;:,.<>?)

### Token Security

- **Token Generation:** Cryptographically secure random tokens (`secrets.token_urlsafe(32)`)
- **Token Expiry:** 1 hour for password reset, 24 hours for email verification
- **One-Time Use:** Tokens are deleted after successful use
- **Unique Tokens:** Each token is unique and cannot be reused

### Database Security

New columns added to `users` table:
```sql
password_reset_token VARCHAR(100) UNIQUE
password_reset_sent_at DATETIME
```

---

## 🛣️ Routes

### Authentication Routes

| Route | Method | Description |
|-------|--------|-------------|
| `/auth/forgot-password` | GET, POST | Request password reset |
| `/auth/reset-password/<token>` | GET, POST | Reset password with token |
| `/profile` | GET, POST | Change password (logged in users) |

### Flow Diagram

```
/auth/login
    │
    ├─→ "Forgot Password?" → /auth/forgot-password
    │                            │
    │                            ├─→ Email registered?
    │                            │   ├─→ YES: Send reset email
    │                            │   └─→ NO: Redirect to /auth/register
    │                            │
    │                            └─→ User clicks email link
    │                                    │
    │                                    └─→ /auth/reset-password/<token>
    │                                            │
    │                                            └─→ New password → Login
    │
    └─→ Login success → /profile (change password anytime)
```

---

## 📧 Email Templates

### Password Reset Email

**Subject:** DialSmart - Password Reset Request

**Contents:**
- Personalized greeting with user's name
- Clear "Reset Password" button
- Plain text reset link (for email clients that don't support HTML)
- Security notice about 1-hour expiry
- Warning if user didn't request the reset

**Example:**
```
Hello John Doe,

We received a request to reset your password. Click the button below:

[Reset Password Button]

Or copy this link: https://dialsmart.my/auth/reset-password/abc123...

This link will expire in 1 hour.
If you didn't request this, please ignore this email.
```

---

## 🧪 Testing

### Test Case 1: Forgot Password (Registered Email)

```bash
# 1. Visit login page
http://localhost:5000/auth/login

# 2. Click "Forgot Password"
http://localhost:5000/auth/forgot-password

# 3. Enter registered email
Email: user@dialsmart.my

# 4. Check for success message
"Password reset instructions have been sent to your email"

# 5. Check email inbox for reset link
# 6. Click reset link
# 7. Enter new password (must meet requirements)
# 8. Verify redirect to login
# 9. Login with new password
```

### Test Case 2: Forgot Password (Unregistered Email)

```bash
# 1. Visit forgot password
http://localhost:5000/auth/forgot-password

# 2. Enter unregistered email
Email: notregistered@example.com

# 3. Check for warning message
"This email is not registered. Please register for an account first."

# 4. Verify redirect to registration page
http://localhost:5000/auth/register
```

### Test Case 3: Change Password in Profile

```bash
# 1. Login as user
http://localhost:5000/auth/login

# 2. Navigate to profile
http://localhost:5000/profile

# 3. Enter:
Current Password: TestUser123!
New Password: NewSecure456@
Confirm Password: NewSecure456@

# 4. Submit and verify success message
# 5. Logout and login with new password
```

### Test Case 4: Expired Reset Token

```bash
# 1. Request password reset
# 2. Wait more than 1 hour
# 3. Click reset link
# 4. Verify error message:
"Password reset link has expired. Please request a new one."

# 5. Verify redirect to forgot password page
```

### Test Case 5: Invalid Password (Too Weak)

```bash
# Try these passwords (should all fail):
- password123      # No uppercase, no special char
- Password         # No number, no special char
- PASSWORD123!     # No lowercase
- Pass12!          # Too short

# This should succeed:
- SecurePass123!   # All requirements met
```

---

## 📊 Database Schema

### Users Table - New Columns

```sql
ALTER TABLE users ADD COLUMN password_reset_token VARCHAR(100);
ALTER TABLE users ADD COLUMN password_reset_sent_at DATETIME;
```

### Migration Required

Run the migration script to add these columns:
```bash
python migrate_database.py
```

**Expected Output:**
```
======================================================================
DialSmart Database Migration
Adding Email Verification Columns
======================================================================

Adding column: password_reset_token
Adding column: password_reset_sent_at

======================================================================
✅ Database migration completed successfully!
======================================================================
```

---

## 💻 Code Examples

### Example 1: Forgot Password Implementation

```python
@bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()

        if not user:
            # Email not registered
            flash('This email is not registered. Please register first.', 'warning')
            return redirect(url_for('auth.register'))

        # Send reset email
        success, message = send_password_reset_email(user)
        if success:
            db.session.commit()
            flash('Reset instructions sent to your email.', 'success')

        return redirect(url_for('auth.login'))

    return render_template('auth/forgot_password.html')
```

### Example 2: Reset Password with Token

```python
@bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = User.query.filter_by(password_reset_token=token).first()

    if not user or is_token_expired(user.password_reset_sent_at, 3600):
        flash('Invalid or expired reset link.', 'danger')
        return redirect(url_for('auth.forgot_password'))

    if request.method == 'POST':
        new_password = request.form.get('new_password')

        # Validate password strength
        is_valid, error = validate_password(new_password)
        if not is_valid:
            flash(error, 'danger')
            return render_template('auth/reset_password.html', token=token)

        # Reset password
        user.set_password(new_password)
        user.password_reset_token = None
        db.session.commit()

        flash('Password reset successful!', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/reset_password.html', token=token)
```

### Example 3: Change Password in Profile

```python
# In app/routes/user.py
@bp.route('/profile', methods=['POST'])
@login_required
def profile():
    new_password = request.form.get('new_password')

    if new_password:
        current_password = request.form.get('current_password')

        if not current_user.check_password(current_password):
            flash('Current password is incorrect.', 'danger')
            return render_template('user/profile.html')

        # Validate new password
        is_valid, error = validate_password(new_password)
        if not is_valid:
            flash(error, 'danger')
            return render_template('user/profile.html')

        current_user.set_password(new_password)
        db.session.commit()
        flash('Password updated successfully.', 'success')
```

---

## 🚨 Error Handling

### Common Errors & Solutions

**Error:** "This email is not registered"
- **Cause:** User entered email that doesn't exist in database
- **Solution:** Redirect to registration page
- **User Action:** Register new account

**Error:** "Invalid or expired reset link"
- **Cause:** Token expired (> 1 hour) or invalid
- **Solution:** Request new password reset
- **User Action:** Go to forgot password page again

**Error:** "Current password is incorrect"
- **Cause:** User entered wrong current password when changing
- **Solution:** Re-enter correct current password
- **User Action:** Verify current password is correct

**Error:** "Password must contain at least one uppercase letter"
- **Cause:** New password doesn't meet strength requirements
- **Solution:** Update password to meet all requirements
- **User Action:** Use stronger password

---

## 📱 User Interface Notes

### Forgot Password Page

**Required Fields:**
- Email input field
- Submit button
- Link back to login
- Link to registration

**Sample HTML:**
```html
<form method="POST">
    <h2>Forgot Password</h2>
    <p>Enter your email address and we'll send you instructions to reset your password.</p>

    <input type="email" name="email" required placeholder="your@email.com">
    <button type="submit">Send Reset Instructions</button>

    <a href="/auth/login">Back to Login</a>
    <a href="/auth/register">Don't have an account? Register</a>
</form>
```

### Reset Password Page

**Required Fields:**
- New password input
- Confirm password input
- Submit button
- Password requirements display

**Sample HTML:**
```html
<form method="POST">
    <h2>Reset Your Password</h2>

    <div class="password-requirements">
        <p>Password must contain:</p>
        <ul>
            <li>At least 8 characters</li>
            <li>One uppercase letter</li>
            <li>One lowercase letter</li>
            <li>One number</li>
            <li>One special character</li>
        </ul>
    </div>

    <input type="password" name="new_password" required placeholder="New Password">
    <input type="password" name="confirm_password" required placeholder="Confirm Password">
    <button type="submit">Reset Password</button>
</form>
```

---

## 🎯 Summary

**Features:**
- ✅ Forgot password with email verification
- ✅ Unregistered email detection and redirect
- ✅ Password reset with secure tokens
- ✅ Password change in user/admin profiles
- ✅ Strong password validation
- ✅ Email notifications
- ✅ Token expiry (1 hour)
- ✅ One-time use tokens

**Security:**
- ✅ Cryptographically secure tokens
- ✅ Password strength enforcement
- ✅ Token expiry
- ✅ Current password verification for changes
- ✅ No password storage in plain text

**User Experience:**
- ✅ Clear error messages
- ✅ Helpful redirects
- ✅ Professional email templates
- ✅ Password requirements displayed
- ✅ Success confirmations

---

**Modified by:** Claude AI Assistant
**Date:** 2025-11-18
**Version:** 1.0
