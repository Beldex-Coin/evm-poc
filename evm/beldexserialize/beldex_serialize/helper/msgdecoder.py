import base64
import asyncio
from .. import bdxserialize as x
from .. import bdxtypes as bdx
import logging

def decodePrefix(prefix, hfversion=18):
    if prefix == None: return
    if isinstance(prefix,list):
        txhex = ''.join('{:02x}'.format(x) for x in prefix)
    prefix = base64.b16decode(prefix, True)
    if not isinstance(prefix, bytearray):
        prefix = bytearray(prefix)
    ar1 = x.Archive(x.MemoryReaderWriter(prefix), False, bdx.hf_versions(hfversion))
    return asyncio.run(ar1.message(None, bdx.TransactionPrefix))

def decodeContract(txhex, hfversion=18):
    if txhex == None: return
    if isinstance(txhex,list):
        txhex = ''.join('{:02x}'.format(x) for x in txhex)
    txhex = base64.b16decode(txhex, True)
    if not isinstance(txhex, bytearray):
        txhex = bytearray(txhex)
    ar1 = x.Archive(x.MemoryReaderWriter(txhex), False, bdx.hf_versions(hfversion))
    result = asyncio.run(ar1.message(None, bdx.TxExtraTagContractSource))
    return result

async def decodePrefixRunner(prefix, hfversion=18):
    try:
        if prefix == None: return
        if isinstance(prefix,list):
            txhex = ''.join('{:02x}'.format(x) for x in prefix)
        prefix = base64.b16decode(prefix, True)
        if not isinstance(prefix, bytearray):
            prefix = bytearray(prefix)
        ar1 = x.Archive(x.MemoryReaderWriter(prefix), False, bdx.hf_versions(hfversion))
        result = await ar1.message(None, bdx.TransactionPrefix)
        return result
    except Exception as e:
        logging.warning("decodePrefixRunner Error: {}".format(e))
        return None

async def decodeContractRunner(txhex, hfversion=18):
    if txhex == None: return
    if isinstance(txhex,list):
        txhex = ''.join('{:02x}'.format(x) for x in txhex)
    txhex = base64.b16decode(txhex, True)
    if not isinstance(txhex, bytearray):
        txhex = bytearray(txhex)
    ar1 = x.Archive(x.MemoryReaderWriter(txhex), False, bdx.hf_versions(hfversion))
    result = await ar1.message(None, bdx.TxExtraTagContractSource)
    return result
