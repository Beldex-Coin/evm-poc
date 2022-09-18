import evmcore.rpc.wallet 
import evmcore.rpc.daemon
import evmcore.rpc.rpc
import evmcore.rpc.evm
import asyncio
# rpc = evmcore.rpc.rpc.JSONRPC('{protocol}://{host}:{port}'.format(protocol='http', host='127.0.0.1', port=33452))
# get_version = {
#       'method': 'get_version',
#       'jsonrpc': '2.0', 
#       'id': '0'
#   }

# try:
#     #res = rpc.send_json_rpc_request(get_version)
#     #print(res)
#     #res=res.generate_from_keys()
# except Exception as e:
#     print('Failed to call version RPC: {}'.format(e))

contract = evmcore.rpc.evm.Contract(None, dummy=True)
address = "ctr1Ncmfi8q8bzvdNvtUbnRUDPqHEyUM83rXwFbpqHVA9vcckHJ2fkM4U4wADYbCi7hh4ej1kjB8UVSKNVwMXDov3C4nqyeKdB"
spendkey = "7e57ad6e5aa9cb2e5e67e2ef7b33cf31031949ebdfb869296ce7cb66ee8d4f01"
viewkey ="59acc8c77f695aa0ca191a4a82af0d3a37e94590b95d23a0062fc033bdab7707"
#response = self.json_rpc.generate_from_keys(filename=self.bdx_address, password="pass", address=self.bdx_address, spendkey=self.m_spend_secret_key,viewkey=self.m_view_secret_key)
contract.bdx_address=address
contract.m_spend_secret_key = spendkey
contract.m_view_secret_key = viewkey
contract.wallet_rpc = None
contract.json_connection_str = '{protocol}://{host}:{port}'.format(protocol='http', host='127.0.0.1', port=33452)
evmcontext = {}
evmcontext[address] = contract
dummycontract = evmcore.rpc.evm.DummyContract(evmcontext, address)
funct = getattr(dummycontract, 'helloworld')
funct2 = getattr(dummycontract, 'transfer_to')
destination = '9uRAySmDmrqCT5EriZw51NVKStb3QEtXfJ6WM3PrzZttU5zt9Z4o2GRNp58Eqot2xLKP9StZAsQ1VTiDdFkQeCVXJ8ppcvF'
asyncio.run(funct(None))
asyncio.run(funct2(destination))
print("wait")

