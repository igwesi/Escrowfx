
class BaseClass(object):
    def __init__(self, make_request):
        self.make_request = make_request
        
    def result_format(self, response, callback=None):
        if response.status_code >= 400:
            result = response.json()
            return result['status'], result['message']
        
        result = response.json()
        if callback:
            return callback(result)
        return result['status'], result['message'], result['data']
    

class Person(BaseClass):
    def create_person(self, data):
        path = "/person"
        response = self.make_request('POST', path, json=data)
        if response.status_code >= 400:
            return None
        return response.json()['data']
    
    def get_person(self, person_id):
        path = "/person/{}".format(person_id)
        # USAGE
            #response = Person.get_person(person_id)
        return self.result_format(self.make_request('GET', path))
    
    def list_persons(self, data):
        path = "/person?page={}&per_page={}".format(data['page'], data['pageSize'])
        
        response = self.make_request('GET', path)
        if response.status_code >= 400:
            return None
        # USAGE
            # payload = {'page': page,'pageSize': pageSize}
            # response = Person.list_persons(data=payload)
        #
        return self.result_format(response)
    
    def upgrade_kyc(self, person_id, data):
        path = "/person/{}/kyc".format(person_id)
        
        response = self.make_request('PATCH', path, json=data)
        if response.status_code >= 400:
            return None
        
        #USAGE
            # response = Person.upgrade_kyc(person_id, data=payload)
        return self.result_format(response)
    

class Business(BaseClass):
    def create_business(self, data):
        path = "/business"
        response = self.make_request('POST', path, json=data)
        if response.status_code >= 400:
            return None
        return response.json()['data']
    
    def get_business(self, business_id):
        path = f"/business/{business_id}"
        response = self.make_request('GET', path)
        if response.status_code >= 400:
            return None
        return response.json()['data']
    
    def list_businesses(self, data):
        path = "/business?page={}&per_page={}".format(data['page'], data['pageSize'])
        response = self.make_request('GET', path)
        if response.status_code >= 400:
            return None
        return response.json()['data']



class Bank(BaseClass):
    """
        Access up-to-date exchange rates for various currency pairs
        With the Rates API, you can:
        * Quickly retrieve current exchange rates.
        * Seamlessly integrate rate data into your applications.
        * Stay informed about fluctuations in currency values.
        * Enhance your financial products and services with precision
        Whether you're an e-commerce platform, financial app, or global business, 
        our Rates API provides you with accurate and real-time exchange rate data to streamline your financial operations.
    """
    def get_rate(self):
        path = "/rate"
        response = self.make_request("GET", path)
        return self.result_format(response)
    
    def get_bank(self, data):
        routing_type = data['routing_type'], 
        routing_number = data['routing_number']
        path = "/bank/resolve?routing_type={}&routing_number={}".format(routing_type, routing_number)
        response = self.make_request("GET", path)
        return self.result_format(response)
    
    def list_banks(self):
        path = "/bank"
        response = self.make_request("GET", path)
        return self.result_format(response)
    
    def resolve_bank(self, data):
        path = "/bank/resolve/account"
        response = self.make_request("POST", path, json=data)
        return self.result_format(response)
    

    def create_account(self, data):
        """Create a new bank account for the authenticated user/business"""
        path = "/bank_account"
        response = self.make_request("POST", path, json=data)
        return self.result_format(response)
    
    def account_info(self, account_id):
        path = "/bank_account/{}".format(account_id)
        response = self.make_request('GET', path)
        return self.result_format(response)
    
    def list_accounts(self, data):
        path = "/bank_account?page={}&per_page={}&from={}&to={}&settlement_currency={}&currency={}&label={}&status={}&provider={}&kind={}&type={}&holder_type={}".format(
            data['page'], data['pageSize'],
            data['from'], data['to'],
            data['settlement_currency'],
            data['currency'],
            data['label'],
            data['status'],
            data['provider'],
            data['kind'],
            data['type'],
            data['holder_type'],
        )
        response = self.make_request('GET', path)
        return self.result_format(response)
    
    def get_deposit(self, deposit_id):
        path = "/deposit/{}".format(deposit_id)
        response = self.make_request("GET", path)
        return self.result_format(response)
    
    def list_deposits(self, data):
        path = "deposit?page={}&per_page={}".format(
            data['page'], data['pageSize']
        )
        response = self.make_request("GET", path)
        return self.result_format(response)
    
    def mock_deposit(self, data):
        path = "/deposit/mock"
        response = self.make_request("PUT", path, json=data)
        return self.result_format(response)
    
    
    def create_payout_destination(self, data):
        pass
    
    def get_payout_destination(self, data):
        pass
    
    def list_payout_destination(self, data):
        pass
    
    def create_payout(self, data):
        path = "/payout"
        response = self.make_request("POST", path, json=data)
        return self.result_format(response)
    
    def get_payout(self, payout_id):
        path = "/payout/{}".format(payout_id)
        response = self.make_request("GET", path)
        return self.result_format(response)
    
    def list_payout(self, data):
        path = "/payout?page={}&per_page={}".format(
            data['page'], data['pageSize']
        )
        response = self.make_request("GET", path)
        return self.result_format(response)    
    
    
    def create_card(self, data):
        path = "/card"
        response = self.make_request("POST", path, json=data)
        return self.result_format(response)
    
    def get_card(self, card_id):
        path = "/card/{}?decrypt=false".format(card_id)
        response = self.make_request("GET", path)
        return self.result_format(response)
    
    def list_cards(self, data):
        path = "/card?page={}&per_page={}".format(
            data['page'], data['pageSize']
        )
        response = self.make_request("GET", path)
        return self.result_format(response)
    
    def fund_card(self, data):
        path = "/card/fund"
        response = self.make_request("POST", path, json=data)
        return self.result_format(response)
    
    def withdraw_card_funds(self, data):
        path = "/card/withdraw"
        
        response = self.make_request("POST", path, json=data)
        return self.result_format(response)
    
    def get_transaction(self, transaction_id):
        path = "/transaction/{}".format(transaction_id)
        response = self.make_request("GET", path)
        return self.result_format(response)
    
    def list_transactions(self, data):
        path = "/transaction?page={}&per_page={}&from={}&to={}&status={}&currency={}&account_id={}&card_id={}&linked_transaction_id={}&asc=false".format(
            data['page'], data['pageSize'], 
            data['from'], data['to'],
            data['status'], data['currency'], 
            data['account_id'], data['card_id'], data['linked_transaction_id'],
        )
        response = self.make_request("GET", path)
        return self.result_format(response)
    
    
    def freeze_card(self, card_id):
        path = "/card/{}".format(card_id)
        payload = {"status":"inactive"}
        response = self.make_request("PATCH", path, json=payload)
        return self.result_format(response)
    
    def unfreeze_card(self, card_id):
        path = "/card/{}".format(card_id)
        payload = {"status":"active"}
        response = self.make_request("PATCH", path, json=payload)
        return self.result_format(response)
    
    def delete_card(self, card_id):
        path = "/card/{}".format(card_id)
        response = self.make_request("DELETE", path)
        return self.result_format(response)
    
    def mock_card(self, data):
        """ This endpoint is only available on the sandbox environment """
        path = "/card/mock"
        response = self.make_request("PUT", path, json=data)
        return self.result_format(response)


class USDT(BaseClass):
    def create_address(self, data):
        path = "/address"
        data = {
            "currency": "USDT",
            "network": "ERC20",
            "label": "",
        }
        response = self.make_request("POST", path, json=data)
        if response.status_code >= 400:
            return None
        
        return self.result_format(response)
    
    def get_address(self, address_id):
        """Get information about a specific USDT address."""
        path = "/address/address_id"
        
        response = self.make_request('GET', path)
        if response.status_code >= 400:
            return None
        return self.result_format(response)
    
    
    def list_addresses(self, data):
        """
        OTHER PARAMETERS 
            from
            to
            holder_type : person, business
            currency: NGN, USD
            status: active, inactive
        """
        path = "/address?page{}&per_page={}".format(data['page'], data['pageSize'])
        response = self.make_request("GET", path)
        
        if response.status_code >= 400:
            return None
        
        return self.result_format(response)      

class Wallet(BaseClass):
    
    def create_wallet(self, data):
        path = "/bank_account"
        response = self.make_request("POST", path, json=data)
        return self.result_format(response)
        
    def get_wallet(self, wallet_id):
        path = "/wallet_account/{}".format(wallet_id)
        response = self.make_request("GET", path)
        return self.result_format(response)
    
    def list_wallets(self, data):
        path = "/wallet_account?page={}&per_page={}".format(
            data['page'], data['pageSize']
        )
        response = self.make_request("GET", path)
        return self.result_format(response)