from django.contrib import admin
from .models import User, Profile, Doctor, EmergencyContact, MentalHealth

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone_number')
    search_fields = ('username', 'email', 'phone_number')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'dob', 'gender', 'appointment_frequency', 'test_timing')
    list_filter = ('gender', 'appointment_frequency')
    search_fields = ('user__username', 'user__email')

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'clinic_or_hospital_name', 'email')
    search_fields = ('name', 'phone_number', 'email')

@admin.register(EmergencyContact)
class EmergencyContactAdmin(admin.ModelAdmin):
    list_display = ('contact_name', 'contact_phone_number', 'contact_relationship', 'profile')
    search_fields = ('contact_name', 'contact_phone_number', 'contact_relationship')

@admin.register(MentalHealth)
class MentalHealthAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'mood_swing', 'optimisim', 'euphoric', 'exhausted',
        'concentration', 'sexual_activity', 'aggressive_response',
        'suicidal_thoughts', 'authority_respect', 'sadness', 'prediction'
    )
    list_filter = ('mood_swing', 'optimisim', 'euphoric', 'exhausted', 'concentration', 'sexual_activity', 'aggressive_response', 'suicidal_thoughts', 'authority_respect', 'sadness')
    search_fields = ('user__username', 'user__email', 'prediction')
