import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django_cryptography.fields import encrypt
from apps.graph.views import Bank
User = get_user_model()



class Wallet(models.Model):
    id              = models.UUIDField(primary_key=True, unique=True, editable=False)
    owner           = models.OneToOneField(User, on_delete=models.CASCADE)
    ngn_id          = encrypt(models.CharField(max_length=500, blank=True))
    usd_id          = encrypt(models.CharField(max_length=500, blank=True))    
    date_created    = models.DateField(auto_now_add=True)    
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.id = str(uuid.uuid4()).replace("-","")
        super().save(*args, **kwargs)
        
    def create_wallet(self):
        ngn = Bank.create_account(
            business_id = self.owner.business_id,
            type        = "virtual", 
            currency    = "NGN", 
            label       = "NGN Wallet"
        )
        usd = Bank.create_account(
            business_id = self.owner.business_id,
            type        = "checking",
            currency    = "USD",
            label       = "USD Wallet"
        )
        self.ngn_id = ngn['data']['id']
        self.usd_id = usd['data']['id']
        self.save()
        return self
    
    def get_usd(self):
        response = Bank.account_info(self.usd_id)
        return response
    
    def get_ngn(self):
        response = Bank.account_info(self.ngn_id)
        return response
        
    def __str__(self):
        return str(self.id)



class payoutLink(models.Model):
    id              = models.UUIDField(primary_key=True, unique=True, editable=False)
    buyer           = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name='buyer')
    seller          = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name='seller')
    
    buyer_currency  = models.CharField(max_length=20, choices=(
        ('NGN', 'NGN'),('USD', 'USD')))
    
    buyer_amount    = models.FloatField(default=0)
    
    seller_currency = models.CharField(max_length=20, choices=(
        ('NGN', 'NGN'), ('USD', 'USD')))
    seller_amount   = models.FloatField(default=0)
    
    
    seller_email    = models.EmailField(blank=True)
    seller_username = models.CharField(max_length=100, blank=True)
    
    buyer_approved  = models.BooleanField(default=False)
    seller_approved = models.BooleanField(default=False)
    
    status          = models.CharField(max_length=100, 
                        choices=(('Pending', 'Pending'),('Done', 'Done'), ('Approved', 'Approved')),
                        default='Pending')
    
    is_done         = models.BooleanField(default=False)
    
    
    seller_payout                       = models.CharField(max_length=500, blank=True, null=True)
    buyer_payout                        = models.CharField(max_length=500, blank=True, null=True)
    buyer_payout_destination            = models.CharField(max_length=500, blank=True, null=True)
    seller_payout_destination           = models.CharField(max_length=500, blank=True, null=True)
    date_created                        = models.DateField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Payout Links"
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.id = str(uuid.uuid4()).replace("-","")
        
        if not self.is_done:
            if self.buyer_approved and self.seller_approved and not self.is_done:
                # Initiate transaction and Post
                buyer_wallet   = Wallet.objects.get(owner=self.buyer)
                seller_wallet  = Wallet.objects.get(owner=self.seller)   
                
                buyer_account  = Bank.account_info(buyer_wallet.usd_id)
                seller_account = Bank.account_info(buyer_wallet.ngn_id)
                
                buyer_payload ={
                    "label"                 : buyer_account["account_label"],
                    "source_type"           : "bank_account",
                    "type"                  : "internal",
                    "destination_type"      : "bank_account",
                    "account_type"          : "person",                    
                }
                
                if self.buyer_currency == "USD":
                    buyer_payload["account_id"] = buyer_wallet.usd_id
                    buyer_payload["destination_account_id"] = seller_wallet.usd_id
                else:
                    buyer_payload["account_id"] = seller_wallet.ngn_id
                    buyer_payload["destination_account_id"] = buyer_wallet.ngn_id

                seller_payload = {
                    "label"                 : seller_account["account_label"],
                    "source_type"           : "bank_account",
                    "type"                  : "internal",
                    "destination_type"      : "bank_account",
                    "account_type"          : "person",
                }
                if not self.seller_currency == "USD":
                    seller_payload["account_id"] = seller_wallet.usd_id
                    seller_payload["destination_account_id"] = buyer_wallet.usd_id
                else:
                    seller_payload["account_id"] = seller_wallet.ngn_id
                    seller_payload["destination_account_id"] = buyer_wallet.ngn_id
                
    
                buyer_payout_destination        = Bank.create_payout_destination(buyer_payload)
                seller_payout_destination       = Bank.create_payout_destination(seller_payload)
                
                self.buyer_payout_destination   = buyer_payout_destination_id   = buyer_payout_destination[2]['id']
                self.seller_payout_destination  = seller_payout_destination_id  = seller_payout_destination[2]['id']
                
                buyer_payout                    = Bank.create_payout(buyer_payout_destination_id, float(self.buyer_amount)*100, "FX Payout")
                seller_payout                   = Bank.create_payout(seller_payout_destination_id, float(self.seller_amount)*100, "FX Payout")
                
                if buyer_payout[0] and seller_payout[0]:
                    self.buyer_payout               = buyer_payout[2]['id']
                    self.seller_payout              = seller_payout[2]['id']
                
                    self.status = 'Approved'
                    self.is_done = True
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.buyer)