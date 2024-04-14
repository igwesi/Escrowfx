from django.shortcuts import render
from django.http import JsonResponse
from . import api
from .api import Bank
from .utils import load_lib

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
            'account_label'         : account[2]['label'],
            'holder_type'           : account[2]['holder_type'],
            'currency'              : account[2]['currency'],
            'balance'               : account[2]['balance'],
            'account_status'        : account[2]['status'],
            'routing_number'        : account[2]['routing_number'],
            'bank_name'             : account[2]['bank_name'],
            'bank_code'             : account[2]['bank_code'],
            'bank_address'          : account[2]['bank_address'],  
            'currency_settlement'   : account[2]['currency_settlement']
        }
        return account_info
    
    def get_transaction(data):
        transaction = graph_instance.get_transaction(data)
        return transaction
    
    def list_transaction(data):
        transactions = graph_instance.list_transactions(data)
        return transactions
    
    def mock_deposit(data):
        data = {
            "account_id"    : "95e2a1a1f45f11eeb8d20edcd86e5ab3",
            "amount"        : 100_000,
            "sender_name"   : "The Raven",
            "description"   : "Payment Test"
        }
        deposit = graph_instance.mock_deposit(data)
        return deposit

    def get_bank_info(data):
        bank = graph_instance.bank_info(data)
        return bank

    def list_banks():
        banks = graph_instance.list_banks()
        return banks
    
    def resolve_bank(data):
        data = {
            "currency"      : data["currency"],
            "bank_code"     : data['bank_code'],
            "account_number": data["account_number"],
        }
        bank = graph_instance.resolve_bank(data)
        return bank
    
    def create(data):
        account = graph_instance.create_account(data)
        return account
    
    def list_accounts(data):
        accounts = graph_instance.list_accounts(data)
        return accounts