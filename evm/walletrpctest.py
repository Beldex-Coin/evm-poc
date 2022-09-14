import evmcore.rpc.wallet 
import evmcore.rpc.daemon
import evmcore.rpc.rpc

rpc = evmcore.rpc.rpc.JSONRPC('{protocol}://{host}:{port}'.format(protocol='http', host='127.0.0.1', port=33452))
get_version = {
      'method': 'get_version',
      'jsonrpc': '2.0', 
      'id': '0'
  }

try:
    res = rpc.send_json_rpc_request(get_version)
    print(res)
    res=res.generate_from_keys()
except Exception as e:
    print('Failed to call version RPC: {}'.format(e))
