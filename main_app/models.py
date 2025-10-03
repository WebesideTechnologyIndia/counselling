from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class UserRegistration(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    whatsapp_mobile = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    course = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    otp = models.CharField(max_length=6, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.email}"

    class Meta:
        verbose_name = "User Registration"
        verbose_name_plural = "User Registrations"


from django.db import models
from django.contrib.auth.models import User

# 1. Document Upload Model
class DocumentUpload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    document_type = models.CharField(max_length=100)
    document_file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='pending')
    
    def __str__(self):
        return f"{self.user.username} - {self.document_type}"


# 2. Choice Filling Model
class ChoiceFilling(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    college_name = models.CharField(max_length=200)
    course_name = models.CharField(max_length=200)
    preference_number = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['preference_number']
    
    def __str__(self):
        return f"{self.user.username} - Preference {self.preference_number}"


class CounsellingStatus(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    application_submitted = models.BooleanField(default=False)
    documents_verified = models.BooleanField(default=False)
    choice_filling_completed = models.BooleanField(default=False)
    seat_allotment_status = models.CharField(max_length=100, default='Pending')
    current_stage = models.CharField(max_length=200, default='Registration Completed')
    
    # NEW FIELDS - Ye add karo
    allotted_college = models.CharField(max_length=300, blank=True, null=True)
    allotted_course = models.CharField(max_length=200, blank=True, null=True)
    allotment_remarks = models.TextField(blank=True, null=True)
    allotment_date = models.DateTimeField(blank=True, null=True)
    
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.current_stage}"


# 4. Doubt Sessions Model
class DoubtSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    doubt_description = models.TextField()
    response = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.subject}"


# 5. Complaint Desk Model
class ComplaintDesk(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    complaint_type = models.CharField(max_length=100)
    complaint_subject = models.CharField(max_length=200)
    complaint_description = models.TextField()
    priority = models.CharField(max_length=50, default='normal')
    status = models.CharField(max_length=50, default='open')
    admin_response = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.complaint_subject}"
    

from django.db import models
from django.contrib.auth.models import User

# Notification Model - Admin announcements ke liye
class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('general', 'General'),
        ('counselling', 'Counselling'),
        ('admission', 'Admission'),
        ('fees', 'Fees'),
        ('important', 'Important'),
    ]
    
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES, default='general')
    college_name = models.CharField(max_length=200, blank=True, null=True)
    fees_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    counselling_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_notifications')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


# User Read Notifications - Track karega kis student ne kya padha
class UserNotificationRead(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    read_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'notification')