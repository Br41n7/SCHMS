# School Admission Portal

A production-ready school admission portal built with Django, Bootstrap 5, and Wagtail CMS. This system provides a complete solution for managing student applications with a secure, user-friendly interface.

## Features

### User Authentication System
- Custom user registration with email verification
- Secure password hashing and validation
- Login with email or username
- Password reset functionality
- Profile management

### Admission Application System
- Unique registration number generation
- Step-by-step application process:
  1. Personal Information
  2. Program Selection
  3. Document Upload
- File upload with validation (passport photo, O'Level results, birth certificate)
- Application status tracking (Draft, Submitted, Under Review, Approved, Rejected)
- Progress indicator showing completion percentage

### Admin Features
- Django admin interface for application management
- Bulk approval/rejection actions
- Application review workflow
- Document viewing and verification
- Status tracking and notes

### Extensibility
- Wagtail CMS integration for content management
- Placeholder models for future features:
  - Timetable management
  - Online learning platform
  - Additional custom pages

## Technology Stack

- **Backend**: Django 4.2.9
- **CMS**: Wagtail 5.2.2
- **Frontend**: Bootstrap 5.3.0
- **Database**: SQLite (default) / PostgreSQL (production)
- **File Storage**: Local filesystem (can be extended to S3)
- **WSGI Server**: Gunicorn

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Setup Instructions

1. **Clone the repository**
```bash
git clone https://github.com/Br41n7/SCHMS
cd SCHMS
```

2. **Create and activate virtual environment**
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and update the following:
# - SECRET_KEY (generate a new one for production)
# - DEBUG (set to False in production)
# - ALLOWED_HOSTS (add your domain)
# - DATABASE_URL (if using PostgreSQL)
# - Email settings (for password reset)
```

5. **Run migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Create a superuser**
```bash
python manage.py createsuperuser
```

7. **Create static files directory**
```bash
python manage.py collectstatic --noinput
```

8. **Run the development server**
```bash
python manage.py runserver
```

Visit `http://localhost:8000` to access the application.

## Configuration

### Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (SQLite by default)
DATABASE_URL=sqlite:///db.sqlite3

# For PostgreSQL (production)
# DATABASE_URL=postgresql://username:password@localhost:5432/dbname

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-email-password

# Security Settings (production)
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
```

### Database Configuration

#### SQLite (Development)
The default configuration uses SQLite. No additional setup required.

#### PostgreSQL (Production)
1. Install PostgreSQL
2. Create a database:
```sql
CREATE DATABASE school_portal;
CREATE USER portal_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE school_portal TO portal_user;
```
3. Update `DATABASE_URL` in `.env`:
```env
DATABASE_URL=postgresql://portal_user:your_password@localhost:5432/school_portal
```

## Deployment

### Deploying to Render

1. **Create a new Web Service on Render**
   - Connect your GitHub repository
   - Select "Python" as the environment

2. **Configure Build Settings**
   - Build Command: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
   - Start Command: `gunicorn school_portal.wsgi:application`

3. **Set Environment Variables**
   Add the following environment variables in Render dashboard:
   ```
   SECRET_KEY=<generate-a-secure-key>
   DEBUG=False
   ALLOWED_HOSTS=<your-render-url>.onrender.com
   DATABASE_URL=<your-postgresql-url>
   SECURE_SSL_REDIRECT=True
   SESSION_COOKIE_SECURE=True
   CSRF_COOKIE_SECURE=True
   ```

4. **Add PostgreSQL Database**
   - Create a PostgreSQL database in Render
   - Copy the internal database URL
   - Set it as `DATABASE_URL` environment variable

5. **Deploy**
   - Push your code to GitHub
   - Render will automatically build and deploy

### Deploying to Other Platforms

The application is configured to work with any platform that supports Python/Django:
- Heroku
- Railway
- DigitalOcean App Platform
- AWS Elastic Beanstalk
- Google Cloud Run

Key requirements:
- Python 3.8+
- PostgreSQL database
- Environment variables configured
- Static files served via Whitenoise

## Usage

### For Applicants

1. **Register an Account**
   - Navigate to the registration page
   - Fill in your details (first name, last name, email, password)
   - Submit the form

2. **Complete Application**
   - Log in to your dashboard
   - Complete the three-step application process:
     - Step 1: Personal Information
     - Step 2: Program Selection
     - Step 3: Document Upload
   - Review your application
   - Submit for review

3. **Track Status**
   - View application status on dashboard
   - Receive notifications when status changes
   - View admin review notes (if any)

### For Administrators

1. **Access Admin Panel**
   - Navigate to `/admin/`
   - Log in with superuser credentials

2. **Review Applications**
   - View all submitted applications
   - Filter by status, program, date
   - Search by registration number or applicant name

3. **Approve/Reject Applications**
   - Open an application
   - Review all information and documents
   - Add review notes
   - Change status to "Approved" or "Rejected"
   - Use bulk actions for multiple applications

## Project Structure

```
school_portal/
├── accounts/              # User authentication app
│   ├── models.py         # Custom User model
│   ├── forms.py          # Registration and login forms
│   ├── views.py          # Authentication views
│   └── urls.py           # URL patterns
├── admissions/           # Admission application app
│   ├── models.py         # Application model
│   ├── forms.py          # Application forms
│   ├── views.py          # Application views
│   ├── admin.py          # Admin configuration
│   └── urls.py           # URL patterns
├── cms/                  # Wagtail CMS app
│   └── models.py         # CMS page models
├── school_portal/        # Project settings
│   ├── settings.py       # Django settings
│   ├── urls.py           # Root URL configuration
│   └── wsgi.py           # WSGI configuration
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── accounts/         # Authentication templates
│   └── admissions/       # Application templates
├── static/               # Static files (CSS, JS, images)
├── media/                # User uploads
├── requirements.txt      # Python dependencies
├── .env.example          # Example environment variables
├── .gitignore           # Git ignore rules
└── manage.py            # Django management script
```

## Extending the System

### Adding New Features

The system is designed for easy extension. Here are some examples:

#### 1. Adding a Timetable Feature

```python
# In admissions/models.py
class Timetable(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.CharField(max_length=200)
    day_of_week = models.CharField(max_length=20)
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.CharField(max_length=100)
```

#### 2. Adding Online Learning

```python
# In admissions/models.py
class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    instructor = models.ForeignKey(User, on_delete=models.CASCADE)
    
class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
```

#### 3. Adding Payment Integration

```python
# In admissions/models.py
class Payment(models.Model):
    application = models.ForeignKey(AdmissionApplication, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=100)
    status = models.CharField(max_length=20)
    paid_at = models.DateTimeField(null=True, blank=True)
```

### Customizing the UI

The system uses Bootstrap 5 for styling. To customize:

1. **Override Bootstrap variables**
   - Create `static/css/custom.css`
   - Add custom styles
   - Include in `base.html`

2. **Modify templates**
   - Templates are in `templates/` directory
   - Extend `base.html` for consistent layout
   - Use Bootstrap classes for styling

## Security Features

- CSRF protection on all forms
- Secure password hashing (Django's built-in)
- File upload validation (size and type)
- SQL injection protection (Django ORM)
- XSS protection (Django templates)
- Secure session management
- HTTPS enforcement in production
- Environment-based configuration

## Testing

Run tests with:
```bash
python manage.py test
```

Create tests in `tests.py` files within each app.

## Troubleshooting

### Common Issues

1. **Static files not loading**
   ```bash
   python manage.py collectstatic --noinput
   ```

2. **Database errors**
   ```bash
   python manage.py migrate
   ```

3. **Permission errors on file uploads**
   - Ensure `media/` directory exists
   - Check file permissions

4. **Email not sending**
   - Verify email settings in `.env`
   - Check EMAIL_BACKEND configuration

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write tests
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions:
- Create an issue on GitHub
- Contact the development team
- Check the documentation

## Changelog

### Version 1.0.0 (Initial Release)
- User registration and authentication
- Step-by-step application process
- Document upload functionality
- Admin approval workflow
- Dashboard with progress tracking
- Wagtail CMS integration
- Production-ready configuration

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📝 License

MIT License - see LICENSE file

## 🆘 Support

- **Documentation**: See this README
- **Issues**: GitHub Issues
- **Email**: iyanuolalegan1@.com

## 🎉 Acknowledgments

- Django framework
- Bootstrap 5
- Paystack
- All contributors

## 📞 Contact

For questions or support:
- Email: iyanuolalegan1@gmail.com
- GitHub: @br41n7
- WA: https://wa.me/+2349118263860

---

**Built with ❤️ using Django**

**Status**: ✅ Production Ready
