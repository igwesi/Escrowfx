from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from django.contrib.auth import get_user_model
from ..models import BankAccount
from apps.graph.views import Bank, Person
User = get_user_model()

class DashboardView(APIView):
    def get(self, request, format=None):
        try:
            user = User.objects.get(user_id=request.user.user_id)
        except User.DoesNotExist:
            return Response({"status": status.HTTP_404_NOT_FOUND, "msg": "User Not Found"}, status=status.HTTP_404_NOT_FOUND)
        
        bank_instance, created = Bank.objects.get_or_create(owner=user)
        account_info = Bank.account_info(bank_instance.usd_id) # "95e2a1a1f45f11eeb8d20edcd86e5ab3"
        graph_person = Person.get_person(user.person_id) # "3a7c09328cb211ee9eff0edcd86e5ab3"
        data = [
            graph_person,
            account_info
        ]
        return Response({"status": status.HTTP_200_OK, "data":data,  "msg": "Successful"}, status=status.HTTP_200_OK)

class CurrencyRate(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, format=None):
        ticker = request.GET.get('ticker')
        rates = Bank.currency_rates()
        if not ticker:
            data = rates
        else:
            data = {
                ticker : rates[2][ticker]
                }
        return Response({"status": status.HTTP_200_OK, "data":data,  "msg": "Successful"}, status=status.HTTP_200_OK)
    
    
class ListBank(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        data = Bank.list_banks()
        return Response({"status": status.HTTP_200_OK, "data":data,  "msg": "Successful"}, status=status.HTTP_200_OK)