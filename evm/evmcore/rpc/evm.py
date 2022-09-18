from types import NoneType
from beldexserialize.beldex_serialize import bdxtypes
import evmcore.rpc.wallet 
import evmcore.rpc.daemon
import evmcore.rpc.rpc
import logging
import asyncio

class ContractTransaction(object):
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
        self.transactions = []
        self.bdx_address = "test_contract"
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
        self.json_connection_str = '{protocol}://{host}:{port}'.format(protocol='http', host='127.0.0.1', port=33452)
        self.wallet_rpc = None
    
    def __str__(self):
        return f"{self.m_view_public_key}, {self.amount}, {self.owner_pubkey}, {str(self.state)}"

    def create_contract_address(self):
        pass
    
    def to_atomic(amount):
        return amount*100 #TODO correct it

    async def create_wallet(self):
        self.wallet_rpc = evmcore.rpc.wallet.Wallet(protocol='http', host='127.0.0.1', port=33452)
        #generate_from_keys(self, restore_height = 0, filename = "", password = "", address = "", spendkey = "", viewkey = "", autosave_current = True):
        response = self.wallet_rpc.generate_from_keys(filename=self.bdx_address, password="", address=self.bdx_address, spendkey=self.m_spend_secret_key,viewkey=self.m_view_secret_key)
        if response['address']==self.bdx_address:
            logging.info("JSON Wallet Created: {}".format())
            #get_balance(self, account_index = 0, address_indices = [], all_accounts = False, strict = False):
            if 'balance' in res:
                res = self.json_rpc.get_balance(self.bdx_address)
                self.amount=int(res['balance']) / pow(10, 9)
    
    async def check_connected_wallet(self):
        result = self.wallet_rpc.get_balance(account_index=0)
        if result['per_subaddress'][0]['address'] is not self.bdx_address:
            await self.open_wallet(self.bdx_address) 
            return False
        return True

    async def transfer(self, destination_address, amount):
        #could check balance, but assuming we have enough for now
        amount = int(amount) * pow(10, 9)
        if not self.wallet_rpc:
            self.wallet_rpc = evmcore.rpc.wallet.Wallet(protocol='http', host='127.0.0.1', port=33452)
            while not await self.check_connected_wallet():
                await asyncio.sleep(0.1)
        #walletrpc only takes current wallet
        #transfer(self, destinations, account_index = 0, subaddr_indices = [], priority = 0, ring_size = 0, unlock_time = 0, payment_id = '', get_tx_key = True, do_not_relay = False, get_tx_hex = False, get_tx_metadata = False):
        destination = {}
        destination['address']=destination_address
        destination['amount']=amount
        result = self.wallet_rpc.transfer(destinations=[destination], priority=1, get_tx_hex=True, get_tx_metadata = True) #unimportant
        self.amount -= amount
        transfersuccesful = False #get_transfer
        while True:
            await asyncio.sleep(1)
            transfersuccesful = False #get_transfer
            check = self.wallet_rpc.get_transfer_by_txid(result.tx_hash)
            if not check['transfer']['locked']: #TODO Check if this is the right variable for transactions that need to be verified
                transfersuccesful=True
            if transfersuccesful:
                logging.info("Transaction from {} to {} tx: {} Succesfull")
                break
        self.transactions.append(ContractTransaction(result.tx_hash))

    def _check_amount(self, spend):
        return spend < self.amount
        
    @property
    def get_amount(self):
        return self.amount

        
class DummyContract(object):
    def __init__(self, evmcontext, contract_address):
        self.evmcontext = evmcontext
        self.contract = self.evmcontext[contract_address]

    async def helloworld(self, *args):
        print("Hello World From Contract")
    
    async def transfer_to(self, destination):
        amount = 7
        await self.contract.transfer(destination, amount)








