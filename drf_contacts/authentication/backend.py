import jwt
from rest_framework import authentication, exceptions 
from django.conf import settings 
from django.contrib.auth.models import User

class JWTauthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        auth_data = authentication.get_authorization_header(request)

        if not auth_data:
            return None

        prefix, token = auth_data.decode("utf-8").split(' ')
        

        try:
            payload = jwt.decode(token, "JWT_SECRETE_KEYJWT_SECRETE_KEYJWT_SECRETE_KEY", algorithms=['HS256'])
            user = User.objects.get(username=payload['username'])
            return (user, token)

        except jwt.DecodeError: 
            raise exceptions.AuthenticationFailed(token)

        except jwt.ExpiredSignatureError: 
            raise exceptions.AuthenticationFailed('Your Token is Expired')

        return super().authenticate(request)