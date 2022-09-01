#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import base64
import unittest
import json
import pkg_resources

import asyncio
import aiounittest

from .test_data import bdxTestData
from .. import bdxserialize as x
from .. import bdxtypes as bdx
from .. import bdxobj as bdxo
from .. import bdxjson as bdxjs


__author__ = 'dusanklinec'


class bdxJsonTest(aiounittest.AsyncTestCase):
    """Simple tests"""

    def __init__(self, *args, **kwargs):
        super(bdxJsonTest, self).__init__(*args, **kwargs)
        self.test_data = bdxTestData()

    def setUp(self):
            self.test_data.reset()

    async def test_simple_msg(self):
        """
        TxinGen
        :return:
        """
        msg = bdx.TxinGen(height=42)
        msg_dict = await bdxo.dump_message(None, msg)
        js = bdxjs.json_dumps(msg_dict, indent=2)
        self.assertTrue(len(js) > 0)

        popo = json.loads(js)
        msg2 = await bdxo.load_message(popo, msg.__class__)
        self.assertIsNotNone(msg2)
        self.assertEqual(msg, msg2)

    async def test_tx_prefix(self):
        """
        TransactionPrefix
        :return:
        """
        msg = self.test_data.gen_transaction_prefix()
        msg_dict = await bdxo.dump_message(None, msg)
        js = bdxjs.json_dumps(msg_dict, indent=2)
        self.assertTrue(len(js) > 0)

        popo = json.loads(js)
        msg2 = await bdxo.load_message(popo, msg.__class__)
        self.assertIsNotNone(msg2)
        self.assertEqual(msg, msg2)

    async def test_boro_sig(self):
        """
        BoroSig
        :return:
        """
        msg = self.test_data.gen_borosig()
        msg_dict = await bdxo.dump_message(None, msg)
        js = bdxjs.json_dumps(msg_dict, indent=2)
        self.assertTrue(len(js) > 0)

        popo = json.loads(js)
        msg2 = await bdxo.load_message(popo, msg.__class__)
        self.assertIsNotNone(msg2)
        self.assertEqual(msg, msg2)


if __name__ == "__main__":
    unittest.main()  # pragma: no cover



