from django.urls import path
from .views import *



urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path("rates", CurrencyRate.as_view(), name="rates"),
    path("bank/list/", ListBank.as_view(), name="list_bank"),
]