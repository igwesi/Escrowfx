from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def api(request):
    return JsonResponse({'msg': 'API LIVE', 'status': 200})

urlpatterns = [
    path('', api, name="api"),
    path('api/user/', include('apps.accounts.api.urls')),
    path('api/finance/', include('apps.Finance.api.urls')),
    path('api/chat/', include('apps.chat.urls')),
    path('admin/', admin.site.urls),
    path('health/', include('health_check.urls'))
]
