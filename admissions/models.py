"""
Models for the admission application system.
Handles application data, file uploads, and approval workflow.
"""
import os
import uuid
from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.utils import timezone


def generate_registration_number():
    """
    Generate a unique registration number for each application.
    Format: YEAR-RANDOM_UUID
    """
    year = timezone.now().year
    unique_id = str(uuid.uuid4().hex[:8]).upper()
    return f"{year}-{unique_id}"


def user_directory_path(instance, filename):
    """
    File upload path: uploads/user_<id>/<filename>
    """
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4().hex}.{ext}"
    return os.path.join('uploads', f'user_{instance.user.id}', filename)


class AdmissionApplication(models.Model):
    """
    Main admission application model.
    Tracks application status and stores applicant information.
    """
    
    # Application Status Choices
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    # Gender Choices
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    # Program Choices (can be extended)
    PROGRAM_CHOICES = [
        ('undergraduate', 'Undergraduate'),
        ('postgraduate', 'Postgraduate'),
        ('diploma', 'Diploma'),
        ('certificate', 'Certificate'),
    ]
    
    # Core Fields
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='admission_application'
    )
    
    registration_number = models.CharField(
        max_length=50,
        unique=True,
        default=generate_registration_number,
        editable=False,
        help_text="Unique registration number for this application"
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft',
        help_text="Current status of the application"
    )
    
    # Personal Information
    date_of_birth = models.DateField(
        null=True,
        blank=True,
        help_text="Applicant's date of birth"
    )
    
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        blank=True,
        help_text="Applicant's gender"
    )
    
    nationality = models.CharField(
        max_length=100,
        blank=True,
        help_text="Applicant's nationality"
    )
    
    address = models.TextField(
        blank=True,
        help_text="Residential address"
    )
    
    city = models.CharField(
        max_length=100,
        blank=True,
        help_text="City of residence"
    )
    
    state = models.CharField(
        max_length=100,
        blank=True,
        help_text="State/Province"
    )
    
    postal_code = models.CharField(
        max_length=20,
        blank=True,
        help_text="Postal/ZIP code"
    )
    
    # Program Information
    program_choice = models.CharField(
        max_length=50,
        choices=PROGRAM_CHOICES,
        blank=True,
        help_text="Desired program of study"
    )
    
    course_of_study = models.CharField(
        max_length=200,
        blank=True,
        help_text="Specific course or major"
    )
    
    # File Uploads
    passport_photo = models.ImageField(
        upload_to=user_directory_path,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
        null=True,
        blank=True,
        help_text="Upload passport photograph (JPG, PNG only, max 5MB)"
    )
    
    olevel_result = models.FileField(
        upload_to=user_directory_path,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'])],
        null=True,
        blank=True,
        help_text="Upload O'Level result (PDF, JPG, PNG only, max 5MB)"
    )
    
    birth_certificate = models.FileField(
        upload_to=user_directory_path,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'])],
        null=True,
        blank=True,
        help_text="Upload birth certificate (PDF, JPG, PNG only, max 5MB)"
    )
    
    # Additional Documents (for extensibility)
    additional_document_1 = models.FileField(
        upload_to=user_directory_path,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])],
        null=True,
        blank=True,
        help_text="Additional supporting document (optional)"
    )
    
    additional_document_2 = models.FileField(
        upload_to=user_directory_path,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])],
        null=True,
        blank=True,
        help_text="Additional supporting document (optional)"
    )
    
    # Application Progress Tracking
    personal_info_completed = models.BooleanField(
        default=False,
        help_text="Step 1: Personal information completed"
    )
    
    program_info_completed = models.BooleanField(
        default=False,
        help_text="Step 2: Program information completed"
    )
    
    documents_uploaded = models.BooleanField(
        default=False,
        help_text="Step 3: Documents uploaded"
    )
    
    # Admin Review Fields
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_applications',
        help_text="Admin who reviewed this application"
    )
    
    review_notes = models.TextField(
        blank=True,
        help_text="Admin notes and comments"
    )
    
    reviewed_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Date and time of review"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    submitted_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Date and time when application was submitted"
    )
    
    class Meta:
        verbose_name = "Admission Application"
        verbose_name_plural = "Admission Applications"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['registration_number']),
            models.Index(fields=['status']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return f"{self.registration_number} - {self.user.get_full_name()}"
    
    def get_completion_percentage(self):
        """
        Calculate application completion percentage.
        """
        steps = [
            self.personal_info_completed,
            self.program_info_completed,
            self.documents_uploaded,
        ]
        completed = sum(steps)
        total = len(steps)
        return int((completed / total) * 100)
    
    def is_complete(self):
        """
        Check if all required steps are completed.
        """
        return all([
            self.personal_info_completed,
            self.program_info_completed,
            self.documents_uploaded,
        ])
    
    def can_submit(self):
        """
        Check if application can be submitted.
        """
        return self.is_complete() and self.status == 'draft'
    
    def submit(self):
        """
        Submit the application for review.
        """
        if self.can_submit():
            self.status = 'submitted'
            self.submitted_at = timezone.now()
            self.save()
            return True
        return False
    
    def approve(self, admin_user, notes=''):
        """
        Approve the application.
        """
        self.status = 'approved'
        self.reviewed_by = admin_user
        self.review_notes = notes
        self.reviewed_at = timezone.now()
        self.save()
    
    def reject(self, admin_user, notes=''):
        """
        Reject the application.
        """
        self.status = 'rejected'
        self.reviewed_by = admin_user
        self.review_notes = notes
        self.reviewed_at = timezone.now()
        self.save()
    
    def get_status_badge_class(self):
        """
        Return Bootstrap badge class based on status.
        """
        status_classes = {
            'draft': 'secondary',
            'submitted': 'info',
            'under_review': 'warning',
            'approved': 'success',
            'rejected': 'danger',
        }
        return status_classes.get(self.status, 'secondary')