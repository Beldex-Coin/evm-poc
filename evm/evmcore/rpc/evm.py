from beldexserialize.beldex_serialize import bdxtypes

class ContractTansaction(object):
    def __init__(self, hash):
        self.txhash = hash
        self.txhistory = None
        self.temp1 =None
        self.temp2 =None

class ContractState(object):
    Running = 0,
    Waiting = 1,
    Pending = 2,
    Idle = 3

class Contract(object):
    def __init__(self, contract, dummy=None):
        if not isinstance(contract, bdxtypes.Contract):
            return
        self.oContract = contract
        self.m_spend_public_key = ''.join('{:02x}'.format(x) for x in contract.contract_address.m_spend_public_key)
        self.m_view_public_key = ''.join('{:02x}'.format(x) for x in contract.contract_address.m_view_public_key)
        self.owner_pubkey = ''.join('{:02x}'.format(x) for x in contract.owner_pubkey)
        self.contract_name = ''.join(chr(x) for x in contract.contract_name)
        self.contract_version = contract.contractversion
        self.m_spend_secret_key = ''.join('{:02x}'.format(x) for x in contract.m_spend_secret_key)
        self.m_view_secret_key = ''.join('{:02x}'.format(x) for x in contract.m_view_secret_key)
        self.contract_source = contract.contract_source
        self.state = ContractState(3)
        self.amount = contract.amount
    
    def __str__(self):
        return f"{self.m_view_public_key}, {self.amount}, {self.owner_pubkey}"
    
    async def transfer(self, destination_address, amount):
        self.amount -= amount
        #implement RPCCall

    def _check_amount(self, spend):
        return spend < self.amount
        
    @property
    def get_amount(self):
        return self.amount

        
class DummyContract(object):
    def __init__(self, evmcontext, contract_address):
        self.evmcontext = evmcontext
        self.contract = self.evmcontext[contract_address]

    async def helloworld(self):
        print("Hello World From Contract")
    
    async def transfer_to(self, destination):
        amount = 7
        await self.contract.transfer(destination, amount)








