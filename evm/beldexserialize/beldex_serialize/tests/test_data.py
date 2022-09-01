#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import base64
import unittest
import pkg_resources

import asyncio
import aiounittest

from .. import bdxserialize as x
from .. import bdxtypes as bdx


__author__ = 'dusanklinec'


class bdxTestData(object):
    """Simple tests data generator"""

    def __init__(self, *args, **kwargs):
        super(bdxTestData, self).__init__()
        self.ec_offset = 0

    def reset(self):
        self.ec_offset = 0

    def generate_ec_key(self, use_offset=True):
        """
        Returns test EC key, 32 element byte array
        :param use_offset:
        :return:
        """
        offset = 0
        if use_offset:
            offset = self.ec_offset
            self.ec_offset += 1

        return bytearray(range(offset, offset+32))

    def gen_transaction_prefix(self):
        """
        Returns test transaction prefix
        :return:
        """
        vin = [
            bdx.TxinToKey(amount=123, key_offsets=[1, 2, 3, 2 ** 76], k_image=bytearray(range(32))),
            bdx.TxinToKey(amount=456, key_offsets=[9, 8, 7, 6], k_image=bytearray(range(32, 64))),
            bdx.TxinGen(height=99)
        ]

        vout = [
            bdx.TxOut(amount=11, target=bdx.TxoutToKey(key=bytearray(range(32)))),
            bdx.TxOut(amount=34, target=bdx.TxoutToKey(key=bytearray(range(64, 96)))),
        ]

        msg = bdx.TransactionPrefix(version=2, unlock_time=10, vin=vin, vout=vout, extra=list(range(31)))
        return msg

    def gen_borosig(self):
        """
        Returns a BoroSig message
        :return:
        """
        ee = self.generate_ec_key()
        s0 = [self.generate_ec_key() for _ in range(64)]
        s1 = [self.generate_ec_key() for _ in range(64)]
        msg = bdx.BoroSig(s0=s0, s1=s1, ee=ee)
        return msg


if __name__ == "__main__":
    unittest.main()  # pragma: no cover


