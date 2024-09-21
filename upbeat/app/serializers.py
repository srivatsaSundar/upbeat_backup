from rest_framework import serializers
from .models import User, Profile, Doctor, EmergencyContact, MentalHealth

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone_number']

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'hashed_password']

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            phone_number=validated_data['phone_number']
        )
        user.set_password(validated_data['hashed_password'])
        user.save()
        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class TokenSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    token_type = serializers.CharField()

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['dob', 'gender', 'appointment_frequency', 'test_timing']


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['name', 'phone_number', 'clinic_or_hospital_name', 'email']


class EmergencyContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyContact
        fields = ['contact_name', 'contact_phone_number', 'contact_relationship']


class MentalHealthSerializer(serializers.ModelSerializer):
    class Meta:
        model = MentalHealth
        fields = ['mood_swing','optimisim','euphoric','exhausted','concentration','sexual_activity','aggressive_response','suicidal_thoughts','authority_respect','sadness','prediction']

class MentalHealthRequestSerializer(serializers.Serializer):
    mood_swing = serializers.ChoiceField(choices=[('NO', 'No'), ('YES', 'Yes')])
    
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
    
    optimisim = serializers.ChoiceField(choices=SCORE_CHOICES)
    euphoric = serializers.ChoiceField(choices=[('Seldom', 'Seldom'), ('Most-Often', 'Most Often'), ('Usually', 'Usually'), ('Sometimes', 'Sometimes')])
    exhausted = serializers.ChoiceField(choices=[('Seldom', 'Seldom'), ('Most-Often', 'Most Often'), ('Usually', 'Usually'), ('Sometimes', 'Sometimes')])
    concentration = serializers.ChoiceField(choices=SCORE_CHOICES)
    sexual_activity = serializers.ChoiceField(choices=SCORE_CHOICES)
    aggressive_response = serializers.ChoiceField(choices=[('NO', 'No'), ('YES', 'Yes')])
    suicidal_thoughts = serializers.ChoiceField(choices=[('NO', 'No'), ('YES', 'Yes')])
    authority_respect = serializers.ChoiceField(choices=[('NO', 'No'), ('YES', 'Yes')])
    sadness = serializers.ChoiceField(choices=[('Seldom', 'Seldom'), ('Most-Often', 'Most Often'), ('Usually', 'Usually'), ('Sometimes', 'Sometimes')])
