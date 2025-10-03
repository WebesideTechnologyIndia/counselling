from django import forms
from .models import UserRegistration

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = UserRegistration
        fields = ['name', 'father_name', 'mobile', 'whatsapp_mobile', 'email', 'course', 'state', 'city']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your full name'
            }),
            'father_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Enter father's name"
            }),
            'mobile': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter mobile number'
            }),
            'whatsapp_mobile': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter WhatsApp number'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email address'
            }),
            'course': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter course name'
            }),
            'state': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter state'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter city'
            }),
        }

class OTPVerificationForm(forms.Form):
    otp = forms.CharField(
        max_length=6,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter 6-digit OTP'
        })
    )

class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password'
        })
    )



from django import forms
from .models import DocumentUpload, ChoiceFilling, DoubtSession, ComplaintDesk

# 1. Document Upload Form
class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = DocumentUpload
        fields = ['document_type', 'document_file']
        widgets = {
            'document_type': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter document type (e.g., 10th Marksheet)'
            }),
            'document_file': forms.FileInput(attrs={
                'class': 'form-control'
            })
        }


# 2. Choice Filling Form
class ChoiceFillingForm(forms.ModelForm):
    class Meta:
        model = ChoiceFilling
        fields = ['college_name', 'course_name', 'preference_number']
        widgets = {
            'college_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter college name'
            }),
            'course_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter course name'
            }),
            'preference_number': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter preference number',
                'min': '1'
            })
        }


# 3. Doubt Session Form
class DoubtSessionForm(forms.ModelForm):
    class Meta:
        model = DoubtSession
        fields = ['subject', 'doubt_description']
        widgets = {
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your doubt subject'
            }),
            'doubt_description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe your doubt in detail',
                'rows': 4
            })
        }


# 4. Complaint Desk Form
class ComplaintDeskForm(forms.ModelForm):
    class Meta:
        model = ComplaintDesk
        fields = ['complaint_type', 'complaint_subject', 'complaint_description', 'priority']
        widgets = {
            'complaint_type': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter complaint type'
            }),
            'complaint_subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter complaint subject'
            }),
            'complaint_description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe your complaint',
                'rows': 4
            }),
            'priority': forms.Select(choices=[
                ('low', 'Low'),
                ('normal', 'Normal'),
                ('high', 'High'),
                ('urgent', 'Urgent')
            ], attrs={
                'class': 'form-control'
            })
        }


from django import forms
from .models import Notification

class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['title', 'message', 'notification_type', 'college_name', 'fees_amount', 'counselling_date']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter notification title'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter notification message',
                'rows': 4
            }),
            'notification_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'college_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'College name (optional)'
            }),
            'fees_amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Fees amount (optional)'
            }),
            'counselling_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }