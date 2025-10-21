"""
Class-based views for admission application management.
Implements step-by-step application process and dashboard.
"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView, DetailView
from django.contrib import messages
from django.utils import timezone

from .models import AdmissionApplication
from .forms import PersonalInfoForm, ProgramInfoForm, DocumentUploadForm


class DashboardView(LoginRequiredMixin, TemplateView):
    """
    Main dashboard view showing application status and progress.
    """
    template_name = 'admissions/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get or create application for current user
        application, created = AdmissionApplication.objects.get_or_create(
            user=self.request.user
        )
        
        context['application'] = application
        context['completion_percentage'] = application.get_completion_percentage()
        context['can_submit'] = application.can_submit()
        context['title'] = 'Dashboard'
        
        return context


class PersonalInfoView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Step 1: Personal Information Form
    """
    model = AdmissionApplication
    form_class = PersonalInfoForm
    template_name = 'admissions/personal_info.html'
    success_url = reverse_lazy('admissions:dashboard')
    success_message = "Personal information saved successfully!"
    
    def get_object(self, queryset=None):
        """
        Get or create application for current user.
        """
        application, created = AdmissionApplication.objects.get_or_create(
            user=self.request.user
        )
        return application
    
    def form_valid(self, form):
        """
        Mark personal info as completed.
        """
        form.instance.personal_info_completed = True
        messages.success(self.request, self.success_message)
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Personal Information'
        context['step'] = 1
        return context


class ProgramInfoView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Step 2: Program Information Form
    """
    model = AdmissionApplication
    form_class = ProgramInfoForm
    template_name = 'admissions/program_info.html'
    success_url = reverse_lazy('admissions:dashboard')
    success_message = "Program information saved successfully!"
    
    def get_object(self, queryset=None):
        """
        Get or create application for current user.
        """
        application, created = AdmissionApplication.objects.get_or_create(
            user=self.request.user
        )
        return application
    
    def dispatch(self, request, *args, **kwargs):
        """
        Ensure personal info is completed first.
        """
        application = self.get_object()
        if not application.personal_info_completed:
            messages.warning(request, "Please complete personal information first.")
            return redirect('admissions:personal_info')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        """
        Mark program info as completed.
        """
        form.instance.program_info_completed = True
        messages.success(self.request, self.success_message)
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Program Information'
        context['step'] = 2
        return context


class DocumentUploadView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Step 3: Document Upload Form
    """
    model = AdmissionApplication
    form_class = DocumentUploadForm
    template_name = 'admissions/document_upload.html'
    success_url = reverse_lazy('admissions:dashboard')
    success_message = "Documents uploaded successfully!"
    
    def get_object(self, queryset=None):
        """
        Get or create application for current user.
        """
        application, created = AdmissionApplication.objects.get_or_create(
            user=self.request.user
        )
        return application
    
    def dispatch(self, request, *args, **kwargs):
        """
        Ensure previous steps are completed.
        """
        application = self.get_object()
        
        if not application.personal_info_completed:
            messages.warning(request, "Please complete personal information first.")
            return redirect('admissions:personal_info')
        
        if not application.program_info_completed:
            messages.warning(request, "Please complete program information first.")
            return redirect('admissions:program_info')
        
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        """
        Mark documents as uploaded if required files are present.
        """
        application = form.instance
        
        # Check if required documents are uploaded
        if application.passport_photo and application.olevel_result and application.birth_certificate:
            application.documents_uploaded = True
        
        messages.success(self.request, self.success_message)
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Upload Documents'
        context['step'] = 3
        return context


class ApplicationDetailView(LoginRequiredMixin, DetailView):
    """
    View to display complete application details.
    """
    model = AdmissionApplication
    template_name = 'admissions/application_detail.html'
    context_object_name = 'application'
    
    def get_object(self, queryset=None):
        """
        Get application for current user.
        """
        return get_object_or_404(AdmissionApplication, user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Application Details'
        return context


class SubmitApplicationView(LoginRequiredMixin, TemplateView):
    """
    View to handle application submission.
    """
    template_name = 'admissions/submit_confirmation.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        application = get_object_or_404(AdmissionApplication, user=self.request.user)
        context['application'] = application
        context['title'] = 'Submit Application'
        return context
    
    def post(self, request, *args, **kwargs):
        """
        Handle application submission.
        """
        application = get_object_or_404(AdmissionApplication, user=request.user)
        
        if application.can_submit():
            application.submit()
            messages.success(
                request,
                f"Application {application.registration_number} submitted successfully! "
                "You will be notified once it has been reviewed."
            )
            return redirect('admissions:dashboard')
        else:
            messages.error(
                request,
                "Cannot submit application. Please ensure all steps are completed."
            )
            return redirect('admissions:dashboard')