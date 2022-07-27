import asyncio
from .. import bdxserialize as x
from .. import bdxtypes as bdx

def decodePrefix(prefix, hfversion=14):
    if prefix == None: return
    ar1 = x.Archive(x.MemoryReaderWriter(prefix), False, bdx.hf_versions(hfversion))
    return asyncio.run(ar1.message(None, bdx.TransactionPrefix))

def decodeContract(txhex, hfversion=14):
    if txhex == None: return
    ar1 = x.Archive(x.MemoryReaderWriter(txhex), False, bdx.hf_versions(hfversion))
    return asyncio.run(ar1.message(None, bdx.TxExtraTagContractSource))
