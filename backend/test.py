from requests import request
from django.http import HttpResponse

def my_view(request):
    hostname = request.get_host()
    return HttpResponse(f"Hostname: {hostname}")

my_view(request)