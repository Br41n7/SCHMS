# Quick Start Guide

Get the School Admission Portal up and running in 5 minutes!

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation Steps

### 1. Clone or Download the Project

```bash
# If using git
git clone <repository-url>
cd school_portal

# Or extract the downloaded ZIP file and navigate to the directory
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

```bash
# Copy the example file
cp .env.example .env

# The default settings work for local development
# No need to change anything for testing
```

### 5. Run Migrations

```bash
python manage.py migrate
```

### 6. Create Admin User

```bash
python manage.py createsuperuser
```

Follow the prompts to create your admin account.

### 7. Start the Server

```bash
python manage.py runserver
```

## Access the Application

- **Main Site**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin/
- **Wagtail CMS**: http://localhost:8000/cms/

## Test the System

### As an Applicant:

1. Go to http://localhost:8000/accounts/register/
2. Create a new account
3. Complete the 3-step application process:
   - Personal Information
   - Program Selection
   - Document Upload
4. Submit your application

### As an Administrator:

1. Go to http://localhost:8000/admin/
2. Log in with your superuser credentials
3. Navigate to "Admission Applications"
4. Review and approve/reject applications

## Default Configuration

The system comes with sensible defaults for development:

- **Database**: SQLite (db.sqlite3)
- **Debug Mode**: Enabled
- **Email**: Console backend (emails printed to terminal)
- **Static Files**: Served by Django development server
- **Media Files**: Stored in `media/` directory

## Next Steps

1. **Customize Settings**: Edit `.env` file for your needs
2. **Add Content**: Use Wagtail CMS to add pages
3. **Configure Email**: Set up SMTP for password reset
4. **Deploy**: Follow DEPLOYMENT.md for production setup

## Common Commands

```bash
# Create migrations after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files (for production)
python manage.py collectstatic

# Run tests
python manage.py test

# Start development server
python manage.py runserver

# Access Django shell
python manage.py shell
```

## Troubleshooting

### Port Already in Use

```bash
# Use a different port
python manage.py runserver 8080
```

### Database Locked Error

```bash
# Stop the server and restart
# Make sure no other process is using the database
```

### Static Files Not Loading

```bash
# Collect static files
python manage.py collectstatic --noinput
```

### Import Errors

```bash
# Make sure virtual environment is activated
# Reinstall dependencies
pip install -r requirements.txt
```

## File Structure Overview

```
school_portal/
├── accounts/              # User authentication
├── admissions/           # Application management
├── cms/                  # Wagtail CMS
├── school_portal/        # Project settings
├── templates/            # HTML templates
├── static/               # Static files (CSS, JS)
├── media/                # User uploads
├── manage.py            # Django management script
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables template
└── README.md           # Full documentation
```

## Getting Help

- Check README.md for detailed documentation
- Review DEPLOYMENT.md for production setup
- See FEATURES_EXTENSION_GUIDE.md for adding features
- Create an issue on GitHub for bugs

## What's Next?

Now that you have the system running:

1. **Explore the Admin Panel**: See how applications are managed
2. **Test the Application Flow**: Go through the entire process
3. **Customize the UI**: Modify templates in `templates/`
4. **Add Features**: Follow FEATURES_EXTENSION_GUIDE.md
5. **Deploy to Production**: Use DEPLOYMENT.md guide

## Production Deployment

When ready to deploy:

1. Set `DEBUG=False` in `.env`
2. Generate a secure `SECRET_KEY`
3. Set up PostgreSQL database
4. Configure email settings
5. Follow DEPLOYMENT.md for platform-specific instructions

## Support

For questions or issues:
- Check the documentation files
- Review Django documentation: https://docs.djangoproject.com/
- Check Wagtail documentation: https://docs.wagtail.org/

---

**Congratulations!** 🎉 Your School Admission Portal is now running!