import json
from . import api
from .api import Bank
from .utils import load_lib

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


GraphAPI = load_lib()
graph_instance = GraphAPI()


def graph(request):
    rates = graph_instance.bank_rates()
    data = {
        "status"  : rates[0],
        "message" : rates[1],
        "ngn_usd" : rates[2]['NGN-USD'],
        "usd_ngn" : rates[2]['USD-NGN']
    }
    return JsonResponse(data, safe=False)


class Person():
    def __init__(self):
        self.person = Person()
    
    def create_person(data):
        data["id_level"]    = "primary"
        data["id_type"]     = "passport"
        data["kyc_level"]   = "basic"
        person = graph_instance.create_person(data)
        return person
    
    def get_person(person_id):
        person = graph_instance.person(person_id)
        return person
    
    def list_persons(data):
        persons = graph_instance.list_persons(data)
        return persons
    
    def upgrade_kyc(person_id, data):
        person = graph_instance.upgrade_kyc(person_id, data)
        return person


class Business():
    def __init__(self):
        self.business = Business()
    
    def create_business(data):
        business = graph_instance.create_business(data)
        return business
    
    def get_business(business_id):
        response = graph_instance.business(business_id)
        response = response[0]
        business = {
            "id"            : response["id"],
            "owner_id"      : response['owner_id'],
            "name"          : response['name'],
            "business_type" : response['business_type'],
            "industry"      : response['industry'],
            "dof"           : response['dof'],
            "is_master"     : response['is_master'],
            "id_type"       : response['id_type'],
            "id_number"     : response['id_number'],
            "address_line1" : response['address_line1'],
            "address_city"  : response['address_city'],
            "address_state"     : response['address_state'],
            "address_country"   : response['address_country'],
            "address_zip"       : response['address_zip'],
            "status"        : response['status'],
            "kyb_status"    : response['kyb_status'],
            "is_deleted"    : response['is_deleted'],
        }
        return business
    
    def list_businesses(data):
        businesses = graph_instance.list_businesses(data)
        return businesses


class Bank():
    def __init__(self):
        self.bank = Bank()
        
    def currency_rates():
        rates  = graph_instance.bank_rates()
        return rates

    def account_info(account_id):
        account = graph_instance.account_info(account_id)
        if account[0] != "success":
            return None
        
        account_info = {
            'account_type'          : account[2]['type'],            
            'account_name'          : account[2]['account_name'],
            'account_number'        : account[2]['account_number'],
            'balance'               : account[2]['balance'],
            'account_label'         : account[2]['label'],
            'holder_type'           : account[2]['holder_type'],
            'currency'              : account[2]['currency'],
            'account_status'        : account[2]['status'],
            'bank_name'             : account[2]['bank_name'],
        }
        
        if account[2]['currency'] == "NGN":
            account_info['bank_code']    = account[2]['bank_code']
            
        if account[2]['currency'] == "USD":
            account_info['bank_address']    = account[2]['bank_address'] 
            account_info['routing_number']  = account[2]['routing_number']
        
        account_info['currency_settlement'] = account[2]['currency_settlement']
        
        return account_info
    
    
    def create_payout_destination(data):
        destination = graph_instance.create_payout_destination(data)
        return destination
    
    def get_payout_destination(data):
        destination = graph_instance.get_payout_destination(data)
        return destination
    
    def list_payout_destination(data):
        destinations = graph_instance.list_payout_destination(data)
        return destinations
    
    def create_payout(destination_id, amount, description):
        payload = {
            "destination_id":destination_id,
            "amount":  float(amount*100),
            "description":description
        }
        payout = graph_instance.create_payout(payload)
        return payout
    
    def get_payout(data):
        payout = graph_instance.get_payout(data)
        return payout
    
    def list_payout(data):
        payouts = graph_instance.list_payout(data)
        return payouts
    
    def get_transaction(data):
        transaction = graph_instance.get_transaction(data)
        return transaction
    
    def list_transaction(data):
        transactions = graph_instance.list_transactions(data)
        return transactions
    
    
    
    def mock_deposit(account_id, amount, sender_name, description):
        payload = {
            "account_id"    : account_id,
            "amount"        : float(amount*100),
            "sender_name"   : sender_name,
            "description"   : description
        }
        deposit = graph_instance.mock_deposit(payload)
        return deposit

    def get_bank_info(routing_type, routing_number):
        payload = {
            "routing_type":routing_type,
            "routing_number":routing_number
        }
        bank = graph_instance.bank_info(payload)
        return bank

    def list_banks():
        banks = graph_instance.list_banks()
        return banks
    
    def resolve_bank(currency, bank_code, account_number):
        data = {
            "currency"      : currency,
            "bank_code"     : bank_code,
            "account_number": account_number,
        }
        bank = graph_instance.resolve_bank(data)
        return bank
    
    def create_account(business_id, type, currency, label):
        payload = {
            "business_id": business_id,
            "type": "business_{}".format(type),
            "currency": str(currency.uppercase()),
            "label": label,
            "autosweep_enabled": False
        }
        account = graph_instance.create_account(payload)
        return account
    
    def list_accounts(data):
        accounts = graph_instance.list_accounts(data)
        return accounts
    
    





@csrf_exempt
@require_POST
def webhook_view(request):
    data = json.loads(request.body)
    return HttpResponse(status=200)