class ContractTansaction(object):
    def __init__(self, hash):
        self.txhash = hash
        self.txhistory = None
        self.temp1 =None
        self.temp2 =None

class Contract(object):
    def __init__(self, hash, contract_name, code, amount, owner=None):
        self.__hash = hash
        self.__code = code
        self.__contract_name = contract_name
        self.__amount = amount
        self.__owner = owner
        self.__txhistory = {}
        self.__key1 = None
        self.__key2 = None
        self.__key3 = None
    
    def transfer(self, tx, amount, pspendkey, pviewkey, destination_address):
        self.__amount -= amount

    def _check_amount(self, spend):
        return spend < self.__amount
    
    @property
    def get_amount(self):
        return self.__amount


