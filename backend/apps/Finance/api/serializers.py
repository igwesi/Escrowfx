from rest_framework import serializers
from ..models import Wallet, payoutLink



class PayoutLinkSerializer(serializers.ModelSerializer):         
    class Meta:
        model = payoutLink
        fields = [
            'id',
            'buyer',
            'seller',
            'buyer_currency',
            'buyer_amount',
            'buyer_approved',
            
            'seller_currency',
            'seller_amount',
            'seller_email',
            'seller_username',
            'seller_approved',
            'status',
            'is_done',
        ]
    
    def create(self, validated_data):
        buyer = validated_data.get('buyer')
        seller = validated_data.get('seller')
        return payoutLink.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.buyer  = validated_data.get('buyer', instance.buyer)
        instance.seller = validated_data.get('seller', instance.seller)
        
        instance.buyer_currency = validated_data.get('buyer_currency', instance.buyer_currency)
        instance.seller_currency = validated_data.get('seller_currency', instance.seller_currency)
        
        instance.buyer_amount = validated_data.get('buyer_amount', instance.buyer_amount)
        instance.seller_amount = validated_data.get('seller_amount', instance.seller_amount)
        
        instance.seller_email = validated_data.get('seller_email', instance.seller_email)
        instance.seller_username = validated_data.get('seller_username', instance.seller_username)
        
        instance.buyer_approved = validated_data.get('buyer_approved', instance.buyer_approved)
        instance.seller_approved = validated_data.get('seller_approved', instance.seller_approved)
        
        instance.status = validated_data.get('status', instance.status)
        instance.is_done = validated_data.get('is_done', instance.is_done)
        
        instance.save()
        return instance


class WalletSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Wallet
        fields = [
            'id',
            'owner',
            'ngn_id',
            'usd_id',
        ]
    
    def create(self, validated_data):
        return Wallet.objects.create(**validated_data)
    
    
    def update(self, instance, validated_data):
        instance.owner    = validated_data.get('owner', instance.user)
        instance.ngn_id   = validated_data.get('ngn_id', instance.ngn_id)
        instance.usd_id   = validated_data.get('usd_id', instance.usd_id)
        
        instance.save()
        return instance