from dragonex.dragonex import dragonex
from mysql import connector

class DB(object):
    def __init__(self, host='localhost', password='changeme', database='test'):
        self.host = host
        self.password = password
        self.conn = connector.connect(user='root', password=self.password, host=self.host, database=database)

    def close(self):
        self.conn.close()

    def update_all_coins(self):
        all_coin = dragonex.get_all_coins()
        sql = """insert into all_coins (coin_id, code) values ("{coin_id}", "{code}") ON DUPLICATE KEY UPDATE code="{code}";"""
        cursor = self.conn.cursor()
        for coin in all_coin.data:
            cursor.execute(sql.format(coin_id=coin['coin_id'], code=coin['code']))
        self.conn.commit()

    def get_all_coins(self):
        sql = "select coin_id, code from all_coins"
        cursor = self.conn.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    def update_all_symbols(self):
        all_symbols = dragonex.get_all_symbols()
        sql = """ insert into all_symbols (symbol_id, symbol) values("{symbol_id}", "{symbol}") ON DUPLICATE KEY UPDATE symbol="{symbol}";"""
        cursor = self.conn.cursor()
        for symbol in all_symbols.data:
            cursor.execute(sql.format(symbol_id=symbol['symbol_id'], symbol=symbol['symbol']))
        self.conn.commit()

    def get_all_symbols(self):
        sql = "select symbol_id, symbol from all_symbols"
        cursor = self.conn.cursor()
        cursor.execute(sql)
        return cursor.fetchall()


    