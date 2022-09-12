from beldexserialize.beldex_serialize import bdxtypes
class ContractTansaction(object):
    def __init__(self, hash):
        self.txhash = hash
        self.txhistory = None
        self.temp1 =None
        self.temp2 =None

class Contract(object):
    def __init__(self, contract):
        if isinstance(contract, bdxtypes.Contract):
            self.oContract = contract
            self.m_spend_public_key = ''.join('{:02x}'.format(x) for x in contract.contract_address.m_spend_public_key)
            self.m_view_public_key = ''.join('{:02x}'.format(x) for x in contract.contract_address.m_view_public_key)
            self.owner_pubkey = ''.join('{:02x}'.format(x) for x in contract.owner_pubkey)
            self.contract_name = ''.join(chr(x) for x in contract.contract_name)
            self.contract_version = contract.contractversion
            self.m_spend_secret_key = ''.join('{:02x}'.format(x) for x in contract.m_spend_secret_key)
            self.m_view_secret_key = ''.join('{:02x}'.format(x) for x in contract.m_view_secret_key)
            self.contract_source = contract.contract_source
            self.amount = contract.amount
    
    def __str__(self):
        return f"{self.m_view_public_key}, {self.amount}, {self.owner_pubkey}"
    
    def transfer(self, tx, amount, pspendkey, pviewkey, destination_address):
        self.amount -= amount

    def _check_amount(self, spend):
        return spend < self.amount
    
    @property
    def get_amount(self):
        return self.amount

        
 



