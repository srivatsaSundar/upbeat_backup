from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import jwt
from django.conf import settings
from .models import User

class CustomTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')

        if not token:
            return None  # No token provided, return None

        try:
            # Assuming the token is in the format "Bearer <token>"
            token = token.split()[1]
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload['sub']
            user = User.objects.get(id=user_id)
            request.session['user_id'] = str(user.id)

        except (jwt.ExpiredSignatureError, jwt.DecodeError, User.DoesNotExist) as e:
            raise AuthenticationFailed('Invalid token')

        return (user, None) 

# Update settings.py
# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': (
#         'app.authentication.CustomTokenAuthentication',
#     ),
# }
