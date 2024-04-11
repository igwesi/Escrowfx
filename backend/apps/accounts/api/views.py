from rest_framework import status
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from django.contrib.auth import authenticate, login
from .renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (
    UserLoginSerializer,
    UserProfileSerializer,
    UserRegistrationSerializer, 
    UserPasswordResetSerializer,
    UserChangePasswordSerializer, 
    SendPasswordResetEmailSerializer, 
)

def get_tokens_for_user(user):
    # Generate User token manually
    refresh = RefreshToken.for_user(user)
    return {
        'refresh':str(refresh),
        'access':str(refresh.access_token)
    }

class UserRegistrationView(APIView):
    permission_classes  = [permissions.AllowAny]
    renderer_classes    = [UserRenderer]

    def get(self, request, format=None):
        return Response({"status": status.HTTP_200_OK, "msg": "API POST Request Only"}, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer  = UserRegistrationSerializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            user  = serializer.create()
            token = get_tokens_for_user(user)
            
            return Response({
                'token' : token,
                'msg'   : 'Registraion done!'},
                status=status.HTTP_201_CREATED)
        
        return Response({'msg':serializer.errors},status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    permission_classes  = [permissions.AllowAny]
    renderer_classes    = [UserRenderer]

    def get(self, request, format=None):
        status_code  = status.HTTP_200_OK
        # GET requests are typically used to retrieve data, not to log in.
        # If you want to provide a form or some other data, you should do it here.
        return Response({"status": status_code, "msg": "API POST Request Only"}, status=status_code)

    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            email       = serializer.data.get('email')
            password    = serializer.data.get('password')
            user        = authenticate(email=email, password=password)
                        
            if user is not None:
                token = get_tokens_for_user(user)        
                return Response({
                    'token'     : token,
                    'email'     : user.email,
                    'first_name': user.first_name,
                    'last_name' : user.last_name,
                    'msg'       : 'Logged in Successfully!'
                },status=status.HTTP_200_OK)
            return Response({'errors':{'non_field_errors':['Email or Password is Incorrect']}},status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)


class UserProfileView(APIView):
    renderer_classes    = [UserRenderer]
    permission_classes  = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        return Response({"user": serializer.data}, status=status.HTTP_200_OK)
    
    def post(self, request, format=None):
        serializer = UserProfileSerializer(request.user, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.update(instance=request.user, data=request.data)
            return Response({"user":serializer.data, "msg":"Profile Updated Successfully"}, status=status.HTTP_200_OK)
        return Response({"msg":"Not Updated"}, status=status.HTTP_502_BAD_GATEWAY)    
    


class UserChangePassword(APIView):
    renderer_classes    = [UserRenderer]
    permission_classes  = [permissions.IsAuthenticated]
    
    def get(self, request, format=None):
        # GET requests are typically used to retrieve data, not to log in.
        status_code  = status.HTTP_200_OK
        return Response({"status": status_code, "msg": "API POST Request Only"}, status=status_code)

    def post(self,request,format=None):
        serializer=UserChangePasswordSerializer(data=request.data, context={'user':request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password Changed Successfully'},status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)        


class SendPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password Reset Link Sent, Please Check Your Email'},status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        


class UserPasswordResetView(APIView):
    renderer_classes=[UserRenderer]
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, uid, token, format=None):
        serializer = UserPasswordResetSerializer(data=request.data, context={'uid':uid,'token':token})

        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password Reset Successfully'},status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)