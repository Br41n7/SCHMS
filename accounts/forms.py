"""
Forms for user registration and authentication.
Includes validation, password confirmation, and CSRF protection.
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import User


class UserRegistrationForm(UserCreationForm):
    """
    Custom registration form with additional fields and validation.
    Extends Django's UserCreationForm for secure password handling.
    """
    
    first_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First Name',
            'autocomplete': 'given-name'
        })
    )
    
    middle_name = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Middle Name (Optional)',
            'autocomplete': 'additional-name'
        })
    )
    
    last_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last Name',
            'autocomplete': 'family-name'
        })
    )
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email Address',
            'autocomplete': 'email'
        })
    )
    
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'autocomplete': 'new-password'
        }),
        help_text="Password must be at least 8 characters long and contain letters and numbers."
    )
    
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm Password',
            'autocomplete': 'new-password'
        })
    )
    
    class Meta:
        model = User
        fields = ['first_name', 'middle_name', 'last_name', 'email', 'password1', 'password2']
    
    def clean_email(self):
        """
        Validate that the email is unique and properly formatted.
        """
        email = self.cleaned_data.get('email', '').lower()
        
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists.")
        
        return email
    
    def clean_first_name(self):
        """
        Validate first name contains only letters and spaces.
        """
        first_name = self.cleaned_data.get('first_name', '')
        
        if not first_name.replace(' ', '').isalpha():
            raise ValidationError("First name should contain only letters.")
        
        return first_name.strip()
    
    def clean_last_name(self):
        """
        Validate last name contains only letters and spaces.
        """
        last_name = self.cleaned_data.get('last_name', '')
        
        if not last_name.replace(' ', '').isalpha():
            raise ValidationError("Last name should contain only letters.")
        
        return last_name.strip()
    
    def clean_middle_name(self):
        """
        Validate middle name if provided.
        """
        middle_name = self.cleaned_data.get('middle_name', '')
        
        if middle_name and not middle_name.replace(' ', '').isalpha():
            raise ValidationError("Middle name should contain only letters.")
        
        return middle_name.strip()
    
    def save(self, commit=True):
        """
        Save the user with properly formatted data.
        """
        user = super().save(commit=False)
        user.email = self.cleaned_data['email'].lower()
        user.username = user.email.split('@')[0]  # Use email prefix as username
        
        if commit:
            user.save()
        
        return user


class UserLoginForm(AuthenticationForm):
    """
    Custom login form with Bootstrap styling.
    """
    
    username = forms.CharField(
        label="Email or Username",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email or Username',
            'autocomplete': 'username'
        })
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'autocomplete': 'current-password'
        })
    )
    
    def clean_username(self):
        """
        Allow login with email or username.
        """
        username = self.cleaned_data.get('username', '')
        
        # If it looks like an email, try to find user by email
        if '@' in username:
            try:
                user = User.objects.get(email=username.lower())
                return user.username
            except User.DoesNotExist:
                pass
        
        return username


class ProfileUpdateForm(forms.ModelForm):
    """
    Form for updating user profile information.
    """
    
    class Meta:
        model = User
        fields = ['first_name', 'middle_name', 'last_name', 'phone_number']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First Name'
            }),
            'middle_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Middle Name (Optional)'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last Name'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+1234567890'
            }),
        }
    
    def clean_phone_number(self):
        """
        Validate phone number format.
        """
        phone = self.cleaned_data.get('phone_number', '')
        
        if phone and not phone.replace('+', '').replace(' ', '').isdigit():
            raise ValidationError("Please enter a valid phone number.")
        
        return phone