#!/usr/bin/env python
# -*- coding: utf-8 -*-
from evmcore.rpc.runner import EVMRunner
from evmcore.rpc.runner import InfoClient
import optparse

if __name__ =="__main__":
    parser = optparse.OptionParser()
    parser.add_option('--info', dest = 'contract_address', default="",
                            help = 'specify public contractaddress')
    parser.add_option('--rpc', dest='rpcsock', default ='ipc:///home/martijn/.beldex/testnet/beldexd.sock', 
                            help='set rpc beldexd sock cq. : ipc:///../../beldexd.sock')
    (options, args) = parser.parse_args()
    if options.contract_address:
        result = InfoClient(options.contract_address)
        print("Result: {}".format(result.result))
    else:
        print(options.rpcsock)
        EVMRunner(options.rpcsock)

