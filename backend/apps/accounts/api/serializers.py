from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.utils import http
from django.utils import encoding
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import authenticate, login
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import CommonPasswordValidator
from apps.accounts.api.utils import Utils


User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    """ Additional field for password confirmation """
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        """ Specify the model and fields to be serialized """
        model = User
        fields = [
            'email', 
            'username', 
            'tel', 
            'first_name', 
            'last_name', 
            'password', 
            'password2'
        ]
        
        """ Additional validation for unique fields """
        extra_kwargs = {
            'email': {'validators': [
                UniqueValidator(
                    queryset=User.objects.all(),
                    message="User with email already exist")]},
            'username': {'validators': [
                UniqueValidator(
                    queryset=User.objects.all(), 
                    message="User must provide a unique username")]},
            'tel': {'validators': [
                UniqueValidator(
                    queryset=User.objects.all(),
                    message="User with phone number already exist")]},
        }

    def validate(self, data):
        """ Validate that the two password fields match """
        password    = data.get('password')
        password2   = data.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")
        return data

    def create(self, validated_data):
        """ Create a new user with the provided data """
        user = User.objects.create_user(
            tel         = validated_data['tel'],
            email       = validated_data['email'],
            username    = validated_data['username'],
            password    = validated_data['password']
        )
        """ Set additional user fields """
        user.first_name      = validated_data['first_name']
        user.last_name       = validated_data['last_name']
        user.save()
        
        """" Return User Object"""
        return user



class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    class Meta:
        model   = User
        fields  = ['email','password']
        
    def validate(self, attrs):
        """ Retrieve email and password from the provided attributes """
        email       = attrs.get('email')
        password    = attrs.get('password')
        
        """ Check if both email and password are provided """
        if email and password:
            """ Attempt to authenticate the user with the provided email and password """
            user = authenticate(
                request=self.context.get('request'), 
                email=email, 
                password=password
            )
            
            """ If authentication fails, raise a validation error """
            if not user:
                raise serializers.ValidationError(
                    "Incorrect Credentials",
                    code='authorization'
                )
            
            """ Prepare email data for successful login """
            data = { 
                'user'       : user,
                'subject'    : 'Account Login Successfully',
                'body'       : 'Please check your email for login details.',
                'template'   : 'accounts/email/login_notification.html',
                'context'    : {'user':user}                
            }
            """ Send email notification for successful login """
            Utils.send_mail_threaded(data)
            
            """ Add the authenticated user to the attributes """
            attrs['user'] = user
        else:
            """ If either email or password is missing, raise a validation error """
            raise serializers.ValidationError("Both fields are required", code='authorization')
        return attrs
    
class UserKYCSerializer(serializers.ModelField):
    
    class Meta:
        model = User
        fields = ['business_name', 'role', 'address_line','city','state','zip_code', 'country']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model  = User
        fields = [
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
        
class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'dob',
            'business_name',
            'role',
            # LOCATION
            'address_line',
            'city',
            'state',
            'country',
            'zip_code',
        ]
    def update(self, instance, validated_data):
       """Update the instance with the validated data """
       instance.last_name      = validated_data['last_name']
       instance.first_name     = validated_data['first_name']
       instance.dob            = validated_data['dob']
       instance.business_name  = validated_data['business_name']
       instance.role           = validated_data['role']
       instance.address_line   = validated_data['address_line']
       instance.zip_code       = validated_data['zip_code']
       instance.city           = validated_data['city']
       instance.state          = validated_data['state']
       instance.country        = validated_data['country']      
       
       """ Save the updated instance """
       instance.save()
       return instance


class UserChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        max_length=255, style={'input_type': 'password'},
        write_only=True
    )
    new_password = serializers.CharField(
        max_length=255, style={'input_type': 'password'},
        write_only=True
    )
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
        user         = self.context.get('user')
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

    def validate(self, data):
        email   = data.get('email')
        request = self.context.get('request')
        if request:
            hostname = request.get_host()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            """ If the user does not exist, raise a validation error """
            raise serializers.ValidationError("You are not a registered user")
        
        """ Generate a password reset token """
        token   = PasswordResetTokenGenerator().make_token(user)
        uid     = urlsafe_base64_encode(encoding.force_bytes(user.user_id))
        
        """ Construct the password reset link """
        link    = f"https://{hostname}/api/user/password/reset/confirm/{uid}/{token}"

        """ Prepare email data """
        emaIl_data = { 
            'user'       : user,
            'subject'    : 'Request to Reset Your Password',
            'body'       : 'Follow the link below to reset Your Password',
            'template'   : 'accounts/email/reset_password_notification.html',
            'context'    : {'user':user, 'link':link, 'site_name':'Silicon'}                
        }
        """Send the password reset email"""
        Utils.send_mail_threaded(emaIl_data)
        return data



class UserPasswordResetSerializer(serializers.Serializer):
    """
    Serializer for resetting a user's password.
    This serializer validates the new password and confirm password fields, checks the token's validity,
    and updates the user's password if the token is valid.
    """
    new_password        = serializers.CharField(
        max_length=255,style={'input-type':'password'},
        write_only=True
    )
    confirm_new_password = serializers.CharField(
        max_length=255,style={'input-type':'password'},
        write_only=True
    )
    class Meta:
        fields=['new_password','confirm_new_password']
    
    def validate(self, data):
        """
        Validate the new password and confirm password fields, check the token's validity,
        and update the user's password if the token is valid.
        """
        password    = data.get('new_password')
        password2   = data.get('confirm_new_password')
        uid         = self.context.get('uid')
        token       = self.context.get('token')
        
        # Check if the new password and confirm password fields match
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't matched")
        
        # Decode the user ID from the uid
        try:
            id      = encoding.smart_str(urlsafe_base64_decode(uid))
            user    = User.objects.get(user_id=id)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError("Invalid or expired token")
        
        # Check if the token is valid
        if not PasswordResetTokenGenerator().check_token(user,token):
            raise serializers.ValidationError("Token is not Valid or Expired")

        # Update the user's password
        user.set_password(password)
        user.save()
        
        return data