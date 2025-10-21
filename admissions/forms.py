"""
Forms for admission application process.
Step-by-step forms with validation.
"""
from django import forms
from django.core.exceptions import ValidationError
from .models import AdmissionApplication


class PersonalInfoForm(forms.ModelForm):
    """
    Step 1: Personal Information Form
    """
    
    class Meta:
        model = AdmissionApplication
        fields = [
            'date_of_birth',
            'gender',
            'nationality',
            'address',
            'city',
            'state',
            'postal_code',
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'placeholder': 'YYYY-MM-DD'
            }),
            'gender': forms.Select(attrs={
                'class': 'form-select'
            }),
            'nationality': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Nigerian, American'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter your full residential address'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'City'
            }),
            'state': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'State/Province'
            }),
            'postal_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Postal/ZIP Code'
            }),
        }
    
    def clean_date_of_birth(self):
        """
        Validate date of birth (must be at least 15 years old).
        """
        from datetime import date, timedelta
        
        dob = self.cleaned_data.get('date_of_birth')
        if dob:
            today = date.today()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            
            if age < 15:
                raise ValidationError("Applicant must be at least 15 years old.")
            
            if age > 100:
                raise ValidationError("Please enter a valid date of birth.")
        
        return dob


class ProgramInfoForm(forms.ModelForm):
    """
    Step 2: Program Information Form
    """
    
    class Meta:
        model = AdmissionApplication
        fields = [
            'program_choice',
            'course_of_study',
        ]
        widgets = {
            'program_choice': forms.Select(attrs={
                'class': 'form-select'
            }),
            'course_of_study': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Computer Science, Business Administration'
            }),
        }
    
    def clean_course_of_study(self):
        """
        Validate course of study is not empty.
        """
        course = self.cleaned_data.get('course_of_study', '').strip()
        
        if not course:
            raise ValidationError("Please specify your desired course of study.")
        
        return course


class DocumentUploadForm(forms.ModelForm):
    """
    Step 3: Document Upload Form
    """
    
    class Meta:
        model = AdmissionApplication
        fields = [
            'passport_photo',
            'olevel_result',
            'birth_certificate',
            'additional_document_1',
            'additional_document_2',
        ]
        widgets = {
            'passport_photo': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/jpeg,image/png'
            }),
            'olevel_result': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'application/pdf,image/jpeg,image/png'
            }),
            'birth_certificate': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'application/pdf,image/jpeg,image/png'
            }),
            'additional_document_1': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'application/pdf,.doc,.docx'
            }),
            'additional_document_2': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'application/pdf,.doc,.docx'
            }),
        }
    
    def clean_passport_photo(self):
        """
        Validate passport photo size and format.
        """
        photo = self.cleaned_data.get('passport_photo')
        
        if photo:
            # Check file size (max 5MB)
            if photo.size > 5 * 1024 * 1024:
                raise ValidationError("Passport photo must be less than 5MB.")
            
            # Check file extension
            ext = photo.name.split('.')[-1].lower()
            if ext not in ['jpg', 'jpeg', 'png']:
                raise ValidationError("Passport photo must be JPG or PNG format.")
        
        return photo
    
    def clean_olevel_result(self):
        """
        Validate O'Level result file.
        """
        result = self.cleaned_data.get('olevel_result')
        
        if result:
            # Check file size (max 5MB)
            if result.size > 5 * 1024 * 1024:
                raise ValidationError("O'Level result must be less than 5MB.")
            
            # Check file extension
            ext = result.name.split('.')[-1].lower()
            if ext not in ['pdf', 'jpg', 'jpeg', 'png']:
                raise ValidationError("O'Level result must be PDF, JPG, or PNG format.")
        
        return result
    
    def clean_birth_certificate(self):
        """
        Validate birth certificate file.
        """
        cert = self.cleaned_data.get('birth_certificate')
        
        if cert:
            # Check file size (max 5MB)
            if cert.size > 5 * 1024 * 1024:
                raise ValidationError("Birth certificate must be less than 5MB.")
            
            # Check file extension
            ext = cert.name.split('.')[-1].lower()
            if ext not in ['pdf', 'jpg', 'jpeg', 'png']:
                raise ValidationError("Birth certificate must be PDF, JPG, or PNG format.")
        
        return cert


class ApplicationReviewForm(forms.ModelForm):
    """
    Admin form for reviewing applications.
    """
    
    class Meta:
        model = AdmissionApplication
        fields = ['status', 'review_notes']
        widgets = {
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'review_notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Enter review notes and comments...'
            }),
        }