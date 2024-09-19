import uuid
import bcrypt
import jwt
from datetime import datetime, timedelta
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings

# User Manager for custom User model
class UserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None):
        if not username:
            raise ValueError("Users must have a username")
        if email:
            email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.is_admin = False  # Regular users are not admins
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None):
        user = self.create_user(username, email, password)
        user.is_admin = True  # Superusers will be admins
        user.save(using=self._db)
        return user

# User Model
class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    hashed_password = models.CharField(max_length=255)
    is_admin = models.BooleanField(default=False)  # Field to distinguish superuser from regular users
    
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def set_password(self, password):
        self.hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.hashed_password.encode('utf-8'))

    def generate_token(self):
        expiration = datetime.now() + timedelta(hours=24)
        payload = {
            "sub": str(self.id),
            "exp": expiration
        }
        return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

    @property
    def is_staff(self):
        # Custom property for admin status; required by Django admin
        return self.is_admin

# Profile Model
class Profile(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    
    APPOINTMENT_FREQUENCY_CHOICES = [
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dob = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    appointment_frequency = models.CharField(max_length=10, choices=APPOINTMENT_FREQUENCY_CHOICES)
    test_timing = models.TimeField()

    def __str__(self):
        return f"{self.user.username}'s Profile"

# Doctor Model
class Doctor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='doctors')
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    clinic_or_hospital_name = models.CharField(max_length=255)
    email = models.EmailField()

    def __str__(self):
        return self.name

# EmergencyContact Model
class EmergencyContact(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='emergency_contacts')
    contact_name = models.CharField(max_length=255)
    contact_phone_number = models.CharField(max_length=15)
    contact_relationship = models.CharField(max_length=50)

    def __str__(self):
        return f"Emergency Contact for {self.profile.user.username}"

# MentalHealth Model
class MentalHealth(models.Model):
    MOOD_CHOICES = [
        ('NO', 'No'),
        ('YES', 'Yes'),
    ]
    
    SCORE_CHOICES = [
        ('1 From 10', '1 From 10'),
        ('2 From 10', '2 From 10'),
        ('3 From 10', '3 From 10'),
        ('4 From 10', '4 From 10'),
        ('5 From 10', '5 From 10'),
        ('6 From 10', '6 From 10'),
        ('7 From 10', '7 From 10'),
        ('8 From 10', '8 From 10'),
        ('9 From 10', '9 From 10'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mood_swing = models.CharField(max_length=3, choices=MOOD_CHOICES)
    optimisim = models.CharField(max_length=20, choices=SCORE_CHOICES)
    euphoric = models.CharField(max_length=20, choices=[
        ('Seldom', 'Seldom'),
        ('Most-Often', 'Most-Often'),
        ('Usually', 'Usually'),
        ('Sometimes', 'Sometimes'),
    ])
    exhausted = models.CharField(max_length=20, choices=[
        ('Seldom', 'Seldom'),
        ('Usually', 'Usually'),
        ('Most-Often', 'Most-Often'),
        ('Sometimes', 'Sometimes'),
    ])
    concentration = models.CharField(max_length=20, choices=SCORE_CHOICES)
    sexual_activity = models.CharField(max_length=20, choices=SCORE_CHOICES)
    aggressive_response = models.CharField(max_length=3, choices=MOOD_CHOICES)
    suicidal_thoughts = models.CharField(max_length=3, choices=MOOD_CHOICES)
    authority_respect = models.CharField(max_length=3, choices=MOOD_CHOICES)
    sadness = models.CharField(max_length=20, choices=[
        ('Seldom', 'Seldom'),
        ('Usually', 'Usually'),
        ('Most-Often', 'Most-Often'),
        ('Sometimes', 'Sometimes'),
    ])
    prediction = models.TextField()

    def __str__(self):
        return f"Mental Health Data for {self.user.username}"