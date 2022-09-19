from types import NoneType
from beldexserialize.beldex_serialize import bdxtypes
import evmcore.rpc.wallet 
import evmcore.rpc.daemon
import evmcore.rpc.rpc
import logging
import asyncio
from binascii import hexlify, unhexlify
import nacl.bindings
scalarmult_B = nacl.bindings.crypto_scalarmult_ed25519_base_noclamp


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
        if contract.contractversion==4:
            self.bdx_address = ''.join(chr(x) for x in contract.contract_address)
        else:
            self.bdx_address = ''.join('{:02x}'.format(x) for x in contract.contract_address.m_view_public_key) #makebdx addres
        
        self.m_spend_public_key = hexlify(scalarmult_B(unhexlify(''.join('{:02x}'.format(x) for x in contract.m_spend_secret_key))))
        self.m_view_public_key = hexlify(scalarmult_B(unhexlify(''.join('{:02x}'.format(x) for x in contract.m_view_secret_key))))
        self.owner_pubkey = contract.owner_pubkey.hex().encode('utf-8')
        self.contract_name = ''.join(chr(x) for x in contract.contract_name).encode('utf-8')
        self.contract_version = contract.contractversion
        self.m_spend_secret_key = ''.join('{:02x}'.format(x) for x in contract.m_spend_secret_key).encode('utf-8')
        self.m_view_secret_key = ''.join('{:02x}'.format(x) for x in contract.m_view_secret_key).encode('utf-8')
        self.contract_source = contract.contract_source
        self.state = ContractState.Idle
        self.amount = self.to_bdx(contract.amount)
        self.json_connection_str = '{protocol}://{host}:{port}'.format(protocol='http', host='127.0.0.1', port=33452)
        self.created_wallet_address=None
        asyncio.run(self.create_wallet())
        self.wallet_rpc = None
    
    def __str__(self):
        return f"{self.m_view_public_key}, {self.amount}, {self.owner_pubkey}, {str(self.state)}"

    def create_contract_address(self):
        pass
    
    def to_atomic(self, amount):
        return amount * pow(10, 9)
    
    def to_bdx(self, amount):
        """Takes atomic and creates create BDX amount"""
        return amount / pow(10, 9)

    async def create_wallet(self):
        self.wallet_rpc = evmcore.rpc.wallet.Wallet(protocol='http', host='127.0.0.1', port=33452)
        #generate_from_keys(self, restore_height = 0, filename = "", password = "", address = "", spendkey = "", viewkey = "", autosave_current = True):
        response = self.wallet_rpc.generate_from_keys(filename=self.bdx_address, password="", address=self.bdx_address, spendkey=self.m_spend_secret_key.decode('utf-8'),viewkey=self.m_view_secret_key.decode('utf-8'))
        
        if 'address' in response:
            self.created_wallet_address = response['address']
            logging.info("JSON Wallet Created: {}".format())
            #get_balance(self, account_index = 0, address_indices = [], all_accounts = False, strict = False)
        elif response['error']=={'code': -1, 'message': 'Wallet already exists.'}:
            self.wallet_rpc.open_wallet(self.bdx_address)
        response = self.wallet_rpc.get_balance()
        if 'balance' in response:
            self.amount=self.to_bdx(int(response['balance']))
    
    async def check_connected_wallet(self):
        result = self.wallet_rpc.get_balance(account_index=0)
        if result['per_subaddress'][0]['address'] is not self.created_wallet_address:
            await self.wallet_rpc.open_wallet(self.bdx_address) 
            return True #TODO should be false
        return True

    async def transfer(self, destination_address, amount):
        #could check balance, but assuming we have enough for now
        amount = self.to_atomic(int(amount))
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
        self.contract = self.evmcontext.contracts[contract_address]

    async def helloworld(self, *args):
        print("Hello World From Contract")
    
    async def transfer_to(self, destination):
        amount = 7
        await self.contract.transfer(destination, amount)








