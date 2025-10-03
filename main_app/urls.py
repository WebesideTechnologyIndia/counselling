# urls.py
from django.contrib import admin
from django.urls import path
from .views import *   # import your view

urlpatterns = [
    path('', home_page, name='home'),  # home page URL
    path('home/', home_page, name='home'),  # home page URL
    path('counselling_services_all_india/',counselling_services_all_india,name='counselling_services_all_india'),
    path('college_counselling_services/',college_counselling_services,name='college_counselling_services'),
    path('admission_india/',admission_india,name="admission_india"),
    path('career_counselling_Services/',career_counselling_services,name='career_counselling_services'),
    path('admission_abroad/',admission_abroad,name='admission_abroad'),
    path('distance_education/',distance_education,name='distance_education'),
    path('online_education/',online_education,name='online_education'),
    path('register/', register, name='register'),
    path('verify-otp/', verify_otp, name='verify_otp'),
    path('login/', login_view, name='login_view'),
    path('logout/', logout_view, name='logout_view'),
    path('professional_counselling_experts/',professional_counselling_experts,name='professional_counselling_experts'),
    path('management_quota_direct_admission/',management_quota_direct_admission,name='management_quota_direct_admission'),

    path('student/dashboard/', student_dashboard, name='student_dashboard'),
    
    # Admin URLs
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('admin/students/', admin_students_list, name='admin_students_list'),
    path('admin/student/<int:student_id>/', admin_student_detail, name='admin_student_detail'),
    path('admin/notifications/', admin_notifications, name='admin_notifications'),

]
