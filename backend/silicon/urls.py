from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/user/', include('apps.accounts.api.urls')),
    path('api/finance/', include('apps.Finance.api.urls')),
    path('api/chat/', include('apps.chat.urls')),
    path('admin/', admin.site.urls),
    path('health/', include('health_check.urls'))
]
