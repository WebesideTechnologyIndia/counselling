from django.shortcuts import render

# Create your views here.


from django.contrib.auth.decorators import login_required


def counselling_services_all_india(request):
    return render(request,'04_counselling_services_home.html')

def college_counselling_services(request):
    return render(request,'02_college_counselling_services.html')

@login_required(login_url='/login/')
def admission_india(request):
    return render(request,'admission_india.html')

def career_counselling_services(request):
    return render(request,'career_counselling_services.html')


@login_required(login_url='/login/')
def admission_abroad(request):
    return render(request, 'admission_abroad.html')

@login_required(login_url='/login/')
def distance_education(request):
    return render(request, 'distance_education.html')

@login_required(login_url='/login/')
def online_education(request):
    return render(request, 'online_education.html')


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
import random
from .models import UserRegistration
from .forms import RegistrationForm, OTPVerificationForm, LoginForm


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
import random
from .models import UserRegistration
from .forms import RegistrationForm, OTPVerificationForm, LoginForm


def register(request):
    # Agar user pehle se logged in hai toh admission_india pe bhej do
    if request.user.is_authenticated:
        return redirect('/admission_india/')
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Save registration data
            registration = form.save(commit=False)
            
            # Generate 6-digit OTP
            otp = str(random.randint(100000, 999999))
            registration.otp = otp
            registration.save()
            
            # Send OTP via email (uncomment when email setup is ready)
            # try:
            #     send_mail(
            #         'Your OTP for Registration',
            #         f'Your OTP is: {otp}',
            #         settings.DEFAULT_FROM_EMAIL,
            #         [registration.email],
            #         fail_silently=False,
            #     )
            # except:
            #     messages.error(request, 'Error sending OTP. Please try again.')
            #     return redirect('register')
            
            # Store email in session for OTP verification
            request.session['registration_email'] = registration.email
            messages.success(request, f'Registration successful! OTP sent to {registration.email}')
            
            # For development - show OTP in console
            print(f"OTP for {registration.email}: {otp}")
            
            return redirect('verify_otp')
    else:
        form = RegistrationForm()
    
    return render(request, 'register.html', {'form': form})


def verify_otp(request):
    email = request.session.get('registration_email')
    
    if not email:
        messages.error(request, 'Please register first.')
        return redirect('register')
    
    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            
            try:
                registration = UserRegistration.objects.get(email=email, otp=otp)
                
                # Create User account
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    password=otp  # You can change this to a proper password later
                )
                
                # Link user to registration
                registration.user = user
                registration.is_verified = True
                registration.save()
                
                # Clear session
                del request.session['registration_email']
                
                messages.success(request, 'OTP verified successfully! You can now login.')
                return redirect('login_view')
                
            except UserRegistration.DoesNotExist:
                messages.error(request, 'Invalid OTP. Please try again.')
    else:
        form = OTPVerificationForm()
    
    return render(request, 'verify_otp.html', {'form': form, 'email': email})

def login_view(request):
    # Agar user pehle se logged in hai toh admission_india pe bhej do
    if request.user.is_authenticated:
        return redirect('/admission_india/')
    
    # Nahi toh login form dikhao
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=email, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful!')
                return redirect('/admission_india/')  # Login ke baad admission_india
            else:
                messages.error(request, 'Invalid email or password.')
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('login_view')


def home_page(request):
    context = {}
    
    # Agar user logged in hai toh uska data dikha do
    if request.user.is_authenticated:
        try:
            user_registration = UserRegistration.objects.get(user=request.user)
            context['user_registration'] = user_registration
        except UserRegistration.DoesNotExist:
            pass
    
    return render(request, 'index.html', context)


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import DocumentUpload, ChoiceFilling, CounsellingStatus, DoubtSession, ComplaintDesk
from .forms import DocumentUploadForm, ChoiceFillingForm, DoubtSessionForm, ComplaintDeskForm


@login_required(login_url='/login/')
def professional_counselling_experts(request):
    # Get user's data
    documents = DocumentUpload.objects.filter(user=request.user).order_by('-uploaded_at')
    choices = ChoiceFilling.objects.filter(user=request.user).order_by('preference_number')
    doubts = DoubtSession.objects.filter(user=request.user).order_by('-created_at')
    complaints = ComplaintDesk.objects.filter(user=request.user).order_by('-created_at')
    
    # Get or create counselling status
    status, created = CounsellingStatus.objects.get_or_create(user=request.user)
    
    # Initialize forms
    document_form = DocumentUploadForm()
    choice_form = ChoiceFillingForm()
    doubt_form = DoubtSessionForm()
    complaint_form = ComplaintDeskForm()
    
    # Handle form submissions
    if request.method == 'POST':
        if 'upload_document' in request.POST:
            document_form = DocumentUploadForm(request.POST, request.FILES)
            if document_form.is_valid():
                doc = document_form.save(commit=False)
                doc.user = request.user
                doc.save()
                messages.success(request, 'Document uploaded successfully!')
                return redirect('professional_counselling_experts')
        
        elif 'add_choice' in request.POST:
            choice_form = ChoiceFillingForm(request.POST)
            if choice_form.is_valid():
                choice = choice_form.save(commit=False)
                choice.user = request.user
                choice.save()
                messages.success(request, 'Choice added successfully!')
                return redirect('professional_counselling_experts')
        
        elif 'submit_doubt' in request.POST:
            doubt_form = DoubtSessionForm(request.POST)
            if doubt_form.is_valid():
                doubt = doubt_form.save(commit=False)
                doubt.user = request.user
                doubt.save()
                messages.success(request, 'Doubt submitted successfully!')
                return redirect('professional_counselling_experts')
        
        elif 'submit_complaint' in request.POST:
            complaint_form = ComplaintDeskForm(request.POST)
            if complaint_form.is_valid():
                complaint = complaint_form.save(commit=False)
                complaint.user = request.user
                complaint.save()
                messages.success(request, 'Complaint registered successfully!')
                return redirect('professional_counselling_experts')
    
    context = {
        'documents': documents,
        'choices': choices,
        'status': status,
        'doubts': doubts,
        'complaints': complaints,
        'document_form': document_form,
        'choice_form': choice_form,
        'doubt_form': doubt_form,
        'complaint_form': complaint_form,
    }
    
    return render(request, 'professional_counselling_experts.html', context)


def management_quota_direct_admission(request):
    return render(request,'management_quot_direct_admission.html')




from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q, Count
from .models import (UserRegistration, DocumentUpload, ChoiceFilling, 
                     CounsellingStatus, DoubtSession, ComplaintDesk, 
                     Notification, UserNotificationRead)
from .forms import (DocumentUploadForm, ChoiceFillingForm, DoubtSessionForm, 
                    ComplaintDeskForm, NotificationForm)


# Check if user is admin
def is_admin(user):
    return user.is_staff or user.is_superuser


@login_required(login_url='/login/')
def student_dashboard(request):
    try:
        user_registration = UserRegistration.objects.get(user=request.user)
    except UserRegistration.DoesNotExist:
        messages.error(request, 'Please complete your registration first.')
        return redirect('register')
    
    # Get user's data
    documents = DocumentUpload.objects.filter(user=request.user).order_by('-uploaded_at')
    choices = ChoiceFilling.objects.filter(user=request.user).order_by('preference_number')
    
    # FIX: Pehle filter karo, phir slice karo
    all_doubts = DoubtSession.objects.filter(user=request.user).order_by('-created_at')
    doubts = all_doubts[:5]
    
    all_complaints = ComplaintDesk.objects.filter(user=request.user).order_by('-created_at')
    complaints = all_complaints[:5]
    
    # Get or create counselling status
    status, created = CounsellingStatus.objects.get_or_create(
        user=request.user,
        defaults={'current_stage': 'Registration Completed'}
    )
    
    # Get notifications
    notifications = Notification.objects.filter(is_active=True)[:10]
    
    # Mark notifications as read
    for notification in notifications:
        UserNotificationRead.objects.get_or_create(
            user=request.user,
            notification=notification
        )
    
    # Calculate completion percentage
    completed_tasks = 0
    if status.application_submitted:
        completed_tasks += 1
    if status.documents_verified:
        completed_tasks += 1
    if status.choice_filling_completed:
        completed_tasks += 1
    
    completion_percentage = (completed_tasks / 3) * 100
    
    # Count statistics
    stats = {
        'total_documents': documents.count(),
        'verified_documents': documents.filter(status='verified').count(),
        'pending_documents': documents.filter(status='pending').count(),
        'total_choices': choices.count(),
        'pending_doubts': all_doubts.filter(status='pending').count(),
        'open_complaints': all_complaints.filter(status='open').count(),
    }
    
    context = {
        'user_registration': user_registration,
        'documents': documents,
        'choices': choices,
        'status': status,
        'doubts': doubts,
        'complaints': complaints,
        'notifications': notifications,
        'stats': stats,
        'completed_tasks': completed_tasks,
        'completion_percentage': completion_percentage,
    }
    
    return render(request, 'student_dashboard.html', context)

# ADMIN DASHBOARD
@login_required(login_url='/login/')
@user_passes_test(is_admin)
def admin_dashboard(request):
    # Get all statistics
    total_students = UserRegistration.objects.filter(is_verified=True).count()
    total_applications = CounsellingStatus.objects.count()
    pending_documents = DocumentUpload.objects.filter(status='pending').count()
    pending_doubts = DoubtSession.objects.filter(status='pending').count()
    open_complaints = ComplaintDesk.objects.filter(status='open').count()
    
    # Recent activities
    recent_registrations = UserRegistration.objects.filter(
        is_verified=True
    ).order_by('-created_at')[:10]
    
    recent_documents = DocumentUpload.objects.select_related('user').order_by('-uploaded_at')[:10]
    recent_doubts = DoubtSession.objects.select_related('user').order_by('-created_at')[:10]
    recent_complaints = ComplaintDesk.objects.select_related('user').order_by('-created_at')[:10]
    
    # Handle notification form
    if request.method == 'POST' and 'create_notification' in request.POST:
        notification_form = NotificationForm(request.POST)
        if notification_form.is_valid():
            notification = notification_form.save(commit=False)
            notification.created_by = request.user
            notification.save()
            messages.success(request, 'Notification created successfully!')
            return redirect('admin_dashboard')
    else:
        notification_form = NotificationForm()
    
    context = {
        'total_students': total_students,
        'total_applications': total_applications,
        'pending_documents': pending_documents,
        'pending_doubts': pending_doubts,
        'open_complaints': open_complaints,
        'recent_registrations': recent_registrations,
        'recent_documents': recent_documents,
        'recent_doubts': recent_doubts,
        'recent_complaints': recent_complaints,
        'notification_form': notification_form,
    }
    
    return render(request, 'admin_dashboard.html', context)


# ADMIN - View All Students
@login_required(login_url='/login/')
@user_passes_test(is_admin)
def admin_students_list(request):
    students = UserRegistration.objects.filter(is_verified=True).select_related('user')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        students = students.filter(
            Q(name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(mobile__icontains=search_query) |
            Q(course__icontains=search_query)
        )
    
    context = {
        'students': students,
        'search_query': search_query,
    }
    
    return render(request, 'admin_students_list.html', context)


# ADMIN - Student Detail View
@login_required(login_url='/login/')
@user_passes_test(is_admin)
def admin_student_detail(request, student_id):
    from datetime import datetime
    
    student = get_object_or_404(UserRegistration, id=student_id)
    documents = DocumentUpload.objects.filter(user=student.user)
    choices = ChoiceFilling.objects.filter(user=student.user).order_by('preference_number')
    doubts = DoubtSession.objects.filter(user=student.user).order_by('-created_at')
    complaints = ComplaintDesk.objects.filter(user=student.user).order_by('-created_at')
    
    try:
        status = CounsellingStatus.objects.get(user=student.user)
    except CounsellingStatus.DoesNotExist:
        status = CounsellingStatus.objects.create(user=student.user)
    
    # Handle application status update - YE NAYA CODE HAI
    if request.method == 'POST' and 'update_application_status' in request.POST:
        status.application_submitted = 'application_submitted' in request.POST
        status.documents_verified = 'documents_verified' in request.POST
        status.choice_filling_completed = 'choice_filling_completed' in request.POST
        status.current_stage = request.POST.get('current_stage')
        status.save()
        
        messages.success(request, f'Application status updated successfully for {student.name}!')
        return redirect('admin_student_detail', student_id=student_id)
    
    # Handle seat allotment update
    if request.method == 'POST' and 'update_seat_allotment' in request.POST:
        status.seat_allotment_status = request.POST.get('seat_allotment_status')
        status.allotted_college = request.POST.get('allotted_college', '')
        status.allotted_course = request.POST.get('allotted_course', '')
        status.allotment_remarks = request.POST.get('allotment_remarks', '')
        
        if status.seat_allotment_status == 'Seat Allotted':
            status.allotment_date = datetime.now()
            status.current_stage = 'Seat Allotted - Pending Admission'
        elif status.seat_allotment_status == 'Admission Confirmed':
            status.current_stage = 'Admission Confirmed'
        
        status.save()
        messages.success(request, f'Seat allotment updated successfully for {student.name}!')
        return redirect('admin_student_detail', student_id=student_id)
    
    # Handle document verification
    if request.method == 'POST' and 'verify_document' in request.POST:
        doc_id = request.POST.get('document_id')
        document = get_object_or_404(DocumentUpload, id=doc_id)
        document.status = 'verified'
        document.save()
        messages.success(request, 'Document verified successfully!')
        return redirect('admin_student_detail', student_id=student_id)
    
    # Handle document rejection
    if request.method == 'POST' and 'reject_document' in request.POST:
        doc_id = request.POST.get('document_id')
        document = get_object_or_404(DocumentUpload, id=doc_id)
        document.status = 'rejected'
        document.save()
        messages.warning(request, 'Document rejected!')
        return redirect('admin_student_detail', student_id=student_id)
    
    # Handle doubt response
    if request.method == 'POST' and 'respond_doubt' in request.POST:
        doubt_id = request.POST.get('doubt_id')
        response_text = request.POST.get('response')
        doubt = get_object_or_404(DoubtSession, id=doubt_id)
        doubt.response = response_text
        doubt.status = 'resolved'
        doubt.save()
        messages.success(request, 'Doubt resolved successfully!')
        return redirect('admin_student_detail', student_id=student_id)
    
    # Handle complaint response
    if request.method == 'POST' and 'respond_complaint' in request.POST:
        complaint_id = request.POST.get('complaint_id')
        response_text = request.POST.get('admin_response')
        complaint = get_object_or_404(ComplaintDesk, id=complaint_id)
        complaint.admin_response = response_text
        complaint.status = 'resolved'
        complaint.save()
        messages.success(request, 'Complaint resolved successfully!')
        return redirect('admin_student_detail', student_id=student_id)
    
    context = {
        'student': student,
        'documents': documents,
        'choices': choices,
        'status': status,
        'doubts': doubts,
        'complaints': complaints,
    }
    
    return render(request, 'admin_student_detail.html', context)

# ADMIN - Manage Notifications
@login_required(login_url='/login/')
@user_passes_test(is_admin)
def admin_notifications(request):
    notifications = Notification.objects.all().order_by('-created_at')
    
    if request.method == 'POST' and 'delete_notification' in request.POST:
        notif_id = request.POST.get('notification_id')
        notification = get_object_or_404(Notification, id=notif_id)
        notification.delete()
        messages.success(request, 'Notification deleted successfully!')
        return redirect('admin_notifications')
    
    context = {
        'notifications': notifications,
    }
    
    return render(request, 'admin_notifications.html', context)