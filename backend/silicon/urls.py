from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/user/', include('accounts.api.urls')),
    path('admin/', admin.site.urls),
]
