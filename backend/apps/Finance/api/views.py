from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from django.contrib.auth import get_user_model
from django.db.models import Q
from .serializers import Wallet, payoutLink, WalletSerializer, PayoutLinkSerializer
from apps.graph.views import Bank, Business
User = get_user_model()


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


class DashboardView(APIView):
    def get(self, request, format=None):
        try:
            user = User.objects.get(user_id=request.user.user_id)
        except User.DoesNotExist:
            return Response({"status": status.HTTP_404_NOT_FOUND, "msg": "User Not Found"}, status=status.HTTP_404_NOT_FOUND)
        
        usd_wallet  = Wallet.objects.get(owner=user).get_usd()
        ngn_wallet  = Wallet.objects.get(owner=user).get_ngn()
        business    = Business.get_business(user.business_id)
        
        data = {
            "business"   : business,
            "ngn_wallet" : ngn_wallet,
            "usd_wallet" : usd_wallet,
        }
        return Response({"status": status.HTTP_200_OK, "data":data,  "msg": "Successful"}, status=status.HTTP_200_OK)


class ListBank(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, format=None):
        data = Bank.list_banks()
        return Response({"status": status.HTTP_200_OK, "data":data,  "msg": "Successful"}, status=status.HTTP_200_OK)



class WalletView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, format=None):
        user = request.user
        currency = request.data.get('currency')
        
        if not Wallet.objects.filter(owner=user).exists():
            wallet = Wallet.objects.create(owner=user)
            wallet.create_wallet()
            wallet.save()
        else:
            wallet = Wallet.objects.get(owner=user)
            
        if currency == "USD":
            response = wallet.get_usd()
        else:
            response = wallet.get_ngn()
    
        return Response({
            "data"  : response,
            "wallet": response,
            "msg"   : "Successful"
        }, status=status.HTTP_200_OK)


class PayoutLink(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, format=None):
        user = request.user
        payout_id = request.data['payout_id']
        
        if not payoutLink.objects.filter(id=payout_id).exists():
            return Response({
                "status": "",
                "data": [],
                "payout_id": payout_id,
                "msg": "Payout with id {} does not exist".format(payout_id)
            }, status=status.HTTP_400_BAD_REQUEST)
        
        trade = payoutLink.objects.get(id=payout_id)
        if not trade.buyer == user and not trade.seller == user:
            return Response({
                "data": [],
                "payout_id": payout_id,
                "msg": "You're are not part of the trade"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = PayoutLinkSerializer(trade)
        return Response({
            "status": "",
            "data": serializer.data,
            "payout_id": payout_id,
            "msg": "Successful"
        }, status=status.HTTP_200_OK)
        
    def post(self, request, format=None):
        user = request.user
        data = request.data
        trade_option = data['trade_option'].upper()
        
        if trade_option == "BUYER":
            data['buyer'] = User.objects.get(user_id=user.user_id)
            data['buyer_approved'] = True
            
            if data['seller_email'] or data['seller_username']:
                data['seller'] = seller = User.objects.get(
                    Q(username=data['seller_username']) 
                    | Q(email=data['seller_email']))
                data['seller_username'] = seller.username
                data['seller_email'] = seller.email
        
        if trade_option == "SELLER":
            data['seller'] = seller = User.objects.get(
                user_id=user.user_id)
            data['seller_username'] = seller.username
            data['seller_email'] = seller.email
            data['seller_approved'] = True
        
        print(data)
        serializer = PayoutLinkSerializer(data=data)
        if not serializer.is_valid():
            return Response({
                "msg": serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response({
            "status": "",
            "data": serializer.data,
            "msg": "Successful"
        }, status=status.HTTP_200_OK)

class PayoutDestination(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, format=None):
        destination_id  = request.data['destination_id']
        response        = Bank.get_payout_destination(destination_id)
        return Response({
            "status": "",
            "data": response,
            "msg": "Successful"
        }, status=status.HTTP_200_OK)
    
    def post(self, request, format=None):
        data        = request.data
        response    = Bank.create_payout_destination(data)
        
        return Response({
            "status": "",
            "data":data,
        }, status=status.HTTP_200_OK)

class Payout(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, format=None):
        payout_id = request.data['payout_id']
        
        response = Bank.get_payout(payout_id)
        
        return Response({
            "status": "",
            "data": response,
            "payout_id": payout_id,
            "msg": "Successful"
        }, status=status.HTTP_200_OK)
    
    
    def post(self, request, format=None):
        data = request.data
        response = Bank.create_payout(data)

        return Response({
            "status": "",
            "data": data,
            "response": response,
        }, status=status.HTTP_200_OK)        
