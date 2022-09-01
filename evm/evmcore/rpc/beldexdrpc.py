#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

class Requester(object):
    def __init__(self, caller):
        self.socket = caller

    def get_info(self, socket=None):
        if not socket:
            socket = self.socket
        if self.socket.isconnected():
            result = socket.sendrecv(["rpc.getinfo"])
        if result[2] != b'200':
            raise RuntimeError("Request failed: got {}".format(result))
        return json.loads(result[3])
    
    def get_tx(self,socket=None, tx=None):
        if not socket:
            socket = self.socket
        if self.socket.isconnected():
            result = socket.sendrecv(["rpc.getinfo"])
        if result[2] != b'200':
            raise RuntimeError("Request failed: got {}".format( result))
        return json.loads(result[3])

    def get_hfinfo(self, socket=None):
        if not socket:
            socket = self.socket
        if self.socket.isconnected():
            result = socket.sendrecv(["rpc.hard_fork_info"])
        if result[2] != b'200':
            raise RuntimeError("Request failed: got {}".format(result))
        return json.loads(result[3])