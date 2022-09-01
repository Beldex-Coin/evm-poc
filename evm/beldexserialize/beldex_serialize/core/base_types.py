class bdxType:
    VERSION = 0

class txType(object):
    standard = 0
    state_change = 1
    key_image_unlock = 2
    stake = 3
    beldex_name_system = 4
    contract = 5
    _count = 6

class extraTag(object):
    TX_EXTRA_TAG_PADDING                    = 0x00
    TX_EXTRA_TAG_PUBKEY                     = 0x01
    TX_EXTRA_NONCE                          = 0x02
    TX_EXTRA_MERGE_MINING_TAG               = 0x03
    TX_EXTRA_TAG_ADDITIONAL_PUBKEYS         = 0x04
    TX_EXTRA_TAG_MASTER_NODE_REGISTER      = 0x70
    TX_EXTRA_TAG_MASTER_NODE_DEREG_OLD     = 0x71
    TX_EXTRA_TAG_MASTER_NODE_WINNER        = 0x72
    TX_EXTRA_TAG_MASTER_NODE_CONTRIBUTOR   = 0x73
    TX_EXTRA_TAG_MASTER_NODE_PUBKEY        = 0x74
    TX_EXTRA_TAG_TX_SECRET_KEY              = 0x75
    TX_EXTRA_TAG_TX_KEY_IMAGE_PROOFS        = 0x76
    TX_EXTRA_TAG_TX_KEY_IMAGE_UNLOCK        = 0x77
    TX_EXTRA_TAG_MASTER_NODE_STATE_CHANGE  = 0x78
    TX_EXTRA_TAG_BURN                       = 0x79
    TX_EXTRA_TAG_BELDEX_NAME_SYSTEM         = 0x7A
    TX_EXTRA_TAG_SECURITY_SIGNATURE         = 0x88
    TX_EXTRA_TAG_CONTRACT_SOURCE            = 0x42
    TX_EXTRA_MYSTERIOUS_MINERGATE_TAG       = 0xDE

class nounceID(object):
    TX_EXTRA_NONCE_PAYMENT_ID               = 0x00
    TX_EXTRA_NONCE_ENCRYPTED_PAYMENT_ID     = 0x01

class UVarintType(bdxType):
    pass


class IntType(bdxType):
    WIDTH = 0
    SIGNED = 0
    VARIABLE = 0

    def __repr__(self):
        return "%s:<w: %s, sig: %s, var: %s>" % (
            self.__class__,
            self.WIDTH,
            self.SIGNED,
            self.VARIABLE,
        )


class BoolType(IntType):
    WIDTH = 1


class UInt8(IntType):
    WIDTH = 1


class Int8(IntType):
    SIGNED = 1
    WIDTH = 1


class UInt16(IntType):
    WIDTH = 2


class Int16(IntType):
    SIGNED = 1
    WIDTH = 2


class UInt32(IntType):
    WIDTH = 4


class Int32(IntType):
    SIGNED = 1
    WIDTH = 4


class UInt64(IntType):
    WIDTH = 8


class SizeT(UInt64):
    WIDTH = 8


class Int64(IntType):
    SIGNED = 1
    WIDTH = 8
