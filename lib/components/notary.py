from datetime import datetime
import logging
import decimal
import base64
import json

from lib import config, util

D = decimal.Decimal

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
        sql = 'SELECT * FROM document_transactions WHERE source IN ({})'.format(','.join(['?' for e in range(0,len(addresses))])) # ugh, I miss ruby
        params = {
                'query': sql,
                'bindings': addresses
        }
        return util.call_jsonrpc_api('sql', params)['result']

    return []
