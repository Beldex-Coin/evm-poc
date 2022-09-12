import asyncio
import zmq.asyncio
import zmq
import logging
logging.basicConfig(level=logging.INFO)

from beldexserialize.beldex_serialize.helper import msgdecoder as bdxdecoder



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
                contract_address=msg[1]
                if contract_address in self.evmcontext.contracts:
                    return [b"info", evmcontext.contracts[contract_address].amount, evmcontext.contracts[contract_address].contract_name]
                else:
                    return [b"info", b"contract not found"]
                return msg
        except Exception as e: 
            print(e)
            return [b"info", b"contract not found"]

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
            except Exception as e: print(e)

class ContractHandler(object):
    def __init__(self, context):
        self.requests = []
    
    async def handle_requests(self):
        while True:
            try:
                if len(self.requests) == 0:
                    await asyncio.sleep(10)
                else:
                    for context, contract, contract_address in self.requests:
                        pass
            except Exception as e: 
                print(e)

    def add_request(self, context, contract, contract_address):
        self.requests.append([context, contract, contract_address])

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
        while True:
            try:
                msg = await self.socket.recv_multipart()
                logging.info(("New TX: {}".format(msg[1].hex())))
                if len(msg) == 3 and msg[0] == b'REPLY' and msg[1] in (b'_blocksub', b'_txallsub', b'_txflashesub') and msg[2] in (b'OK', b'ALREADY'):
                    if msg[2] == b'ALREADY':
                        continue
                    what = 'new blocks' if msg[1] == b'_blocksub' else 'new txes' if msg[1] == b'_txallsub' else 'new flashes'
                    if what in self.subbed:
                        print("Re-subscribed to {} (perhaps the server restarted?)".format(what))
                    else:
                        self.subbed.add(what)
                elif len(msg) == 3 and msg[0] == b'notify.mempool':
                    print("New TX: {}".format(msg[1].hex()))
                    if len(msg)>2:
                        otx = await bdxdecoder.decodePrefixRunner(prefix=msg[2])
                        print(otx)
                        if otx.txtype==5: #txtype_contract
                            contract = bdxdecoder.decodeContract(otx.extra)
                            if __debug__: print("Handle contract name: {}".format(''.join(chr(x) for x in contract.contract.contact_name)))
                else:
                    await asyncio.sleep(1)
            except Exception as e: 
                print(e)


class TestClient(object):
    def __init__(self, evmcontext):
        self.evmcontext = evmcontext
        self.ctx = zmq.asyncio.Context()
        self.socket = self.ctx.socket(zmq.REQ)
#        self.socket.connect('tcp://127.0.0.1:5555')
    
    async def send_recv(self):
        await asyncio.sleep(0.1) #wait a bit for bind
        result = self.socket.connect("tcp://127.0.0.1:5555")
        await self.socket.send_multipart([b'info', b'address'])
        result = await self.socket.recv_multipart()
        logging.info(result)
        print(result)

class EVMRunner(object):
    def __init__(self, evmrpc):
        self.evmrpc = evmrpc
        self.evmserver = EVMServer(evmrpc)
        self.contracthandler = ContractHandler(evmrpc)
        self.subscription = SubBeldexTX(evmrpc, self.contracthandler)
        self.tasks ={}
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.tasks['EVMServer'] = self.evmserver.recv_and_process()
        self.tasks['ContractHandler'] = self.contracthandler.handle_requests()
        self.tasks['Subscription'] = self.subscription.run_subscribe()
        
    
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
                await asyncio.sleep(2)
                logging.info("Status of {} is {}".format(name, future.done()))
                if future.done():
                    logging.info("RestartMe of {} is {}".format(name, future.done()))
                    #del running[name]
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




