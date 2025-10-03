from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import UserRegistration


@admin.register(UserRegistration)
class UserRegistrationAdmin(admin.ModelAdmin):
    list_display = [
        'name', 
        'email', 
        'mobile', 
        'course', 
        'state', 
        'city', 
        'is_verified', 
        'created_at'
    ]
    
    list_filter = [
        'is_verified', 
        'state', 
        'course', 
        'created_at'
    ]
    
    search_fields = [
        'name', 
        'email', 
        'mobile', 
        'father_name', 
        'city'
    ]
    
    readonly_fields = [
        'created_at', 
        'updated_at', 
        'otp'
    ]
    
    list_per_page = 25
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'father_name', 'email')
        }),
        ('Contact Details', {
            'fields': ('mobile', 'whatsapp_mobile')
        }),
        ('Academic Information', {
            'fields': ('course', 'state', 'city')
        }),
        ('Account Information', {
            'fields': ('user', 'is_verified', 'otp')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return self.readonly_fields + ('email',)
        return self.readonly_fields
    

from django.contrib import admin
from .models import DocumentUpload, ChoiceFilling, CounsellingStatus, DoubtSession, ComplaintDesk


@admin.register(DocumentUpload)
class DocumentUploadAdmin(admin.ModelAdmin):
    list_display = ['user', 'document_type', 'uploaded_at', 'status']
    list_filter = ['status', 'uploaded_at']
    search_fields = ['user__username', 'document_type']


@admin.register(ChoiceFilling)
class ChoiceFillingAdmin(admin.ModelAdmin):
    list_display = ['user', 'college_name', 'course_name', 'preference_number', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'college_name', 'course_name']


@admin.register(CounsellingStatus)
class CounsellingStatusAdmin(admin.ModelAdmin):
    list_display = ['user', 'current_stage', 'application_submitted', 'documents_verified', 'updated_at']
    list_filter = ['application_submitted', 'documents_verified', 'choice_filling_completed']
    search_fields = ['user__username']


@admin.register(DoubtSession)
class DoubtSessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'subject', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username', 'subject']


@admin.register(ComplaintDesk)
class ComplaintDeskAdmin(admin.ModelAdmin):
    list_display = ['user', 'complaint_subject', 'priority', 'status', 'created_at']
    list_filter = ['status', 'priority', 'created_at']
    search_fields = ['user__username', 'complaint_subject']