from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.utils import http
from django.utils import encoding
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import authenticate, login
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import CommonPasswordValidator
from apps.accounts.api.utils import Utils


User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'business_name','role', 'email', 'username', 'tel', 'address_line', 'city', 'state', 'zip_code', 'country', 'password', 'password2']
        extra_kwargs = {
            'email': {'validators': [UniqueValidator(queryset=User.objects.all(), message="User with email already exist")]},
            'username': {'validators': [UniqueValidator(queryset=User.objects.all(), message="User must provide a unique username")]},
            'business_name': {'validators': [UniqueValidator(queryset=User.objects.all(), message="Business name already registered")]},
            'tel': {'validators': [UniqueValidator(queryset=User.objects.all(), message="User with phone number already exist")]},
            'password': {'write_only': True},
            'password2': {'write_only': True},
        }

    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            first_name      = validated_data['first_name'],
            last_name       = validated_data['last_name'],
            business_name   = validated_data['business_name'],
            role            = validated_data['role'],
            
            username        = validated_data['username'],
            email           = validated_data['email'],
            tel             = validated_data['tel'],
            
            address_line    = validated_data['address_line'],
            city            = validated_data['city'],
            state           = validated_data['state'],
            zip_code        = validated_data['zip_code'],
            country         = validated_data['country'],
            
            password        = validated_data['password']
        )
        data = {
            "subject"   :   "Account Created Successfully",
            "body"      :   f"Hello {user.last_name} {user.first_name}, We are glad to serve you.",
            "to_email"  :   user.email
        }
        Utils.send_mail(data)
        return user


class UserLoginSerializer(serializers.ModelSerializer):
    email   = serializers.EmailField()
    class Meta:
        model   = User
        fields  = ['email','password']

    def validate(self, attrs):
        email       = attrs.get('email')
        password    = attrs.get('password')
        
        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)
            
            if not user:
                raise serializers.ValidationError("Incorrect Credentials", code='authorization')
            
            data = {
                'subject'    : "Account Login Successfully",
                'body'       : f"Hello {user.last_name} {user.first_name}, Welcome back",
                'to_email'   : user.email,
            }
            Utils.send_mail_threaded(data)
            attrs['user'] = user
        else:
            raise serializers.ValidationError("Both fields are required", code='authorization')
        return attrs
    

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model   = User
        fields  = [
            'email',            
            'tel',
            'username',
            'first_name',
            'last_name',
            'dob',
            
            'business_name',
            'role',
            
            # LOCATION
            'address_line',
            'city',
            'state',
            'zip_code',
            'country'
        ]
    
    def update(self, instance, validated_data):
        instance.email          = validated_data.get('email', instance.email)
        instance.tel          = validated_data.get('tel', instance.tel)
        instance.username       = validated_data.get('username', instance.username)
        instance.last_name      = validated_data.get('last_name', instance.last_name)
        instance.first_name     = validated_data.get('first_name', instance.first_name)
        instance.dob            = validated_data.get('dob', instance.dob)
        
        instance.business_name  = validated_data.get('business_name', instance.business_name)
        instance.role           = validated_data.get('role', instance.role)
        
        instance.zip_code       = validated_data.get('zip_code', instance.zip_code)
        instance.address_line   = validated_data.get('address_line', instance.address_line)
        instance.city           = validated_data.get('city', instance.city)
        instance.state          = validated_data.get('state', instance.state)
        instance.country        = validated_data.get('country', instance.country)
        
        instance.password       = validated_data.get('password', instance.password)
        instance.save()
        
        return instance


class UserChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    new_password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    confirm_new_password = serializers.CharField(
        max_length=255, 
        style={'input_type': 'password'}, 
        write_only=True, 
        validators=[CommonPasswordValidator]
    )

    class Meta:
        fields = ['old_password', 'new_password', 'confirm_new_password']

    def validate(self, data):
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        user = self.context.get('user')

        if not user.check_password(old_password):
            raise serializers.ValidationError("Old Password is not Correct")

        return data

    def save(self, **kwargs):
        user = self.context.get('user')
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


class SendPasswordResetEmailSerializer(serializers.Serializer):
    email=serializers.EmailField()
    class Meta:
        fields=['email']

    def validate(self, attrs):
        email   = attrs.get('email')
        
        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            raise serializers.ValidationError("You are not a registered user")
        
        user    = User.objects.get(email=email)
        uid     = http.urlsafe_base64_encode(encoding.force_bytes(user.user_id))
        token   = PasswordResetTokenGenerator().make_token(user)
        link    = "http://localhost:8000/api/user/reset-password/"+uid+'/'+token
        data    = {
            "subject"   :   "Reset Your Password",
            "body"      :   f"{user.last_name} {user.first_name}, Click the following link to reset Your Password: {link}",
            "to_email"  :   user.email
        }
        Utils.send_mail(data)
        return attrs



class UserPasswordResetSerializer(serializers.Serializer):
    new_password            = serializers.CharField(max_length=255,style={'input-type':'password'},write_only=True)
    confirm_new_password    = serializers.CharField(max_length=255,style={'input-type':'password'},write_only=True)
    
    class Meta:
        fields=['new_password','confirm_new_password']
    
    def validate(self,data):
        # try:
        password    = data.get('new_password')
        password2   = data.get('confirm_new_password')
        uid         = self.context.get('uid')
        token       = self.context.get('token')

        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't matched")
        try:
            id      = encoding.smart_str(http.urlsafe_base64_decode(uid))
            user    = User.objects.get(id=id)
        except (TypeError, ValueError, OverflowError, ObjectDoesNotExist):
            raise serializers.ValidationError("Invalid or expired token")

        if not PasswordResetTokenGenerator().check_token(user,token):
            raise serializers.ValidationError("Token is not Valid or Expired")
        
        user.set_password(password)
        user.save()
        return data