from django.urls import path
from .views import *

urlpatterns = [
    path('user/signup', SignupView.as_view(), name='signup'),
    path('user/login', LoginView.as_view(), name='login'),
    path('profile/profile', create_profile, name='create_profile'),
    path('profile/doctor_details', create_doctor, name='create_doctor'),
    path('profile/emergency_contact', create_emergency_contact, name='create_emergency_contact'),
    path('profile/user_details', get_user_details, name='get_user_details'),
    path('profile/profile_details', get_profile_details, name='get_profile_details'),
    path('profile/delete_profile', delete_profile, name='delete_profile'),
    path('mental_health/classify', mental_care, name='mental_care'),
    path('mental_health/mental_health', get_mental_health_data, name='get_mental_health_data'),
]
