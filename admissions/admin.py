"""
Admin configuration for admission applications.
Includes approval workflow and detailed views.
"""
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from .models import AdmissionApplication


@admin.register(AdmissionApplication)
class AdmissionApplicationAdmin(admin.ModelAdmin):
    """
    Custom admin interface for admission applications with approval workflow.
    """
    
    list_display = [
        'registration_number',
        'user_full_name',
        'user_email',
        'program_choice',
        'status_badge',
        'completion_progress',
        'submitted_at',
        'created_at',
    ]
    
    list_filter = [
        'status',
        'program_choice',
        'gender',
        'created_at',
        'submitted_at',
    ]
    
    search_fields = [
        'registration_number',
        'user__email',
        'user__first_name',
        'user__last_name',
        'course_of_study',
    ]
    
    readonly_fields = [
        'registration_number',
        'user',
        'created_at',
        'updated_at',
        'submitted_at',
        'completion_progress',
    ]
    
    fieldsets = (
        ('Application Information', {
            'fields': (
                'registration_number',
                'user',
                'status',
                'completion_progress',
            )
        }),
        ('Personal Information', {
            'fields': (
                'date_of_birth',
                'gender',
                'nationality',
                'address',
                'city',
                'state',
                'postal_code',
            )
        }),
        ('Program Information', {
            'fields': (
                'program_choice',
                'course_of_study',
            )
        }),
        ('Documents', {
            'fields': (
                'passport_photo',
                'olevel_result',
                'birth_certificate',
                'additional_document_1',
                'additional_document_2',
            )
        }),
        ('Review Information', {
            'fields': (
                'reviewed_by',
                'review_notes',
                'reviewed_at',
            )
        }),
        ('Timestamps', {
            'fields': (
                'created_at',
                'updated_at',
                'submitted_at',
            ),
            'classes': ('collapse',)
        }),
    )
    
    actions = [
        'approve_applications',
        'reject_applications',
        'mark_under_review',
    ]
    
    def user_full_name(self, obj):
        """Display user's full name."""
        return obj.user.get_full_name()
    user_full_name.short_description = 'Applicant Name'
    
    def user_email(self, obj):
        """Display user's email."""
        return obj.user.email
    user_email.short_description = 'Email'
    
    def status_badge(self, obj):
        """Display status as colored badge."""
        badge_class = obj.get_status_badge_class()
        return format_html(
            '<span class="badge bg-{}">{}</span>',
            badge_class,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def completion_progress(self, obj):
        """Display completion progress bar."""
        percentage = obj.get_completion_percentage()
        color = 'success' if percentage == 100 else 'warning' if percentage >= 50 else 'danger'
        return format_html(
            '<div class="progress" style="width: 100px;">'
            '<div class="progress-bar bg-{}" role="progressbar" style="width: {}%">{}%</div>'
            '</div>',
            color,
            percentage,
            percentage
        )
    completion_progress.short_description = 'Progress'
    
    def approve_applications(self, request, queryset):
        """Bulk approve applications."""
        count = 0
        for application in queryset:
            if application.status in ['submitted', 'under_review']:
                application.approve(request.user, 'Approved via bulk action')
                count += 1
        
        self.message_user(
            request,
            f'{count} application(s) approved successfully.'
        )
    approve_applications.short_description = 'Approve selected applications'
    
    def reject_applications(self, request, queryset):
        """Bulk reject applications."""
        count = 0
        for application in queryset:
            if application.status in ['submitted', 'under_review']:
                application.reject(request.user, 'Rejected via bulk action')
                count += 1
        
        self.message_user(
            request,
            f'{count} application(s) rejected.'
        )
    reject_applications.short_description = 'Reject selected applications'
    
    def mark_under_review(self, request, queryset):
        """Mark applications as under review."""
        count = queryset.filter(status='submitted').update(
            status='under_review',
            reviewed_by=request.user,
            reviewed_at=timezone.now()
        )
        
        self.message_user(
            request,
            f'{count} application(s) marked as under review.'
        )
    mark_under_review.short_description = 'Mark as under review'
    
    def save_model(self, request, obj, form, change):
        """
        Auto-set reviewed_by and reviewed_at when status changes.
        """
        if change and 'status' in form.changed_data:
            if obj.status in ['approved', 'rejected', 'under_review']:
                obj.reviewed_by = request.user
                obj.reviewed_at = timezone.now()
        
        super().save_model(request, obj, form, change)