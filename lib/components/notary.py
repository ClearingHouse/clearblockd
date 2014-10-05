from datetime import datetime
import logging
import decimal
import base64
import json

from lib import config, util

D = decimal.Decimal

def get_document_for_hash(hash_string = '', hash_type = 0):
    if hash:
        sql = 'SELECT * FROM documents WHERE hash_string = ? and hash_type = ? COLLATE NOCASE'
        params = {
                'query': sql,
                'bindings': (hash_string, hash_type)
        }
        return util.call_jsonrpc_api('sql', params)['result']

    return {}

def get_document_state_for(addresses = []):
    if isinstance(addresses, list) and len(addresses)>0:
        sql = 'SELECT * FROM documents WHERE owner IN ({})'.format(','.join(['?' for e in range(0,len(addresses))]))
        params = {
                'query': sql,
                'bindings': addresses
        }
        return util.call_jsonrpc_api('sql', params)['result']

    return []

def get_documents_for(addresses = []):
    if isinstance(addresses, list) and len(addresses)>0:
        my_addresses = ','.join(['?' for e in range(0,len(addresses))])
        sql = 'SELECT * FROM document_transactions WHERE source IN ({}) OR destination IN ({})'.format(my_addresses, my_addresses) # ugh, I miss ruby
        bindings = []
        bindings += addresses + addresses
        params = {
                'query': sql,
                'bindings': bindings
        }
        return util.call_jsonrpc_api('sql', params)['result']

    return []
