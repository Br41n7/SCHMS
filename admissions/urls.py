"""
URL patterns for admissions app.
"""
from django.urls import path
from .views import (
    DashboardView,
    PersonalInfoView,
    ProgramInfoView,
    DocumentUploadView,
    ApplicationDetailView,
    SubmitApplicationView,
)

app_name = 'admissions'

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('personal-info/', PersonalInfoView.as_view(), name='personal_info'),
    path('program-info/', ProgramInfoView.as_view(), name='program_info'),
    path('upload-documents/', DocumentUploadView.as_view(), name='document_upload'),
    path('application-detail/', ApplicationDetailView.as_view(), name='application_detail'),
    path('submit/', SubmitApplicationView.as_view(), name='submit_application'),
]