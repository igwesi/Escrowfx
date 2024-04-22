from django.urls import path
from graphene_django.views import GraphQLView
from .views import *
from .schemas import schema

urlpatterns = [
    path("", GraphQLView.as_view(graphiql=True, schema=schema)),
    path('login/', UserLoginView.as_view(), name='login'),
    path('kyc/', UserKYC.as_view(), name='kyc'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('register/', UserRegistrationView.as_view(), name='register'),    
    
    path('token/refresh/', RefreshTokenView.as_view(), name='refreshToken'),
    path('password/change/', UserChangePassword.as_view(), name='changePassword'),
    path('password/reset/', SendPasswordResetEmailView.as_view(), name='reset-password'),
    path('password/reset/confirm/<uid>/<token>', UserPasswordResetView.as_view(), name='confirm_reset'),
]