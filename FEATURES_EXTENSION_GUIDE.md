# Features Extension Guide

This guide provides detailed instructions for extending the School Admission Portal with additional features.

## Table of Contents

1. [Adding a Timetable System](#adding-a-timetable-system)
2. [Adding Online Learning Platform](#adding-online-learning-platform)
3. [Adding Payment Integration](#adding-payment-integration)
4. [Adding Notification System](#adding-notification-system)
5. [Adding Student Portal](#adding-student-portal)
6. [Adding Exam Management](#adding-exam-management)

---

## Adding a Timetable System

### Step 1: Create Models

Add to `admissions/models.py`:

```python
class Timetable(models.Model):
    """
    Timetable for approved students.
    """
    DAYS_OF_WEEK = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='timetables'
    )
    course_name = models.CharField(max_length=200)
    course_code = models.CharField(max_length=50)
    day_of_week = models.CharField(max_length=20, choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.CharField(max_length=100)
    instructor = models.CharField(max_length=200)
    semester = models.CharField(max_length=50)
    academic_year = models.CharField(max_length=20)
    
    class Meta:
        ordering = ['day_of_week', 'start_time']
        verbose_name = "Timetable Entry"
        verbose_name_plural = "Timetable Entries"
    
    def __str__(self):
        return f"{self.course_name} - {self.day_of_week} {self.start_time}"
```

### Step 2: Create Views

Add to `admissions/views.py`:

```python
from django.views.generic import ListView

class TimetableView(LoginRequiredMixin, ListView):
    """
    Display student's timetable.
    """
    model = Timetable
    template_name = 'admissions/timetable.html'
    context_object_name = 'timetable_entries'
    
    def get_queryset(self):
        return Timetable.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Organize by day of week
        timetable_by_day = {}
        for entry in context['timetable_entries']:
            day = entry.get_day_of_week_display()
            if day not in timetable_by_day:
                timetable_by_day[day] = []
            timetable_by_day[day].append(entry)
        
        context['timetable_by_day'] = timetable_by_day
        context['title'] = 'My Timetable'
        return context
```

### Step 3: Add URL Pattern

Add to `admissions/urls.py`:

```python
path('timetable/', TimetableView.as_view(), name='timetable'),
```

### Step 4: Create Template

Create `templates/admissions/timetable.html`:

```html
{% extends 'base.html' %}

{% block content %}
<div class="container">
    <h2><i class="bi bi-calendar-week me-2"></i>My Timetable</h2>
    
    {% for day, entries in timetable_by_day.items %}
    <div class="card mb-3">
        <div class="card-header">
            <h5>{{ day }}</h5>
        </div>
        <div class="card-body">
            <div class="table-responsive">
                <table class="table">
                    <thead>
                        <tr>
                            <th>Time</th>
                            <th>Course</th>
                            <th>Room</th>
                            <th>Instructor</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for entry in entries %}
                        <tr>
                            <td>{{ entry.start_time|time:"g:i A" }} - {{ entry.end_time|time:"g:i A" }}</td>
                            <td>{{ entry.course_name }} ({{ entry.course_code }})</td>
                            <td>{{ entry.room }}</td>
                            <td>{{ entry.instructor }}</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
    {% endfor %}
</div>
{% endblock %}
```

### Step 5: Register in Admin

Add to `admissions/admin.py`:

```python
@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    list_display = ['course_name', 'user', 'day_of_week', 'start_time', 'room']
    list_filter = ['day_of_week', 'semester', 'academic_year']
    search_fields = ['course_name', 'course_code', 'user__email']
```

---

## Adding Online Learning Platform

### Step 1: Create Models

Add to `admissions/models.py`:

```python
class Course(models.Model):
    """
    Online course model.
    """
    title = models.CharField(max_length=200)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    instructor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='taught_courses'
    )
    thumbnail = models.ImageField(upload_to='courses/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title


class Enrollment(models.Model):
    """
    Student course enrollment.
    """
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    progress = models.IntegerField(default=0)  # 0-100
    
    class Meta:
        unique_together = ['student', 'course']
    
    def __str__(self):
        return f"{self.student.get_full_name()} - {self.course.title}"


class Lesson(models.Model):
    """
    Course lesson/module.
    """
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    content = models.TextField()
    video_url = models.URLField(blank=True)
    order = models.IntegerField(default=0)
    duration_minutes = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Assignment(models.Model):
    """
    Course assignment.
    """
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateTimeField()
    max_score = models.IntegerField(default=100)
    
    def __str__(self):
        return self.title


class Submission(models.Model):
    """
    Student assignment submission.
    """
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file = models.FileField(upload_to='submissions/')
    submitted_at = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(null=True, blank=True)
    feedback = models.TextField(blank=True)
    
    class Meta:
        unique_together = ['assignment', 'student']
    
    def __str__(self):
        return f"{self.student.get_full_name()} - {self.assignment.title}"
```

### Step 2: Create Views

Add to `admissions/views.py`:

```python
class CourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'admissions/course_list.html'
    context_object_name = 'courses'
    
    def get_queryset(self):
        return Course.objects.filter(is_active=True)


class CourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = 'admissions/course_detail.html'
    context_object_name = 'course'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_enrolled'] = Enrollment.objects.filter(
            student=self.request.user,
            course=self.object
        ).exists()
        return context
```

---

## Adding Payment Integration

### Step 1: Install Stripe

```bash
pip install stripe
```

### Step 2: Create Payment Model

Add to `admissions/models.py`:

```python
class Payment(models.Model):
    """
    Payment tracking for application fees.
    """
    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    application = models.OneToOneField(
        AdmissionApplication,
        on_delete=models.CASCADE,
        related_name='payment'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    payment_method = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    paid_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Payment for {self.application.registration_number}"
```

### Step 3: Create Payment View

```python
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

class PaymentView(LoginRequiredMixin, TemplateView):
    template_name = 'admissions/payment.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        application = get_object_or_404(
            AdmissionApplication,
            user=self.request.user
        )
        context['application'] = application
        context['stripe_public_key'] = settings.STRIPE_PUBLIC_KEY
        return context
    
    def post(self, request, *args, **kwargs):
        application = get_object_or_404(
            AdmissionApplication,
            user=request.user
        )
        
        try:
            # Create Stripe payment intent
            intent = stripe.PaymentIntent.create(
                amount=5000,  # $50.00 in cents
                currency='usd',
                metadata={'application_id': application.id}
            )
            
            # Create payment record
            Payment.objects.create(
                application=application,
                amount=50.00,
                payment_method='stripe',
                transaction_id=intent.id,
                status='pending'
            )
            
            return JsonResponse({'client_secret': intent.client_secret})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
```

---

## Adding Notification System

### Step 1: Create Notification Model

```python
class Notification(models.Model):
    """
    User notifications.
    """
    NOTIFICATION_TYPES = [
        ('info', 'Information'),
        ('success', 'Success'),
        ('warning', 'Warning'),
        ('error', 'Error'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.title}"
```

### Step 2: Create Notification Utility

Create `admissions/utils.py`:

```python
from .models import Notification

def create_notification(user, title, message, notification_type='info'):
    """
    Create a notification for a user.
    """
    return Notification.objects.create(
        user=user,
        title=title,
        message=message,
        notification_type=notification_type
    )

def notify_application_status_change(application):
    """
    Notify user when application status changes.
    """
    status_messages = {
        'submitted': 'Your application has been submitted successfully.',
        'under_review': 'Your application is now under review.',
        'approved': 'Congratulations! Your application has been approved.',
        'rejected': 'Your application was not approved. Please contact admissions.',
    }
    
    if application.status in status_messages:
        create_notification(
            user=application.user,
            title=f'Application Status: {application.get_status_display()}',
            message=status_messages[application.status],
            notification_type='success' if application.status == 'approved' else 'info'
        )
```

### Step 3: Add Signal Handler

Create `admissions/signals.py`:

```python
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import AdmissionApplication
from .utils import notify_application_status_change

@receiver(post_save, sender=AdmissionApplication)
def application_status_changed(sender, instance, created, **kwargs):
    """
    Send notification when application status changes.
    """
    if not created and instance.status != 'draft':
        notify_application_status_change(instance)
```

Register signals in `admissions/apps.py`:

```python
class AdmissionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'admissions'
    verbose_name = 'Admission Applications'
    
    def ready(self):
        import admissions.signals
```

---

## Best Practices for Extensions

1. **Keep Models Focused**: Each model should have a single responsibility
2. **Use Signals**: For cross-cutting concerns like notifications
3. **Write Tests**: Test new features thoroughly
4. **Document Changes**: Update README and documentation
5. **Use Migrations**: Always create and run migrations for model changes
6. **Follow Django Conventions**: Use Django's built-in features when possible
7. **Security First**: Validate all user input and use permissions
8. **Performance**: Use select_related and prefetch_related for queries
9. **Scalability**: Design features to handle growth
10. **User Experience**: Keep the UI consistent and intuitive

## Running Migrations After Changes

```bash
python manage.py makemigrations
python manage.py migrate
```

## Testing New Features

```bash
python manage.py test admissions
```

## Conclusion

This guide provides a foundation for extending the School Admission Portal. Each feature can be further customized based on specific requirements. Remember to:

- Test thoroughly before deploying
- Keep security in mind
- Document your changes
- Follow Django best practices
- Maintain code quality