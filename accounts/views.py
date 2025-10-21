"""
Class-based views for user authentication and registration.
Implements secure registration, login, logout, and profile management.
"""
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetConfirmView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.shortcuts import redirect
from django.contrib import messages

from .forms import UserRegistrationForm, UserLoginForm, ProfileUpdateForm
from .models import User


class RegisterView(SuccessMessageMixin, CreateView):
    """
    User registration view with form validation and automatic login.
    """
    model = User
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('admissions:dashboard')
    success_message = "Registration successful! Welcome to the School Admission Portal."
    
    def dispatch(self, request, *args, **kwargs):
        """
        Redirect authenticated users to dashboard.
        """
        if request.user.is_authenticated:
            return redirect('admissions:dashboard')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        """
        Save the user and log them in automatically.
        """
        response = super().form_valid(form)
        
        # Log the user in after successful registration
        login(self.request, self.object, backend='django.contrib.auth.backends.ModelBackend')
        
        return response
    
    def get_context_data(self, **kwargs):
        """
        Add additional context for the template.
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Register'
        return context


class CustomLoginView(SuccessMessageMixin, LoginView):
    """
    Custom login view with email or username support.
    """
    form_class = UserLoginForm
    template_name = 'accounts/login.html'
    success_message = "Welcome back! You have successfully logged in."
    
    def dispatch(self, request, *args, **kwargs):
        """
        Redirect authenticated users to dashboard.
        """
        if request.user.is_authenticated:
            return redirect('admissions:dashboard')
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        """
        Redirect to next parameter or default dashboard.
        """
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return reverse_lazy('admissions:dashboard')
    
    def get_context_data(self, **kwargs):
        """
        Add additional context for the template.
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Login'
        return context


class CustomLogoutView(LogoutView):
    """
    Custom logout view with success message.
    """
    next_page = reverse_lazy('accounts:login')
    
    def dispatch(self, request, *args, **kwargs):
        """
        Add success message on logout.
        """
        if request.user.is_authenticated:
            messages.success(request, "You have been successfully logged out.")
        return super().dispatch(request, *args, **kwargs)


class ProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    View for users to update their profile information.
    """
    model = User
    form_class = ProfileUpdateForm
    template_name = 'accounts/profile_update.html'
    success_url = reverse_lazy('admissions:dashboard')
    success_message = "Your profile has been updated successfully."
    
    def get_object(self, queryset=None):
        """
        Return the current user's profile.
        """
        return self.request.user
    
    def get_context_data(self, **kwargs):
        """
        Add additional context for the template.
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Profile'
        return context


class CustomPasswordResetView(SuccessMessageMixin, PasswordResetView):
    """
    Custom password reset view with success message.
    """
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    subject_template_name = 'accounts/password_reset_subject.txt'
    success_url = reverse_lazy('accounts:login')
    success_message = "Password reset instructions have been sent to your email."
    
    def get_context_data(self, **kwargs):
        """
        Add additional context for the template.
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reset Password'
        return context


class CustomPasswordResetConfirmView(SuccessMessageMixin, PasswordResetConfirmView):
    """
    Custom password reset confirmation view.
    """
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:login')
    success_message = "Your password has been reset successfully. You can now log in."
    
    def get_context_data(self, **kwargs):
        """
        Add additional context for the template.
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Set New Password'
        return context