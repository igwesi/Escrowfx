from rest_framework import status
from django import db
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from django.contrib.auth import authenticate, login
from .renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from apps.graph.views import Person, Business
from .serializers import (
    User,
    UserLoginSerializer,
    UserProfileSerializer,
    UpdateProfileSerializer,
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


class RefreshTokenView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request, format=None):
        refresh_token = request.data.get("refresh")
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                return Response(
                    {'access': str(token.access_token)},
                    status=status.HTTP_200_OK
                )
            except Exception as e:
                return Response(
                    {'error': str(e)}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(
            {'error': 'Refresh token not provided'}, 
            status=status.HTTP_400_BAD_REQUEST
        )


class UserRegistrationView(APIView):
    permission_classes  = [permissions.AllowAny]
    renderer_classes    = [UserRenderer]
    def get(self, request, format=None):
        return Response(
            {"status": status.HTTP_200_OK, "msg": "API POST Request Only"}, 
            status=status.HTTP_200_OK
        )

    def post(self, request, format=None):
        serializer  = UserRegistrationSerializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            user  = serializer.create(serializer.data)
            token = get_tokens_for_user(user)
            
            return Response({
                'token' : token,
                'msg'   : 'Registraion done!'},
                status=status.HTTP_201_CREATED
            )
        return Response(
            {'msg':serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )


class UserLoginView(APIView):
    permission_classes  = [permissions.AllowAny]
    renderer_classes    = [UserRenderer]
    
    def get(self, request, format=None):
        status_code  = status.HTTP_200_OK
        # GET requests are typically used to retrieve data, not to log in.
        # If you want to provide a form or some other data, you should do it here.
        return Response(
            {"status": status_code, "msg": "API POST Request Only"},
            status=status_code
        )

    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            email       = serializer.data.get('email')
            password    = serializer.data.get('password')
            user        = authenticate(email=email, password=password)
            
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({
                    'token'         : token,
                    'email'         : user.email,
                    'first_name'    : user.first_name,
                    'last_name'     : user.last_name,
                    'is_verified'   : user.is_verified,
                    'msg'       : 'Logged in Successfully!'
                },status=status.HTTP_200_OK)
            return Response(
                {'errors':{'non_field_errors':['Email or Password is Incorrect']}},
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)


class UserKYC(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        return Response({"user": serializer.data}, status=status.HTTP_200_OK)
    
    def post(self, request, format=None):
        user            = request.user
        data            = request.data
        
        person_payload = {
            'name_first'        : user.first_name,
            'name_last'         : user.last_name,
            'phone'             : user.get_tel(),
            'email'             : user.email,
            'dob'               : user.get_dob(),
            
            'id_type'           : data['id_type'],
            'id_number'         : data['id_number'],
            'id_country'        : data['id_country'],
            
            'address_line1'     : data['address_line'],
            'address_city'      : data['address_city'],
            'address_state'     : data['address_state'],
            'address_country'   : data['address_country'],
        }
        if data['id_upload']:
            person_payload['id_upload'] = data['id_upload']
        if data['bvn']:
            person_payload['bank_id_number'] = data['bvn']
        
        user_instance               = User.objects.get(email=user.email)
        user_instance.role          = data['role']
        user_instance.business_name = data['company_name']
        user_instance.address_line  = data['address_line']
        user_instance.city          = data['address_city']
        user_instance.state         = data['address_state']
        user_instance.country       = data['address_country']
        user_instance.zip_code      = data['address_zip']       
        user_instance.save()
        
        # try:
        #     person_response             = Person.create_person(person_payload)
        #     print(person_response)
        #     user_instance.person_id     = person_response[2]['id']
        #     user_instance.save()
        # except Exception as e:
        #     print(e)
            
        # try:
        #     dof             = data['dof'] 
        #     ein             = data['company_ein']
        #     industry        = data['industry']
        #     business_type   = data['business_type']
        #     business_payload = {
        #         'owner_id'          : user_instance.person_id,
        #         'name'              : user_instance.business_name,
        #         'business_type'     : business_type,
        #         'industry'          : industry,
        #         'id_type'           : 'ein',
        #         'id_number'         : ein,
                
        #         'address_line1'     : user_instance.address_line,
        #         'address_city'      : user_instance.city,
        #         'address_state'     : user_instance.state,
        #         'address_country'   : user_instance.country,
        #         'address_zip'       : user_instance.zip_code,
        #         'dof'               : dof
        #     }
        #     print(business_payload)
        #     business_response = Business.create_business(business_payload)
        # except Exception as e:
        #     print(e)
        
        return Response(
            {"status_code":status.HTTP_200_OK, "msg":"KYC has been submitted Successfully"}, 
            status=status.HTTP_200_OK
        )


class UserProfileView(APIView):
    renderer_classes    = [UserRenderer]
    permission_classes  = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        return Response({"user": serializer.data}, status=status.HTTP_200_OK)
    
    def post(self, request, format=None):
        serializer = UpdateProfileSerializer(request.user, data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            serializer.update(instance=request.user, validated_data=request.data)
            return Response(
                {
                    "status_code":status.HTTP_200_OK,
                    "user":serializer.data, 
                    "msg":"Profile Updated Successfully"
                }, 
                status=status.HTTP_200_OK
            )
        
        return Response(
            {"status_code":status.HTTP_502_BAD_GATEWAY, "msg":"Not Updated"}, 
            status=status.HTTP_502_BAD_GATEWAY
        )    
    

class UserChangePassword(APIView):
    renderer_classes    = [UserRenderer]
    permission_classes  = [permissions.IsAuthenticated]
    
    def get(self, request, format=None):
        # GET requests are typically used to retrieve data, not to log in.
        status_code  = status.HTTP_200_OK
        return Response(
            {"status": status_code, "msg": "API POST Request Only"},
            status=status_code
        )

    def post(self,request,format=None):
        serializer=UserChangePasswordSerializer(
            data=request.data, 
            context={'user':request.user}
        )
        if serializer.is_valid(raise_exception=True):
            return Response(
                {'msg':'Password Changed Successfully'},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)        


class SendPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data, context={'request': request})

        if serializer.is_valid(raise_exception=True):
            return Response(
                {'msg':'Password Reset Link Sent, Please Check Your Email'}, 
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        


class UserPasswordResetView(APIView):
    renderer_classes=[UserRenderer]
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, uid, token, format=None):
        print(uid, token)
        serializer = UserPasswordResetSerializer(
            data=request.data, 
            context={'uid':uid,'token':token}
        )
        
        if serializer.is_valid(raise_exception=True):
            return Response(
                {'msg':'Password Reset Successfully'},
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


