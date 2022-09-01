#!/usr/bin/env python
# -*- coding: utf-8 -*-
import zmq
from evmcore.rpc import rpc_client
from bson import BSON   
import os, sys, traceback
import time
import json


#rpcclient = rpcclient.EVMRPC("ipc:///home/martijn/.beldex/testnet/beldexd.sock",timeout=5)


# class EVMRPC(object):
#     """
#     ZMQRPC: client class to export a class to an zmqrpc queue or client.
#     """
#     def __init__(self,target,timeout=30):
#         """
#         Instantiate this class with a zmq target (eg 'tcp://127.0.0.1:5000') and a timeout (in seconds) for method calls.
#         Then call zmqrpc server exported methods from the class.
#         """
        
#         self._context = zmq.Context()
#         self._zmqsocket = self._context.socket(zmq.DEALER)
#         # Connect to everything, or just one
#         if isinstance(target,list):
#             for t in target:
#                 self._zmqsocket.connect(target)
#         else:
#             self._zmqsocket.connect(target)
#         self._socket = target

#         self._pollin = zmq.Poller()
#         self._pollin.register(self._zmqsocket,zmq.POLLIN)
#         self._pollout = zmq.Poller()
#         self._pollout.register(self._zmqsocket,zmq.POLLOUT)
#         self._timeout = timeout
#         self._lastrun = None

#     def sendresv(self, catagory, args=None, kwarks=None, timeout=5):
#         msg = [catagory, catagory, args, kwarks]
#         self._zmqsocket.send(msg)  
#         for i in range(0,timeout*100):
#             if len(self._pollin.poll(timeout=1)) > 0:
#                 break
#             time.sleep(0.01)
#         msg_in = self._zmqsocket.recv(flags=zmq.NOBLOCK)
#         return msg_in


#     def _dorequest(self,msg,timeout=5):
#         """
#         _dorequest: Set up a BSON string and send zmq REQ to ZMQRPC target
#         """
#         # Set up bson message
#         #bson = BSON.encode(msg)
#         bson=msg
#         print(bson)
#         bson=msg
#         # Send...
#         try:
#             self._pollout.poll(timeout=timeout*1000) # Poll for outbound send, then send
#             self._zmqsocket.send(bson,flags=zmq.NOBLOCK)
#         except:
#             raise RuntimeWarning('Request failure')

#         # Poll for inbound then rx
#         try:        
#             for i in range(0,timeout*100):
#                 if len(self._pollin.poll(timeout=1)) > 0:
#                     break
#                 time.sleep(0.01)
#             msg_in = self._zmqsocket.recv(flags=zmq.NOBLOCK)
        
#         except:
#             raise RuntimeError('Response timeout')

#         if msg_in == None:
#             raise print('No response')
#         result = BSON(msg_in).decode()
#         self._lastrun = result.get('runner')
        
#         return result

if __name__ =="__main__":
    rpc = rpc_client.EVMRPC("ipc:///home/martijn/.beldex/testnet/beldexd.sock",timeout=5)
    info = rpc.sendrecv([b'rpc.get_info'])
    print(info)
    #y = rpc._zmqsocket.recv_multipart()
    #if(y) : print(y)
    info2 =rpc.request.get_info(rpc)
    print(info2)
 #   z = rpc._zmqsocket.recv(flags=zmq.NOBLOCK)
    print("wait")

#ipc:///home/martijn/.beldex/testnet/beldexd.sock

