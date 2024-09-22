from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from .models import User, Profile, Doctor, EmergencyContact,MentalHealth
from .serializers import *
import pickle
import pandas as pd
import random
from together import Together

# User Signup
class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            return Response({"message": "User has been created"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# User Login
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = User.objects.filter(email=email).first()

            if user and user.check_password(password):
                token = user.generate_token()  # Assume User model has a generate_token method
                token_serializer = TokenSerializer(data={"access_token": token, "token_type": "bearer"})

                if token_serializer.is_valid():
                    return Response(token_serializer.data, status=status.HTTP_200_OK)
            
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

## Profile creation
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_profile(request):
    user_id = request.session.get('user_id')
    try:    
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = ProfileSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=user)
        return Response({"message": "Profile has been created"}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Doctor details creation
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_doctor(request):
    user_id = request.session.get('user_id')
    try:    
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
   
    profile = get_object_or_404(Profile, user=user)  # Get the profile associated with the user
    serializer = DoctorSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(profile=profile)  # Associate the doctor with the profile
        return Response({"message": "Doctor details have been created"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Emergency contact creation
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_emergency_contact(request):
    user_id = request.session.get('user_id')
    try:    
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    
    profile = get_object_or_404(Profile, user=user)  # Get the profile associated with the user
    serializer = EmergencyContactSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(profile=profile)  # Associate the emergency contact with the profile
        return Response({"message": "Emergency Contact details have been created"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Get current user details
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_details(request):
    user_id = request.session.get('user_id')
    try:    
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    
    user_data = {
        "id": str(user.id),
        "username": user.username,
        "email": user.email,
        "phone_number":user.phone_number,
    }
    return Response(user_data)

# Get profile details along with doctor and emergency contact
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile_details(request):
    user_id = request.session.get('user_id')
    try:    
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    
    profile = get_object_or_404(Profile, user=user)
    doctor = Doctor.objects.filter(profile=profile).first()
    emergency_contact = EmergencyContact.objects.filter(profile=profile).first()
    
    response_data = {
        "profile": ProfileSerializer(profile).data,
        "doctor": DoctorSerializer(doctor).data if doctor else None,
        "emergency_contact": EmergencyContactSerializer(emergency_contact).data if emergency_contact else None
    }
    return Response(response_data)



# model_file_path = 'app/best_model.pkl'
# with open(model_file_path, "rb") as file:
# loaded_model = pickle.load(open('app/best_model.pkl', 'rb'))

def custom_encode(value):
    label_mappings = {
        'mood_swing': {'NO': 0, 'YES': 1},
        'optimisim': {'1 From 10': 0, '2 From 10': 1, '3 From 10': 2, '4 From 10': 3, '5 From 10': 4, '6 From 10': 5, '7 From 10': 6, '8 From 10': 7, '9 From 10': 8},
        'euphoric': {'Seldom': 0, 'Most-Often': 1, 'Usually': 2, 'Sometimes': 3},
        'exhausted': {'Sometimes': 0, 'Usually': 1, 'Seldom': 2, 'Most-Often': 3},
        'concentration': {'1 From 10': 0, '2 From 10': 1, '3 From 10': 2, '4 From 10': 3, '5 From 10': 4, '6 From 10': 5, '7 From 10': 6, '8 From 10': 7, '9 From 10': 8},
        'sexual_activity': {'1 From 10': 0, '2 From 10': 1, '3 From 10': 2, '4 From 10': 3, '5 From 10': 4, '6 From 10': 5, '7 From 10': 6, '8 From 10': 7, '9 From 10': 8},
        'aggressive_response': {'NO': 0, 'YES': 1},
        'suicidal_thoughts': {'NO': 0, 'YES': 1},
        'authority_respect': {'NO': 0, 'YES': 1},
        'sadness': {'Usually': 0, 'Sometimes': 1, 'Seldom': 2, 'Most-Often': 3}
    }
    for col, mapping in label_mappings.items():
        if value in mapping:
            return mapping[value]
    return None

def encode_categorical_features(data):
    encoded_data = {}
    for column, value in data.items():
        encoded_value = custom_encode(value)
        if encoded_value is not None:
            encoded_data[column] = encoded_value
    return encoded_data

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mental_care(request):

    user_id = request.session.get('user_id')
    try:    
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = MentalHealthRequestSerializer(data=request.data)
    if serializer.is_valid():
        data_dict = serializer.validated_data
        encoded_data = encode_categorical_features(data_dict)
        encoded_df = pd.DataFrame([encoded_data])
        # predictions = loaded_model.predict(encoded_df)
        classes = ["Bipolar type 1", "Bipolar type 2", "Depression"]
        predictions=random.choice(classes)
        
        new_data = MentalHealth(
            user_id=user.id,
            mood_swing=data_dict['mood_swing'],
            optimisim=data_dict['optimisim'],
            euphoric=data_dict['euphoric'],
            exhausted=data_dict['exhausted'],
            concentration=data_dict['concentration'],
            sexual_activity=data_dict['sexual_activity'],
            aggressive_response=data_dict['aggressive_response'],
            suicidal_thoughts=data_dict['suicidal_thoughts'],
            authority_respect=data_dict['authority_respect'],
            sadness=data_dict['sadness'],
            prediction=predictions
        )
        new_data.save()

        return Response({"predictions": predictions[0]}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_mental_health_data(request):
    user_id = request.session.get('user_id')
    try:    
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    mental_health_data = MentalHealth.objects.filter(user_id=user.id).all()
    serializer = MentalHealthSerializer(mental_health_data, many=True)
    return Response(serializer.data)

# Delete profile and associated records
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_profile(request):
    user_id = request.session.get('user_id')
    try:    
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    
    profile = get_object_or_404(Profile, user=user)
    doctor = Doctor.objects.filter(profile=profile).first()
    emergency_contact = EmergencyContact.objects.filter(profile=profile).first()
    mental_health_data = MentalHealth.objects.filter(user_id=user.id).all()
    
    mental_health_data.delete()
    doctor.delete()
    emergency_contact.delete()
    profile.delete()
   
    return Response({"message": "Profile and associated records deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


client = Together(api_key="2eb1d5b8248409cc8509947d37fbcf0945c28d5bebbd6599feca1e0d41e912ed")

class ChatBotView(APIView):
    """
    This API view handles chatbot interaction. The client sends a query, and the chatbot
    responds with psychiatric advice.
    """

    def post(self, request):
        query = request.data.get('query', None)

        if query:
            try:
                # Make a request to the Together API for the chatbot completion
                response = client.chat.completions.create(
                    model="togethercomputer/llama-2-13b-chat",
                    max_tokens=100,
                    messages=[
                        {
                            "role": 'system',
                            "content": 'You are a psychiatrist. A patient would come to you and you should provide them advice based on the previous replies. Try to provide a solution based on their replies ',
                        },
                        {
                            "role": 'user',
                            "content": query,
                        },
                    ],
                )

                # Extract the chatbot's response
                bot_response = response.choices[0].message.content

                # Send the response back to the client
                return Response({"response": bot_response}, status=status.HTTP_200_OK)

            except Exception as e:
                # Handle any exceptions and return a 500 Internal Server Error
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # If no query was provided in the request
        return Response({"error": "No query provided"}, status=status.HTTP_400_BAD_REQUEST)