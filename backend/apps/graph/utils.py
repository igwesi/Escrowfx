import hmac
import hashlib
import requests
import importlib
from .import api


class GraphAPI(object):
    def __init__(self, django=True, **kwargs):
        if django:
            from .import settings
            self.access_key  = kwargs.get('GRAPH_ACCESS_KEY', settings.GRAPH_ACCESS_KEY)
            self.base_url    = kwargs.get('GRAPH_baseURL', settings.GRAPH_API_URL)
        else:
            for key, value in kwargs.items():
                setattr(self, key, value)
        
        self.bank_api       = api.Bank(self.make_request)
        self.business_api   = api.Business(self.make_request)
        self.person_api     = api.Person(self.make_request)
        self.wallet_api     = api.Wallet(self.make_request)
        self.usdt_api       = api.USDT(self.make_request)

    def make_request(self, method, path, **kwargs):
        options = {
            'GET': requests.get,
            'POST': requests.post,
            'PUT': requests.put,
            'PATCH': requests.patch,
            'DELETE': requests.delete,
        }
        url = "{}{}".format(self.base_url, path)
        headers = {
            "Authorization": "Bearer {}".format(self.access_key),
            'Content-Type': "application/json"
        }
        return options[method](url, headers=headers, **kwargs)
    
    
    # Person
    def create_person(self, data):
        return self.person_api.create_person(data)
    
    def person(self, person_id):
        return self.person_api.get_person(person_id)
    
    def list_persons(self, data):
        return self.person_api.list_persons(data)
    
    def upgrade_kyc(self, person_id, data):
        return self.person_api.upgrade_kyc(person_id, data)
    
    # BUSINESS OPERATION
    def create_business(self, data):
        return self.business_api.create_business(data)
    
    def business(self, business_id):
        return self.business_api.get_business(business_id)
    
    def list_businesses(self, data):
        return self.business_api.list_businesses(data)
    
    # BANK OPERATIONS
    def bank_rates(self):
        return self.bank_api.get_rate()
    
    def bank_info(self, data):
        return self.bank_api.get_bank(data)
    
    def list_banks(self):
        return self.bank_api.list_banks()
    
    def resolve_bank(self, data):
        return self.bank_api.resolve_bank(data)
    
    def create_account(self, data):
        return self.bank_api.create_account(data)
    
    def account_info(self, account_id):
        return self.bank_api.account_info(account_id)
    
    def list_accounts(self, data):
        return self.bank_api.list_accounts(data)
    
    def get_deposit(self, deposit_id):
        return self.bank_api.get_deposit(deposit_id)
    
    def list_deposits(self, data):
        return self.bank_api.list_deposits(data)
    
    def mock_deposit(self, data):
        return self.bank_api.mock_deposit(data)
    
    def create_payout_destination(self, data):
        return self.bank_api.create_payout_destination(data)
    
    def get_payout_destination(self, data):
        return self.bank_api.get_payout_destination(data)
    
    def list_payout_destination(self, data):
        return self.bank_api.list_payout_destination(data)
    
    def create_payout(self, data):
        return self.bank_api.create_payout(data)
    
    def get_payout(self, payout_id):
        return self.bank_api.get_payout(payout_id)
    
    def list_payout(self, data):
        return self.bank_api.list_payout(data)
    
    
    # CARD OPERATION
    def create_card(self, data):
        return self.bank_api.create_card(data)
    
    def get_card(self, card_id):
        return self.bank_api.get_card(card_id)
    
    def list_cards(self, data):
        return self.bank_api.list_cards(data)
    
    def fund_card(self, data):
        return self.bank_api.fund_card(data)
    
    def withdraw_card_funds(self, data):
        return self.bank_api.withdraw_card_funds(data)
    
    def freeze_card(self, card_id):
        return self.bank_api.freeze_card(card_id)
    
    def unfreeze_card(self, card_id):
        return self.bank_api.unfreeze_card(card_id)
    
    def delete_card(self, card_id):
        return self.bank_api.delete_card(card_id)
    
    def mock_card(self, data):
        return self.bank_api.mock_card(data)
    
    # TRANSACTION OPERATIONS
    def get_transaction(self, transaction_id):
        return self.bank_api.get_transaction(transaction_id)
    
    def list_transactions(self, data):
        return self.bank_api.list_transactions(data)
    
    def verify_transaction(self, method, **kwargs):
        return ""
    def verify_payment(self, code, **kwargs):
        return ""
    
    # WALLET OPERATION
    def create_wallet(self, data):
        return self.wallet_api.create_wallet(data)
    
    def get_wallet(self, wallet_id):
        return self.wallet_api.get_wallet(wallet_id)
    
    def list_wallets(self, data):
        return self.wallet_api.list_wallets(data)
    
    # USDT OPERATION
    def create_usdt_address(self, data):
        return self.usdt_api.create_address(data)
    
    def get_usdt_address(self, address_id):
        return self.usdt_api.get_address(address_id)
    
    def list_usdt_addresses(self, data):
        return self.usdt_api.list_addresses(data)



def load_lib(config=None):
    """
    """
    from . import settings
    config_lib = config or settings.GRAPH_LIB_MODULE
    module = importlib.import_module(config_lib)
    return module.GraphAPI

def generate_digest(data):
    from . import settings
    return hmac.new(
        settings.GRAPH_ACCESS_KEY.encode("utf-8"),
        msg = data,
        digestmod = hashlib.sha512).hexdigest()


class MockRequest(object):
    def __init__(self, response, **kwargs):
        self.response = response
        self.overwrite = True
        if kwargs.get('overwrite'):
            self.overwrite = True
        self.status_code = kwargs.get('status_code', 200)
        
    @classmethod
    def raise_for_status(cls):
        pass
    
    def json(self):
        if self.overwrite:
            return self.response
        return {'data': self.response}