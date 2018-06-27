# -*- coding: utf-8 -*-

from dragonex import DragonExV1

HOST = 'https://openapi.dragonex.im'

def user_own_coin_keys(dragonex):
    print('getting user own coin keys')
    r = dragonex.get_user_own_coins()
    key = set()
    for item in r.data:
        key = key.union(set(dict(item).keys()))
    return key

def all_symbol_keys(dragonex):
    print('getting all symbol keys')
    r = dragonex.get_all_symbols()
    key = set()
    print(r.data)
    for item in r.data:
        key = key.union(set(dict(item).keys()))
    return key

def all_coin_keys(dragonex):
    print('getting all coin keys ...')
    r = dragonex.get_all_coins()
    key = set()
    for item in r.data:
        key = key.union(set(dict(item).keys()))
    return key

if __name__ == '__main__':
    import os
    ACCESS_KEY = os.environ.get('ACCESS_KEY')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    dragonex = DragonExV1(access_key=ACCESS_KEY, secret_key=SECRET_KEY, host=HOST)
    dragonex.ensure_token_enable(False)

    keys = {}
    keys['user_own_coin'] = user_own_coin_keys(dragonex)
    keys['all_symbol'] = all_symbol_keys(dragonex)
    keys['all_coins'] = all_coin_keys(dragonex)

    print(keys)
