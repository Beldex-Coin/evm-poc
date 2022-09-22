import asyncio
import zmq.asyncio
import zmq
import logging
logging.basicConfig(level=logging.INFO)

from beldexserialize.beldex_serialize.helper import msgdecoder as bdxdecoder
from beldexserialize.beldex_serialize.bdxtypes import ContractType
from evmcore.rpc.evm import ContractState
from evmcore.rpc.evm import Contract
from evmcore.rpc.evm import DummyContract
from evmcore.rpc import rpc_client

globalhandler = None

class Task(object):
    def __init__(self, name, future):
        self.name = name
        self.future = future

class EVMServer(object):
    def __init__(self, evmcontext):
        self.evmcontext = evmcontext
        self.ctx = zmq.asyncio.Context()
        self.socket = self.ctx.socket(zmq.REP)

    async def handle_request(self, msg):
        try:
            logging.info("MSG handle_request : {}".format(msg))
            if msg[0]==b'info':
                contract_address=msg[1].decode('utf-8')
                if contract_address in self.evmcontext.contracts:
                    return [b"info", 
                            "Amount: {}".format(self.evmcontext.contracts[contract_address].amount).encode('utf-8'),
                            "Contract_name: {}".format(self.evmcontext.contracts[contract_address].contract_name).encode('utf-8'), 
                            "Contract State {}".format(self.evmcontext.contracts[contract_address].state).encode('utf-8')]
                else:
                    return [b"info", 
                            b"error", 
                            b"contract not found"]
            elif msg[0] == b'test':
                #bdx_transaction = b'04020000000202000aedfb0c93059512d1048508ce04b2060437ab01e0a73fbcadc4641b0800a91b450fd1c5fe982bebaef63d619021ca680914770c02000a8be608c91cfbc603e9229607ae0baf06e50b8d14a5054336395fc42d5aaecf046bc3a99ba4a520ebbdc6becb560b94792861cca09cec02000259fe2cc43b3f182ab3b91fbc63c20e35bf56fbc1c88c42b6a0f447ceeb36dbbb0002c28b683dd8e01f7c5c70b461ffa5f6f06c52c2023c0fb30fb5f1854c1e746000ec0101696f3519cc6959eaef19000ecd74899ffe8790a2f0ffb51a8cff146afe4846ac02090134886b6ca6ca72054200030d636f6e74726163747465737434b0674cdde81b84b6a9e2b2bdae62a9b342815e6a9244a3bc788aba210425b675efc1bd6161cdbd7ce5dd764935dabf3dc869c6d6556e53de2644f7ce5731f3a99fd8eb3137b37657f28f81f7ab6a635f80e302bc0d0b3a46208567d8d77bf6e71abab2b31ae5f464e67b392b2605aba547a1dde58fb91ff5a6d76f2a1c557b0b000000000000000000000000000000000000000000000000000000000000000006736f7572636500e876481700000005058ef1da062db92351180007debb263314139dd037429bcc5667c941b233beea398251eddd600609361ea704f4ca5c2c91ef76c5777ff9ee37257ed60a18917be901f337d79f2acb7bb2b96bd0230f319ec65bd01401b6af54d09702e8e00940457a89464be2725c5fdc07f96f2c0d1ea19d6166df7071e40342169609ad1be52f5804e827070e4e3563b927b441ebcca69ed5f9d2024094054b17338279ad499bcb3e4aba64a27781a4826c9ad3c3c1e25c7e6b848c8935cf9345ca2817256f0b100416fbc37c89ee760fa43fbeb1c4d0887b948a6f6eaa17f035f5c6b021e4a5bc77ef8487b1aaad40a3601937713fcaec69fe050cadf62d6acf68589faae45a7a4b17661e2fb7c47faf10c991579dd707396b640907bf87f6329a3afe63c087a9c535040396a5f977817f98d162e7db01be33cd163cd6bfa1300a9b1cddcf41d2204fab13371500d12761bca02bf00900026d08624c2cd4fcb542eab7aeb8703dd8615491c9c88ff352c6f678ed336b2ec01b5ca633c028bc7fe066dc6989af1282d321fc4b6823ac81a227b1070fa14f953a36c27d9ae3b7d9dd5210f70acc6047c60fd286a878b6b5bda801bed33f8b6c484e6b80ec3b590937636dcac5e4a06dc1f35a4088445255ca54969644664a1dc3f00387fc4aad99ec740d31658fd86bdd0bbfc125d11047cb38c3af1a7faa9397be9a2c071ffe16936a232e8df1a65f3b2dd85a1f6db031bc0a9dbabdf03c4651295b483c0cf2e69c43e97c66736a1c262aaec2d1827aba7ad18ce90bb78c1795f376835e777a37f7e90bb8c42b7b6fc139591370382192c513a0483ca155e22c9efb27f97662bef7592de4edfb1036f309b82cc6161d5ee0bbab2f68a93f01f13d1ebb84acdb952c301bc38f1f6545650dd993a28115e05a7235cc936819aedc242fc9365bf3b877939f2508907e2feae6ebb7af022ae429bcceb5314b1eb6de2b7054f2e43144adf5643f80aa5283c6115466687b35930d2862a1c786684c9f2e930dd3fc1ff0603fb699f3517cfa739b40f7840f6ec011eda3487e434ba0019dab690f38cecfe7dd493c960144a6000898aa0a909734496157bea8ad01e838fa36b409bb0396d620cc71510152c5bff352dd198c882005692ad2636e6cd13cf091880b1b19c26961e782c7ba6fc1793a0b52bb620cf1992bc78b3fb011525e89ad0509317cd0414a5c0bedd405d9b451a661c821759e65665c197429bac7b746f0f605972fdac370d1ce1c6de1b69ab1ee7be42233c7bc3ebc0b55788cc8803aaf6f01585d43d0ba85d7a3d5bcfa3ef5c23672c0e56b29cb51ef7a2ad09b4d1bff75046e0240a6c00851ce237101b44434c174e4114bffa15a4e3eb219e2d3e782e30b092d4b309049db3202386effd251c0e5687d9132bcedf6819dce5ca10dbfb20fc3d3456bb0069e9a0498ef41b2f4954d32761ec1db82d6eeff4986d1e9a8e3033e94d59ca1af23ee033f349e58e6b57e9f78c07d39850dca872093e242d44c01b9eaffc396ad08a0fa7dd07977b77228f171db4b2dcc137437c8e0afc124bd0e3c91c52d7e0e7ffc3acbce96d8581584a506eb999f129166e8e4652b1601ad0ae501e87ac6d5c52ae6e7396cb04280cf85396bdb36b62e7f44e390c10ca8670801564dfdc24ba48dbecba76f20e04ff4092c18706b7730c278ad0885e7c7398cb47302ab1ef45736768140cfc304cc1256152e2c80237b786b5687e01f543d013016bb1ee9a38df53a3c49768cbb47589aa02a73c6195dceab1bad58aabaac0db4b9c35a112a57d8f6e707af674754bfd51e4a900da408845729f620ed435b0ed16af9f22145ddee0e016b588968ffb614b453ac647df3cdecf823f4855f8005d04116d0d0756e8753e44542b6fc8963f36efd11bf0497e600d9fd83e0508e0460db0aeafe371ce21dc0ef94a2157a98f5dedf61a24cafd8ccb8f9d5d5fb8a039920e7ce1d3bcaa963a1c74fdeca9ca850ab55fa332eaa9ea563cbe1a9609d0a571225d1d7afaaf5dc00a4163363e92a94fb81ca47f8cb3b39236049c2f57e0f8200621073a1f0c8bf6b4491da62715f4137adfeed4feb3888578b5e86539d04c4ee5f08323680baedf725ff1690b8e7719e557f018fb0a0c7fa88c61b1cf909e5604066b07e110cb0287e16e7e6a26304a71abb2f4ad6e3eae534003afb290c447dc130512d4f36ffc3d7a4cbdd61bc6b58dc70cc7930cce7dfa78548f8051711f4ed14ba729fca3306a696bbbb21dce078e8f4a615cbfa16207211d92b6ff929053e82b0ae7b5968f9fd3e3190c7b955fcd15318d570d5a43e1510e7798195'
                otx = await bdxdecoder.decodePrefixRunner(prefix=msg[2])
                print(otx)
                if otx.txtype==5: #txtype_contract
                    contract = await bdxdecoder.decodeContractRunner(otx.extra) #decode contract from source. 
                    globalhandler.add_request(contract.contract, contract.contract.contract_address)
                    return msg
            elif msg[0] == b'transfertest':
                #bdx_transaction = b'04020000000202000aedfb0c93059512d1048508ce04b2060437ab01e0a73fbcadc4641b0800a91b450fd1c5fe982bebaef63d619021ca680914770c02000a8be608c91cfbc603e9229607ae0baf06e50b8d14a5054336395fc42d5aaecf046bc3a99ba4a520ebbdc6becb560b94792861cca09cec02000259fe2cc43b3f182ab3b91fbc63c20e35bf56fbc1c88c42b6a0f447ceeb36dbbb0002c28b683dd8e01f7c5c70b461ffa5f6f06c52c2023c0fb30fb5f1854c1e746000ec0101696f3519cc6959eaef19000ecd74899ffe8790a2f0ffb51a8cff146afe4846ac02090134886b6ca6ca72054200030d636f6e74726163747465737434b0674cdde81b84b6a9e2b2bdae62a9b342815e6a9244a3bc788aba210425b675efc1bd6161cdbd7ce5dd764935dabf3dc869c6d6556e53de2644f7ce5731f3a99fd8eb3137b37657f28f81f7ab6a635f80e302bc0d0b3a46208567d8d77bf6e71abab2b31ae5f464e67b392b2605aba547a1dde58fb91ff5a6d76f2a1c557b0b000000000000000000000000000000000000000000000000000000000000000006736f7572636500e876481700000005058ef1da062db92351180007debb263314139dd037429bcc5667c941b233beea398251eddd600609361ea704f4ca5c2c91ef76c5777ff9ee37257ed60a18917be901f337d79f2acb7bb2b96bd0230f319ec65bd01401b6af54d09702e8e00940457a89464be2725c5fdc07f96f2c0d1ea19d6166df7071e40342169609ad1be52f5804e827070e4e3563b927b441ebcca69ed5f9d2024094054b17338279ad499bcb3e4aba64a27781a4826c9ad3c3c1e25c7e6b848c8935cf9345ca2817256f0b100416fbc37c89ee760fa43fbeb1c4d0887b948a6f6eaa17f035f5c6b021e4a5bc77ef8487b1aaad40a3601937713fcaec69fe050cadf62d6acf68589faae45a7a4b17661e2fb7c47faf10c991579dd707396b640907bf87f6329a3afe63c087a9c535040396a5f977817f98d162e7db01be33cd163cd6bfa1300a9b1cddcf41d2204fab13371500d12761bca02bf00900026d08624c2cd4fcb542eab7aeb8703dd8615491c9c88ff352c6f678ed336b2ec01b5ca633c028bc7fe066dc6989af1282d321fc4b6823ac81a227b1070fa14f953a36c27d9ae3b7d9dd5210f70acc6047c60fd286a878b6b5bda801bed33f8b6c484e6b80ec3b590937636dcac5e4a06dc1f35a4088445255ca54969644664a1dc3f00387fc4aad99ec740d31658fd86bdd0bbfc125d11047cb38c3af1a7faa9397be9a2c071ffe16936a232e8df1a65f3b2dd85a1f6db031bc0a9dbabdf03c4651295b483c0cf2e69c43e97c66736a1c262aaec2d1827aba7ad18ce90bb78c1795f376835e777a37f7e90bb8c42b7b6fc139591370382192c513a0483ca155e22c9efb27f97662bef7592de4edfb1036f309b82cc6161d5ee0bbab2f68a93f01f13d1ebb84acdb952c301bc38f1f6545650dd993a28115e05a7235cc936819aedc242fc9365bf3b877939f2508907e2feae6ebb7af022ae429bcceb5314b1eb6de2b7054f2e43144adf5643f80aa5283c6115466687b35930d2862a1c786684c9f2e930dd3fc1ff0603fb699f3517cfa739b40f7840f6ec011eda3487e434ba0019dab690f38cecfe7dd493c960144a6000898aa0a909734496157bea8ad01e838fa36b409bb0396d620cc71510152c5bff352dd198c882005692ad2636e6cd13cf091880b1b19c26961e782c7ba6fc1793a0b52bb620cf1992bc78b3fb011525e89ad0509317cd0414a5c0bedd405d9b451a661c821759e65665c197429bac7b746f0f605972fdac370d1ce1c6de1b69ab1ee7be42233c7bc3ebc0b55788cc8803aaf6f01585d43d0ba85d7a3d5bcfa3ef5c23672c0e56b29cb51ef7a2ad09b4d1bff75046e0240a6c00851ce237101b44434c174e4114bffa15a4e3eb219e2d3e782e30b092d4b309049db3202386effd251c0e5687d9132bcedf6819dce5ca10dbfb20fc3d3456bb0069e9a0498ef41b2f4954d32761ec1db82d6eeff4986d1e9a8e3033e94d59ca1af23ee033f349e58e6b57e9f78c07d39850dca872093e242d44c01b9eaffc396ad08a0fa7dd07977b77228f171db4b2dcc137437c8e0afc124bd0e3c91c52d7e0e7ffc3acbce96d8581584a506eb999f129166e8e4652b1601ad0ae501e87ac6d5c52ae6e7396cb04280cf85396bdb36b62e7f44e390c10ca8670801564dfdc24ba48dbecba76f20e04ff4092c18706b7730c278ad0885e7c7398cb47302ab1ef45736768140cfc304cc1256152e2c80237b786b5687e01f543d013016bb1ee9a38df53a3c49768cbb47589aa02a73c6195dceab1bad58aabaac0db4b9c35a112a57d8f6e707af674754bfd51e4a900da408845729f620ed435b0ed16af9f22145ddee0e016b588968ffb614b453ac647df3cdecf823f4855f8005d04116d0d0756e8753e44542b6fc8963f36efd11bf0497e600d9fd83e0508e0460db0aeafe371ce21dc0ef94a2157a98f5dedf61a24cafd8ccb8f9d5d5fb8a039920e7ce1d3bcaa963a1c74fdeca9ca850ab55fa332eaa9ea563cbe1a9609d0a571225d1d7afaaf5dc00a4163363e92a94fb81ca47f8cb3b39236049c2f57e0f8200621073a1f0c8bf6b4491da62715f4137adfeed4feb3888578b5e86539d04c4ee5f08323680baedf725ff1690b8e7719e557f018fb0a0c7fa88c61b1cf909e5604066b07e110cb0287e16e7e6a26304a71abb2f4ad6e3eae534003afb290c447dc130512d4f36ffc3d7a4cbdd61bc6b58dc70cc7930cce7dfa78548f8051711f4ed14ba729fca3306a696bbbb21dce078e8f4a615cbfa16207211d92b6ff929053e82b0ae7b5968f9fd3e3190c7b955fcd15318d570d5a43e1510e7798195'
                globalhandler.add_request(contract.contract, contract.contract.contract_address)
                return msg
        except Exception as e: 
            logging.warning(e)
            return  [b"info", 
                        b"error", 
                        b"contract not found"]

    async def recv_and_process(self):
        self.socket.bind("tcp://127.0.0.1:5555")
        while True:
            try:
                msg = await self.socket.recv_multipart()
                logging.info("MSG recv_and_process : {}".format(msg))
                reply= await self.handle_request(msg)
                if reply:
                    await self.socket.send_multipart(reply)
                else:
                    logging.info("Error recv_and_process : {}".format(msg))
            except Exception as e: logging.warning(e)

class ContractHandler(object):
    def __init__(self, evmcontext):
        self.evmcontext = evmcontext
        self.requests = []
        self.methodcalls=[]

    async def contract_waiter(self, contract_address):
        while self.evmcontext.contracts[contract_address].state == ContractState.Running:
            asyncio.sleep(1)

    def load_contract(self, contract_address):
        logging.debug("Loading Contract: {}".format(contract_address))
        #contract_source = self.evmcontext.contracts[contract_address]
        #always return DummyContract
        return DummyContract(self.evmcontext, contract_address)

    async def handle_method_call(self,contract_address, contract_interaction, contract_type):
        if self.evmcontext.contracts[contract_address].state is not ContractState.Idle:
            await self.contract_waiter(contract_address) #wait for contract
        self.evmcontext.contracts[contract_address].state = ContractState.Running
        #Dirty way of doing this
        try:
            contract_obj = self.load_contract(contract_address)
            calling_method = ''.join(chr(x) for x in contract_interaction.method)
            logging.info("Calling method: {} for Address: {} ContractName: {}".format(calling_method, 
                                                                                        contract_address,
                                                                                        self.evmcontext.contracts[contract_address].contract_name.decode('utf-8')))
            funct = getattr(contract_obj, calling_method)
            await funct(''.join(chr(x) for x in contract_interaction.args))
            self.evmcontext.contracts[contract_address].state = ContractState.Idle
        except Exception as e: 
            logging.warning(e)
            self.evmcontext.contracts[contract_address].state = ContractState.Idle
    
    async def handle_requests(self):
        while True:
            try:
                running_contract = None
                if len(self.requests) == 0:
                    await asyncio.sleep(10)
                else:
                    running_contract = None
                    for contract_interaction, contract_address in self.requests:
                        running_contract = [contract_interaction,contract_address]
                        logging.info("Received Contract {} type : {}".format(contract_address, contract_interaction.contract_type))
                        if contract_interaction.contract_type == ContractType.Create:
                            if contract_address not in self.evmcontext.contracts:
                                result = self.evmcontext.create_contract(contract_interaction)
                        elif contract_interaction.contract_type == ContractType.PublicMethod:
                            self.methodcalls.append(asyncio.ensure_future(self.handle_method_call(contract_address, contract_interaction, ContractType.PublicMethod)))
                        elif contract_interaction.contract_type == ContractType.SignedMethod:
                            self.methodcalls.append(asyncio.ensure_future(self.handle_method_call(contract_address, contract_interaction, ContractType.SignedMethod)))
                        elif contract_interaction.contract_type == ContractType.Terminate:
                            pass
                        else:
                            logging.error('received contract request Name {}'.format(contract_interaction.contract_name))
                    self.requests.pop(self.requests.index(running_contract))
            except Exception as e: 
                self.requests.pop(self.requests.index(running_contract))
                logging.warning(e)

    def add_request(self,contract, contract_address):
        self.requests.append([contract, contract_address])

class SubBeldexTX(object):
    def __init__(self, evmcontext, contracthandler):
        self.evmcontext = evmcontext
        self.contracthandler = contracthandler
        self.ctx = zmq.asyncio.Context()
        self.socket = self.ctx.socket(zmq.DEALER)
        self.socket.setsockopt(zmq.CONNECT_TIMEOUT, 5000)
        self.socket.setsockopt(zmq.HANDSHAKE_IVL, 5000)
        self.socket.connect('ipc:///home/martijn/.beldex/testnet/beldexd.sock')
        self.subbed = None
        asyncio.run(self.subscribe())

    async def subscribe(self):
        await self.socket.send_multipart([b'sub.mempool', b'_txallsub', b'all'])
        self.subbed = set()
    
    async def run_subscribe(self):
        if not self.subbed: await self.subscribe()
        while True:
            try:
                msg = await self.socket.recv_multipart()
                if len(msg) == 3 and msg[0] == b'REPLY' and msg[1] in (b'_blocksub', b'_txallsub', b'_txflashesub') and msg[2] in (b'OK', b'ALREADY'):
                    if msg[2] == b'ALREADY':
                        continue
                    what = 'new blocks' if msg[1] == b'_blocksub' else 'new txes' if msg[1] == b'_txallsub' else 'new flashes'
                    if what in self.subbed:
                        print("Re-subscribed to {} (perhaps the server restarted?)".format(what))
                    else:
                        self.subbed.add(what)
                elif len(msg) == 3 and msg[0] == b'notify.mempool':
                    logging.debug("New TX: {} prefix {}".format(msg[1].hex(), msg[2].hex()))
                    if len(msg)>2:
                        otx = await bdxdecoder.decodePrefixRunner(prefix=msg[2].hex())
                        if otx.txtype==5: #txtype_contract
                            contract = await bdxdecoder.decodeContractRunner(otx.extra)
                            self.contracthandler.add_request(contract.contract, ''.join(chr(x) for x in contract.contract.contract_address))
                else:
                    logging.warning("Received Weird stuff {}".format(msg))
                    await asyncio.sleep(1)
            except Exception as e: 
                logging.warning(e)

class PingPong(object):
    def __init__(self, evmcontext):
        self.evmcontext = evmcontext
    
    async def ping(self):
        while True:
            try:
                await asyncio.sleep(30)
                pass #do rpc->beldex->getversion self.evmcontext.rpc.getversion()
            except Exception as e: 
                    logging.warning(e)


class InfoClient(object):
    def __init__(self, contract_address):
        self.ctx = zmq.asyncio.Context()
        self.socket = self.ctx.socket(zmq.REQ)
        self.result = None
        asyncio.run(self.send_recv(contract_address))
    
    async def send_recv(self, contract_address):
        result = self.socket.connect("tcp://127.0.0.1:5555")
        await asyncio.sleep(0.1) #wait a bit for bind
        await self.socket.send_multipart([b'info', contract_address.encode('utf-8')])
        self.result = await self.socket.recv_multipart()

class EVMRunner(object):
    def __init__(self, connectionstring):
        self.beldexdrpc = rpc_client.EVMRPC(connectionstring,timeout=5)
        self.evmserver = EVMServer(self.beldexdrpc)
        self.contracthandler = ContractHandler(self.beldexdrpc)
        self.subscription = SubBeldexTX(self.beldexdrpc, self.contracthandler)
        self.pingpong = PingPong(self.beldexdrpc)
        global globalhandler
        globalhandler = self.contracthandler
        self.tasks ={}
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.tasks['EVMServer'] = self.evmserver.recv_and_process()
        self.tasks['ContractHandler'] = self.contracthandler.handle_requests()
        self.tasks['Subscription'] = self.subscription.run_subscribe()
        self.tasks['PingPong'] = self.pingpong.ping()
        self.start()
        
    def start(self):
        self.loop.run_until_complete(self.run_tasks())

    async def run_tasks(self):
        running ={}
        for name,task in self.tasks.items():
            await asyncio.sleep(0.1)
            running[name]= asyncio.ensure_future(task)
            logging.info("Started {}".format(name))
        while True:
            restart = None
            for name, future in running.items():
                await asyncio.sleep(10)
                logging.info("Status of {} is {}".format(name, "Running" if not future.done() else "Stopped"))
                if future.done():
                    logging.info("RestartMe of {} is {}".format(name, "running" if not future.done() else "Stopped"))
                    restart = name
            if restart:
                del running[restart]
                running[restart]= asyncio.ensure_future(self.tasks[restart])
                logging.info("Restarted {}".format(restart))
                restart=None

# if __name__=='__main__':
#     contracts = {}
#     evmcontext = [contracts]
#     runner = EVMRunner(evmcontext)




