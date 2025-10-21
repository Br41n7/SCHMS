# Deployment Guide

This guide provides detailed instructions for deploying the School Admission Portal to production environments.

## Pre-Deployment Checklist

Before deploying to production, ensure you have:

- [ ] Set `DEBUG=False` in environment variables
- [ ] Generated a strong `SECRET_KEY`
- [ ] Configured `ALLOWED_HOSTS` with your domain
- [ ] Set up a PostgreSQL database
- [ ] Configured email settings for password reset
- [ ] Enabled security settings (SSL, secure cookies)
- [ ] Collected static files
- [ ] Run all migrations
- [ ] Created a superuser account
- [ ] Tested the application locally

## Deployment to Render

### Step 1: Prepare Your Repository

1. Ensure all code is committed to Git
2. Push to GitHub/GitLab/Bitbucket

### Step 2: Create a Render Account

1. Go to [render.com](https://render.com)
2. Sign up or log in
3. Connect your Git repository

### Step 3: Create a PostgreSQL Database

1. Click "New +" → "PostgreSQL"
2. Configure:
   - Name: `school-portal-db`
   - Database: `school_portal`
   - User: (auto-generated)
   - Region: Choose closest to your users
   - Plan: Free or paid based on needs
3. Click "Create Database"
4. Copy the "Internal Database URL" (starts with `postgresql://`)

### Step 4: Create a Web Service

1. Click "New +" → "Web Service"
2. Connect your repository
3. Configure:
   - Name: `school-admission-portal`
   - Environment: `Python 3`
   - Region: Same as database
   - Branch: `main` or `master`
   - Build Command:
     ```bash
     pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
     ```
   - Start Command:
     ```bash
     gunicorn school_portal.wsgi:application
     ```
   - Plan: Free or paid based on needs

### Step 5: Configure Environment Variables

Add these environment variables in Render dashboard:

```
SECRET_KEY=<generate-using-python-secrets>
DEBUG=False
ALLOWED_HOSTS=<your-app-name>.onrender.com
DATABASE_URL=<paste-internal-database-url>
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
```

To generate a secure SECRET_KEY:
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Step 6: Deploy

1. Click "Create Web Service"
2. Wait for the build to complete
3. Your app will be available at `https://<your-app-name>.onrender.com`

### Step 7: Create Superuser

1. Go to Render dashboard
2. Click on your web service
3. Click "Shell" tab
4. Run:
   ```bash
   python manage.py createsuperuser
   ```
5. Follow the prompts

### Step 8: Test Your Deployment

1. Visit your app URL
2. Test registration
3. Test login
4. Test application submission
5. Access admin panel at `/admin/`

## Deployment to Heroku

### Step 1: Install Heroku CLI

```bash
# macOS
brew tap heroku/brew && brew install heroku

# Windows
# Download from https://devcenter.heroku.com/articles/heroku-cli

# Linux
curl https://cli-assets.heroku.com/install.sh | sh
```

### Step 2: Login to Heroku

```bash
heroku login
```

### Step 3: Create Heroku App

```bash
heroku create school-admission-portal
```

### Step 4: Add PostgreSQL

```bash
heroku addons:create heroku-postgresql:mini
```

### Step 5: Set Environment Variables

```bash
heroku config:set SECRET_KEY="<your-secret-key>"
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS="<your-app-name>.herokuapp.com"
heroku config:set SECURE_SSL_REDIRECT=True
heroku config:set SESSION_COOKIE_SECURE=True
heroku config:set CSRF_COOKIE_SECURE=True
```

### Step 6: Create Procfile

Create a file named `Procfile` in the project root:

```
web: gunicorn school_portal.wsgi:application --log-file -
release: python manage.py migrate
```

### Step 7: Deploy

```bash
git add .
git commit -m "Prepare for Heroku deployment"
git push heroku main
```

### Step 8: Create Superuser

```bash
heroku run python manage.py createsuperuser
```

### Step 9: Open Your App

```bash
heroku open
```

## Deployment to DigitalOcean App Platform

### Step 1: Create App

1. Go to DigitalOcean App Platform
2. Click "Create App"
3. Connect your GitHub repository

### Step 2: Configure App

1. **Build Command:**
   ```bash
   pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
   ```

2. **Run Command:**
   ```bash
   gunicorn school_portal.wsgi:application
   ```

3. **Environment Variables:**
   Add all required environment variables

### Step 3: Add Database

1. Add a PostgreSQL database component
2. Copy the connection string
3. Set as `DATABASE_URL` environment variable

### Step 4: Deploy

Click "Deploy" and wait for the build to complete.

## Deployment to AWS Elastic Beanstalk

### Step 1: Install EB CLI

```bash
pip install awsebcli
```

### Step 2: Initialize EB

```bash
eb init -p python-3.11 school-admission-portal
```

### Step 3: Create Environment

```bash
eb create school-portal-env
```

### Step 4: Configure Environment Variables

```bash
eb setenv SECRET_KEY="<your-secret-key>" DEBUG=False ALLOWED_HOSTS="<your-eb-url>"
```

### Step 5: Deploy

```bash
eb deploy
```

### Step 6: Open App

```bash
eb open
```

## Post-Deployment Tasks

### 1. Set Up Email

Configure email settings for password reset:

```python
# In production .env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### 2. Configure Custom Domain

#### Render
1. Go to Settings → Custom Domains
2. Add your domain
3. Update DNS records as instructed

#### Heroku
```bash
heroku domains:add www.yourdomain.com
```

### 3. Set Up SSL Certificate

Most platforms provide free SSL certificates automatically. Ensure:
- `SECURE_SSL_REDIRECT=True`
- `SESSION_COOKIE_SECURE=True`
- `CSRF_COOKIE_SECURE=True`

### 4. Configure Media File Storage

For production, consider using cloud storage:

#### AWS S3

1. Install boto3:
```bash
pip install boto3 django-storages
```

2. Update settings.py:
```python
# Add to INSTALLED_APPS
INSTALLED_APPS = [
    # ...
    'storages',
]

# S3 Configuration
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME', default='us-east-1')
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
```

### 5. Set Up Monitoring

#### Sentry (Error Tracking)

1. Install Sentry:
```bash
pip install sentry-sdk
```

2. Configure in settings.py:
```python
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn=config('SENTRY_DSN'),
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=True
)
```

### 6. Set Up Backups

#### Database Backups

**Render:**
- Automatic backups included in paid plans
- Manual backups via dashboard

**Heroku:**
```bash
heroku pg:backups:schedule DATABASE_URL --at '02:00 America/Los_Angeles'
```

**DigitalOcean:**
- Automatic daily backups available
- Configure in database settings

### 7. Performance Optimization

1. **Enable Caching:**
```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': config('REDIS_URL'),
    }
}
```

2. **Database Connection Pooling:**
```python
# settings.py
DATABASES['default']['CONN_MAX_AGE'] = 600
```

3. **Compress Static Files:**
Whitenoise already handles this automatically.

## Monitoring and Maintenance

### Health Checks

Create a health check endpoint:

```python
# school_portal/urls.py
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({'status': 'healthy'})

urlpatterns = [
    # ...
    path('health/', health_check),
]
```

### Log Monitoring

Access logs:

**Render:**
```bash
# Via dashboard or CLI
render logs -s <service-name>
```

**Heroku:**
```bash
heroku logs --tail
```

### Database Maintenance

Run periodic maintenance:

```bash
# Optimize database
python manage.py dbshell
VACUUM ANALYZE;

# Clear old sessions
python manage.py clearsessions
```

## Troubleshooting

### Static Files Not Loading

1. Ensure `STATIC_ROOT` is set
2. Run `collectstatic`:
```bash
python manage.py collectstatic --noinput
```
3. Verify Whitenoise is in `MIDDLEWARE`

### Database Connection Errors

1. Check `DATABASE_URL` format
2. Ensure database is accessible
3. Verify credentials

### 500 Internal Server Error

1. Check logs for details
2. Ensure `DEBUG=False`
3. Verify all environment variables are set
4. Check database migrations

### File Upload Issues

1. Verify `MEDIA_ROOT` and `MEDIA_URL` settings
2. Check file permissions
3. Consider using cloud storage for production

## Security Best Practices

1. **Keep Dependencies Updated:**
```bash
pip list --outdated
pip install --upgrade <package>
```

2. **Regular Security Audits:**
```bash
pip install safety
safety check
```

3. **Monitor Access Logs:**
Review logs regularly for suspicious activity

4. **Implement Rate Limiting:**
Consider using Django Ratelimit or similar

5. **Regular Backups:**
Automate database and media file backups

6. **Use Environment Variables:**
Never commit secrets to version control

## Scaling Considerations

### Horizontal Scaling

1. Use load balancers
2. Deploy multiple instances
3. Use session storage (Redis/Memcached)

### Database Scaling

1. Use connection pooling
2. Implement read replicas
3. Optimize queries with indexes

### Media File Scaling

1. Use CDN for static files
2. Use cloud storage (S3, GCS)
3. Implement image optimization

## Support and Resources

- Django Documentation: https://docs.djangoproject.com/
- Render Documentation: https://render.com/docs
- Heroku Documentation: https://devcenter.heroku.com/
- Wagtail Documentation: https://docs.wagtail.org/

## Conclusion

Your School Admission Portal is now deployed and ready for production use. Remember to:
- Monitor logs regularly
- Keep dependencies updated
- Perform regular backups
- Test thoroughly before major updates
- Document any custom configurations