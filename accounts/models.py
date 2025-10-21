"""
Custom User Model for the School Admission Portal.
Extends Django's AbstractUser to include additional fields.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


class User(AbstractUser):
    """
    Custom User model with additional fields for school portal.
    Extends Django's AbstractUser to maintain compatibility with built-in auth system.
    """
    
    # Additional name fields
    middle_name = models.CharField(
        max_length=150,
        blank=True,
        help_text="Optional middle name"
    )
    
    # Override email to make it required and unique
    email = models.EmailField(
        unique=True,
        help_text="Required. Enter a valid email address."
    )
 
    # Phone number with validation
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=17,
        blank=True,
        help_text="Optional. Contact phone number."
    )
    
    # Profile completion tracking
    profile_completed = models.BooleanField(
        default=False,
        help_text="Indicates if user has completed their profile"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['-date_joined']
    
    def __str__(self):
        return self.get_full_name() or self.username
    
    def get_full_name(self):
        """
        Return the first_name, middle_name, and last_name with spaces in between.
        """
        full_name = f"{self.first_name}"
        if self.middle_name:
            full_name += f" {self.middle_name}"
        if self.last_name:
            full_name += f" {self.last_name}"
        return full_name.strip() or self.username
    
    def save(self, *args, **kwargs):
        """
        Override save to ensure email is lowercase and username is set.
        """
        if self.email:
            self.email = self.email.lower()
        
        # If username is not set, use email prefix
        if not self.username:
            self.username = self.email.split('@')[0]
        
        super().save(*args, **kwargs)
