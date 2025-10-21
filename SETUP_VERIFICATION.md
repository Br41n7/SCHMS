# Setup Verification Checklist

Use this checklist to verify your School Admission Portal installation is complete and working correctly.

## Pre-Installation Verification

- [ ] Python 3.8+ installed (`python --version`)
- [ ] pip installed (`pip --version`)
- [ ] Virtual environment tool available

## Installation Verification

### 1. Project Files
- [ ] All project files extracted/cloned
- [ ] Directory structure matches documentation
- [ ] `.env.example` file present
- [ ] `requirements.txt` file present
- [ ] `manage.py` file present

### 2. Virtual Environment
```bash
# Create and activate virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# Verify activation (should show venv path)
which python  # macOS/Linux
where python  # Windows
```
- [ ] Virtual environment created
- [ ] Virtual environment activated
- [ ] Python path points to venv

### 3. Dependencies Installation
```bash
pip install -r requirements.txt
```
- [ ] All packages installed without errors
- [ ] Django installed (`python -m django --version`)
- [ ] Wagtail installed (`wagtail --version`)

### 4. Environment Configuration
```bash
cp .env.example .env
```
- [ ] `.env` file created
- [ ] SECRET_KEY present (can use default for dev)
- [ ] DEBUG=True for development
- [ ] ALLOWED_HOSTS configured

### 5. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```
- [ ] Migrations created successfully
- [ ] All migrations applied
- [ ] `db.sqlite3` file created
- [ ] No error messages

### 6. Static Files
```bash
mkdir -p static media
```
- [ ] `static/` directory exists
- [ ] `media/` directory exists
- [ ] Directories have write permissions

### 7. Superuser Creation
```bash
python manage.py createsuperuser
```
- [ ] Superuser created successfully
- [ ] Username recorded
- [ ] Password recorded (securely)
- [ ] Email recorded

### 8. Development Server
```bash
python manage.py runserver
```
- [ ] Server starts without errors
- [ ] Accessible at http://localhost:8000
- [ ] No warning messages (except DEBUG=True)

## Functional Testing

### User Registration
1. Navigate to http://localhost:8000/accounts/register/
2. Fill in registration form:
   - [ ] First name field works
   - [ ] Middle name field works (optional)
   - [ ] Last name field works
   - [ ] Email field works
   - [ ] Password fields work
   - [ ] Password confirmation validates
3. Submit form
   - [ ] Form validates correctly
   - [ ] User created successfully
   - [ ] Redirected to dashboard
   - [ ] Success message displayed

### User Login
1. Navigate to http://localhost:8000/accounts/login/
2. Test login:
   - [ ] Can login with email
   - [ ] Can login with username
   - [ ] Wrong password shows error
   - [ ] Invalid credentials show error
   - [ ] Successful login redirects to dashboard

### Application Process

#### Step 1: Personal Information
1. Navigate to http://localhost:8000/admissions/personal-info/
2. Fill in form:
   - [ ] Date of birth field works
   - [ ] Gender dropdown works
   - [ ] Nationality field works
   - [ ] Address textarea works
   - [ ] City field works
   - [ ] State field works
   - [ ] Postal code field works
3. Submit form:
   - [ ] Validation works
   - [ ] Data saved successfully
   - [ ] Redirected to dashboard
   - [ ] Step marked as complete

#### Step 2: Program Information
1. Navigate to http://localhost:8000/admissions/program-info/
2. Fill in form:
   - [ ] Program choice dropdown works
   - [ ] Course of study field works
3. Submit form:
   - [ ] Validation works
   - [ ] Data saved successfully
   - [ ] Redirected to dashboard
   - [ ] Step marked as complete

#### Step 3: Document Upload
1. Navigate to http://localhost:8000/admissions/upload-documents/
2. Upload files:
   - [ ] Passport photo upload works
   - [ ] O'Level result upload works
   - [ ] Birth certificate upload works
   - [ ] Additional documents upload works (optional)
   - [ ] File size validation works (max 5MB)
   - [ ] File type validation works
3. Submit form:
   - [ ] Files uploaded successfully
   - [ ] Files stored in media directory
   - [ ] Redirected to dashboard
   - [ ] Step marked as complete

### Dashboard
1. Navigate to http://localhost:8000/admissions/dashboard/
2. Verify display:
   - [ ] Registration number shown
   - [ ] Status badge displayed
   - [ ] Progress bar shows 100%
   - [ ] All steps marked complete
   - [ ] Submit button enabled

### Application Submission
1. Click "Submit Application" button
2. Verify:
   - [ ] Confirmation page displayed
   - [ ] Application summary shown
   - [ ] Checkbox validation works
   - [ ] Submit button initially disabled
   - [ ] Submit button enables after checkbox
3. Submit application:
   - [ ] Application submitted successfully
   - [ ] Status changed to "Submitted"
   - [ ] Success message displayed
   - [ ] Cannot edit after submission

### Application Detail View
1. Navigate to http://localhost:8000/admissions/application-detail/
2. Verify display:
   - [ ] All personal information shown
   - [ ] All program information shown
   - [ ] All documents listed
   - [ ] Document links work
   - [ ] Status displayed correctly

### Admin Panel
1. Navigate to http://localhost:8000/admin/
2. Login with superuser credentials
3. Verify access:
   - [ ] Admin panel loads
   - [ ] Users section visible
   - [ ] Admission Applications section visible
   - [ ] Wagtail sections visible

### Application Management (Admin)
1. Click "Admission Applications"
2. Verify list view:
   - [ ] Applications listed
   - [ ] Registration numbers shown
   - [ ] Status badges displayed
   - [ ] Search works
   - [ ] Filters work
3. Click on an application
4. Verify detail view:
   - [ ] All information displayed
   - [ ] Documents accessible
   - [ ] Status can be changed
   - [ ] Review notes field works
5. Test approval:
   - [ ] Change status to "Approved"
   - [ ] Add review notes
   - [ ] Save changes
   - [ ] Status updated successfully
6. Test bulk actions:
   - [ ] Select multiple applications
   - [ ] Bulk approve works
   - [ ] Bulk reject works
   - [ ] Bulk mark under review works

### Profile Update
1. Navigate to http://localhost:8000/accounts/profile/update/
2. Update information:
   - [ ] Form pre-filled with current data
   - [ ] Can update first name
   - [ ] Can update middle name
   - [ ] Can update last name
   - [ ] Can update phone number
3. Submit form:
   - [ ] Changes saved successfully
   - [ ] Success message displayed
   - [ ] Redirected to dashboard

### Password Reset
1. Navigate to http://localhost:8000/accounts/password-reset/
2. Enter email:
   - [ ] Form accepts email
   - [ ] Validation works
3. Submit form:
   - [ ] Success message displayed
   - [ ] Email sent (check console in dev mode)
   - [ ] Reset link in email works

### Logout
1. Click logout in navigation
2. Verify:
   - [ ] User logged out successfully
   - [ ] Redirected to login page
   - [ ] Success message displayed
   - [ ] Cannot access protected pages

## Security Testing

### CSRF Protection
- [ ] All forms have CSRF token
- [ ] Forms fail without CSRF token
- [ ] CSRF token validates correctly

### File Upload Security
- [ ] Cannot upload files larger than 5MB
- [ ] Cannot upload disallowed file types
- [ ] Files stored securely in media directory
- [ ] File paths not predictable

### Authentication Security
- [ ] Cannot access dashboard without login
- [ ] Cannot access application pages without login
- [ ] Cannot access other users' applications
- [ ] Password reset requires valid token

### Form Validation
- [ ] Email validation works
- [ ] Password strength validation works
- [ ] Required fields enforced
- [ ] Date validation works
- [ ] File type validation works

## Performance Testing

### Page Load Times
- [ ] Homepage loads quickly
- [ ] Dashboard loads quickly
- [ ] Form pages load quickly
- [ ] Admin panel loads quickly

### Database Queries
- [ ] No N+1 query issues
- [ ] Queries optimized
- [ ] No slow queries

## Browser Compatibility

Test in multiple browsers:
- [ ] Chrome/Chromium
- [ ] Firefox
- [ ] Safari
- [ ] Edge

## Responsive Design

Test on different screen sizes:
- [ ] Desktop (1920x1080)
- [ ] Laptop (1366x768)
- [ ] Tablet (768x1024)
- [ ] Mobile (375x667)

## Documentation Verification

- [ ] README.md present and complete
- [ ] QUICK_START.md present
- [ ] DEPLOYMENT.md present
- [ ] FEATURES_EXTENSION_GUIDE.md present
- [ ] PROJECT_SUMMARY.md present
- [ ] All documentation accurate

## Production Readiness

### Environment Variables
- [ ] SECRET_KEY can be changed
- [ ] DEBUG can be set to False
- [ ] ALLOWED_HOSTS configurable
- [ ] DATABASE_URL configurable
- [ ] Email settings configurable

### Static Files
```bash
python manage.py collectstatic --noinput
```
- [ ] Static files collected successfully
- [ ] staticfiles/ directory created
- [ ] No errors during collection

### Database Migration
- [ ] All migrations up to date
- [ ] No pending migrations
- [ ] Migrations reversible

### Security Settings
- [ ] SECURE_SSL_REDIRECT configurable
- [ ] SESSION_COOKIE_SECURE configurable
- [ ] CSRF_COOKIE_SECURE configurable
- [ ] SECURE_HSTS_SECONDS configurable

## Deployment Verification

### Build Script
```bash
chmod +x build.sh
./build.sh
```
- [ ] Build script executable
- [ ] Dependencies install successfully
- [ ] Static files collected
- [ ] Migrations run successfully

### Render Configuration
- [ ] render.yaml present
- [ ] Configuration valid
- [ ] Environment variables defined

### Gunicorn
```bash
gunicorn school_portal.wsgi:application
```
- [ ] Gunicorn starts successfully
- [ ] Application accessible
- [ ] No errors in logs

## Common Issues Checklist

### Issue: ModuleNotFoundError
- [ ] Virtual environment activated
- [ ] Dependencies installed
- [ ] Correct Python version

### Issue: Database Locked
- [ ] Only one server instance running
- [ ] Database file not open elsewhere
- [ ] Proper file permissions

### Issue: Static Files Not Loading
- [ ] STATIC_URL configured
- [ ] STATIC_ROOT configured
- [ ] collectstatic run
- [ ] Whitenoise in MIDDLEWARE

### Issue: File Upload Fails
- [ ] media/ directory exists
- [ ] Directory has write permissions
- [ ] File size within limits
- [ ] File type allowed

### Issue: CSRF Verification Failed
- [ ] {% csrf_token %} in forms
- [ ] CSRF middleware enabled
- [ ] Cookies enabled in browser

## Final Verification

- [ ] All tests passed
- [ ] No errors in console
- [ ] No warnings (except DEBUG=True)
- [ ] Application fully functional
- [ ] Ready for development/deployment

## Sign-Off

**Verified by:** _br41n7__________________

**Date:** ______oct___11__________

**Environment:** [ ] Development [ ] Staging [ ] Production

**Notes:**
_____________________________________________
_____________________________________________
_____________________________________________

---

## Next Steps After Verification

1. **For Development:**
   - Start building features
   - Follow FEATURES_EXTENSION_GUIDE.md
   - Write tests for new features

2. **For Production:**
   - Follow DEPLOYMENT.md
   - Set up PostgreSQL
   - Configure environment variables
   - Set up email service
   - Deploy to chosen platform

3. **For Team Handoff:**
   - Share documentation
   - Provide access credentials
   - Schedule knowledge transfer
   - Set up monitoring

## Support

If any verification step fails:
1. Check the error message
2. Review relevant documentation
3. Check Django/Wagtail documentation
4. Review troubleshooting section in README.md
5. Create an issue with details

---

**Congratulations!** If all checks pass, your School Admission Portal is ready! 🎉