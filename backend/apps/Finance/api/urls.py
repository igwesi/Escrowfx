from django.urls import path
from .views import *



urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path("ngn/", WalletView.as_view(), name="ngn_wallet"),
    path("usd/", WalletView.as_view(), name="ngn_wallet"),
    
    path("rates", CurrencyRate.as_view(), name="rates"),
    path("bank/list/", ListBank.as_view(), name="list_bank"),
    
    path('payout/', PayoutLink.as_view(), name="payout_link"),
    path('payout/<str:payout_id>/', PayoutLink.as_view(), name="get_payout_link"),
    
    path('transaction/payout/', Payout.as_view(), name="payout"),

    path("transaction/nip/payout/", PayoutDestination.as_view(), name='nip_payout_destination'),
    path("transaction/wire/payout/", PayoutDestination.as_view(), name='wire_payout_destination'),
    path("transaction/internal/payout/", PayoutDestination.as_view(), name='create_payout_destination'),   
]