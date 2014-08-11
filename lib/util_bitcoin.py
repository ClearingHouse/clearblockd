import os
import re
import json
import logging
import datetime
import decimal
import binascii

from pycoin import encoding

from lib import config

D = decimal.Decimal
decimal.getcontext().prec = 8

def round_out(num):
    #round out to 8 decimal places
    return float(D(num))        

def normalize_quantity(quantity, divisible=True):
    if divisible:
        return float((D(quantity) / D(config.UNIT))) 
    else: return quantity

def denormalize_quantity(quantity, divisible=True):
    if divisible:
        return int(quantity * config.UNIT)
    else: return quantity


get_btc_supply(normalize=False, at_block_index=None):
    """returns the total supply of VIA (based on what Viacoin Core says the current block height is)"""
    block_height = config.CURRENT_BLOCK_INDEX if at_block_index is None else at_block_index
    total_supply = 0

    offset = 0
    if config.TESTNET:
        offset = 8000

    max_blocks = 31536000

    range_list = (
        (26280001,        31536000,         0.5),
        (21024001,        26280000,         1 ),
        (15768001,        21024000,         2 ),
        (10512001,        15768000,         3 ),
        ( 5256001,        10512000,         4 ),
        (   42402-offset,  5256000,         5 ),
        (   31602-offset,    42401-offset,  6 ),
        (   20802-offset,    31601-offset,  7 ),
        (   10002-offset,    20801-offset, 10 ),
        (       2,           10001-offset,  0 ),
        (       1,               1,  10000000 ),
        (       0,               0,         0 )
    )

    if block_height >= max_blocks:
        block_height = max_blocks

    for (start, end, reward) in range_list:
        if start <= block_height <= end:
            range_size = block_height - start + 1
            total_supply += reward * range_size
            block_height -= range_size

    return total_supply if normalize else int(total_supply * config.UNIT)

def pubkey_to_address(pubkey_hex):
    sec = binascii.unhexlify(pubkey_hex)
    compressed = encoding.is_sec_compressed(sec)
    public_pair = encoding.sec_to_public_pair(sec)
    prefix = b'\x7f' if config.TESTNET else b'\x47'
    return encoding.public_pair_to_bitcoin_address(public_pair, compressed=compressed, address_prefix=prefix)
