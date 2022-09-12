from zmq import Context
from evmcore.rpc.runner import EVMRUNNER
import time
evmrpc =[]
#evmrunner = EVMRUNNER(evmrpc)

import asyncio
import zmq
import zmq.asyncio

ctx = zmq.asyncio.Context()

async def async_process(msg):
    print(msg)

async def recv_and_process():
    sock = ctx.socket(zmq.REP)
    sock.bind('tcp://127.0.0.1:11223')
    msg = await sock.recv_multipart() # waits for msg to be ready
    reply = await async_process(msg)
    await sock.send_multipart(reply)

async def send_and_process():
    context = zmq.asyncio.Context()
    socket = ctx.socket(zmq.REQ)
    socket.connect('tcp://127.0.0.1:11223')
    for i in range(10):
        msg = "msg {0}".format(i)
        await socket.send(bytes(msg, 'utf-8'))
        print("Sending ", msg)
        await socket.recv()

async def main_thread():
    asyncio.gather(recv_and_process(),send_and_process())

asyncio.run(main_thread())
print("wait")