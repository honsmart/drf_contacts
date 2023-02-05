from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializers import UserSerializers
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings 
from django.contrib import auth
import jwt

# Create your views here.
class RegisterView(GenericAPIView):
    serializer_class = UserSerializers

    def post(self, request):
        serializer=UserSerializers(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LoginView(GenericAPIView):
    def post(self, request):
        data = request.data
        username = data.get("username", "")
        password = data.get("password", "")

        user = auth.authenticate(username=username,password=password)

        if user: 
            auth_token  = jwt.encode({'username': user.username},  "JWT_SECRETE_KEYJWT_SECRETE_KEYJWT_SECRETE_KEY")

            serializer = UserSerializers(user)
            data = {
                "user": serializer.data,
                "token": auth_token
            }

            return Response(data, status=status.HTTP_200_OK)

        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
