#!/usr/bin/env python
# -*- coding: utf-8 -*-
from yaml import serialize
import zmq
import os, sys, traceback
import time
import json
from .beldexdrpc import Requester
from .evm import Contract
from beldexserialize.beldex_serialize.helper import msgdecoder as bdxdecode

class EVMRPC(object):
    """
    ZMQRPC: client class to export a class to an zmqrpc queue or client.
    """
    def __init__(self,target,timeout=30):
        """
        Instantiate this class with a zmq target (eg 'tcp://127.0.0.1:5000') and a timeout (in seconds) for method calls.
        Then call zmqrpc server exported methods from the class.
        """
        
        self._context = zmq.Context()
        self._zmqsocket = self._context.socket(zmq.DEALER)
        # Connect to everything, or just one
        if isinstance(target,list):
            for t in target:
                self._zmqsocket.connect(target)
        else:
            self._zmqsocket.connect(target)
        self._pollin = zmq.Poller()
        
        self._pollin.register(self._zmqsocket,zmq.POLLIN)
        self._pollout = zmq.Poller()
        self._pollout.register(self._zmqsocket,zmq.POLLOUT)
        self._timeout = timeout
        self._lastrun = None
        self.request = Requester(self)
        self.contracts = {}
        self._loader()
    
    def _getblocks(self, startheight, endheight):
        if endheight<=startheight: return "error"
        currentheight = startheight
        blocks = []
        while(currentheight<=endheight):
            jump=99
            if endheight-currentheight < 100 : jump = endheight-currentheight
            blocks_temp =json.loads(self.sendrecv([b'rpc.get_block_headers_range'], 
                                                    [json.dumps({'start_height':currentheight, 'end_height':currentheight+jump, 'get_tx_hashes':True}).encode()])[3])
            blocks += blocks_temp['headers']
            currentheight= currentheight + jump +1
            print(len(blocks))
        return blocks
    
    def _getTxFromBlocks(self, blocks):
        txids =[]
        for block in blocks:
            if 'tx_hashes' in block:
                print(block)
                txids+=block['tx_hashes']
        return txids

    def _searchContractInteractions(self, txids):
        """BruteForce for contract interactions, for here we can find contract_create"""
        contractinteractions={}
        for txid in txids:
            tx = json.loads(self.sendrecv([b'rpc.get_transaction_pool'], [json.dumps({'tx_extra':True, 'stake_info':True, 'hash':txid}).encode()])[3])
            txjson = json.loads(tx['transactions'][0]['tx_json'])
            if txjson['type']==5:
                contractinteractions[txid] = txjson['extra']
        return contractinteractions
    
    def _decode_interaction(self, interaction):
        return bdxdecode.decodeContract(interaction[1])

    def _create_contract(self, raw_contract):
        contract = raw_contract.contract
        contract_name = ''.join(chr(x) for x in contract.contact_name)
        contract_source = contract.contract_source
        amount = contract.deposit_amount
        hash = raw_contract.txpubkey
        if contract_name not in self.contracts: 
            self.contracts[contract_name] = Contract(hash, contract_name, contract_source, amount)
            return True
        else:
            print(contract_name, contract_source, amount)
            return False

    def _loader(self):
        info = self.request.get_info()
        self.height = info['height']
        self.testnet = info['testnet']
        hfinfo = self.request.get_hfinfo()
        self.hfversion = hfinfo['version']
        self.hfstart = hfinfo['earliest_height']
        self.blocks = self._getblocks(54810,54810+987)
        self.contractinteractions = self._searchContractInteractions(self._getTxFromBlocks(self.blocks))
        for interaction in self.contractinteractions.items():
            result = self._decode_interaction(interaction)
            if hasattr(result.contract, 'contract_source'):
                self._create_contract(result)
            elif hasattr(result.contract, 'contract_method'):
                pass
            elif hasattr(result.contract, 'terminate' ):
                del self.contracts[result.contract.contract_name] #''join thing
        if __debug__:
            print('wait')
    
    def block_loader(height=None):
        pass

    def sendrecv(self, msg, args=None, kwarks=None, timeout=5):
        """Send Receive no Identifier needed, input must be array"""
        if not msg : raise RuntimeWarning("Nothing message to send")
        if isinstance(msg[0],str): 
            msg[0]=bytes(msg[0], 'utf-8')
        if args : msg+=args
        if kwarks : msg+=kwarks
        msg.insert(1, b'hi') #TODO: do something smart here
        print(msg)
        self._zmqsocket.send_multipart(msg)  
        for i in range(0,timeout*100):
            if len(self._pollin.poll(timeout=1)) > 0:
                break
            time.sleep(0.01)
        msg_incoming = self._zmqsocket.recv_multipart()
        return msg_incoming

    def isconnected(self):
        return True #TODO: implement this

