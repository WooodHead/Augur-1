import time
from dragonex.dragonex import dragonex
from mysql import connector
import logging

class DB(object):
    def __init__(self, host='localhost', password='changeme', database='test'):
        self.host = host
        self.password = password
        self.conn = connector.connect(user='root', password=self.password, host=self.host, database=database)
        self.kline_map = {
            3: {'table_name': 'kline_15min', 'interval': 15},
            5: {'table_name': 'kline_60min', 'interval': 60}
        }

    def close(self):
        self.conn.close()

    def update_all_coins(self):
        logging.info('updating all coins')
        all_coin = dragonex.get_all_coins()
        sql = """insert into all_coins (coin_id, code) values ("{coin_id}", "{code}") ON DUPLICATE KEY UPDATE code="{code}";"""
        cursor = self.conn.cursor()
        for coin in all_coin.data:
            cursor.execute(sql.format(coin_id=coin['coin_id'], code=coin['code']))
        cursor.close()
        self.conn.commit()

    def get_all_coins(self):
        sql = "select coin_id, code from all_coins"
        cursor = self.conn.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()
        return data

    def update_all_symbols(self):
        logging.info('updating all symbols')
        all_symbols = dragonex.get_all_symbols()
        sql = """ insert into all_symbols (symbol_id, symbol) values("{symbol_id}", "{symbol}") ON DUPLICATE KEY UPDATE symbol="{symbol}";"""
        cursor = self.conn.cursor()
        for symbol in all_symbols.data:
            cursor.execute(sql.format(symbol_id=symbol['symbol_id'], symbol=symbol['symbol']))
        cursor.close()
        self.conn.commit()

    def get_all_symbols(self):
        sql = "select symbol_id, symbol from all_symbols"
        cursor = self.conn.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()
        return data

    def update_all_klines(self, kline_type):
        """ k线类型：3-15min线， 5-60min线 """
        logging.info('updating all klines of type %s' % kline_type)
        symbols = self.get_all_symbols()
        for symbol in symbols:
            self.update_kline(symbol[0], kline_type)

    def update_kline(self, symbol_id, kline_type):
        """ k线类型：3-15min线， 5-60min线 """
        logging.info('updating kline for %s of type %s' % (symbol_id, kline_type))
        if kline_type not in self.kline_map:
            logging.error("Kline Type Error: only 3 and 5 are supported")
            return
        table_name = self.kline_map[kline_type]['table_name']
        interval = self.kline_map[kline_type]['interval']
        self._update_kline(symbol_id, table_name, interval)

    def get_latest_kline(self, symbol_id, kline_type):
        """ k线类型：3-15min线， 5-60min线 """
        if kline_type not in self.kline_map:
            logging.error("Kline Type Error: only 3 and 5 are supported")
            return None
        table_name = self.kline_map[kline_type]['table_name']
        interval = self.kline_map[kline_type]['interval']
        return self._get_latest_kline(symbol_id, table_name)
        
    def _update_kline(self, symbol_id, table_name, interval):
        latest = self._get_latest_kline(symbol_id, table_name)
        if latest:
            start_time = latest[7] * 1000000000
        else:
            interval_sec = 60 * interval
            # start_time = (int(time.time() / interval_sec) * interval_sec - 2 * interval_sec) * 1000000000 # from now - 2 * interval 
            start_time = 1514736000 * 1000000000 # 2018-01-01 00:00:00
        sql = """ insert ignore into %s (symbol_id, 
                                           amount, 
                                           close_price, 
                                           max_price, 
                                           min_price, 
                                           open_price, 
                                           pre_close_price, 
                                           `timestamp`, 
                                           usdt_amount, 
                                           volume)
                  values (%s, %s, %s, %s, %s, %s, %s, %d, %s, %s) 
              """
        count = 100
        l = 100
        while l >= count:
            klines = dragonex.get_market_kline(symbol_id=symbol_id, start_time=start_time, search_direction=1, kline_type=3, count=count)
            data = klines.data
            if len(data) == 0: # no data
                return
            l = len(data['lists'])
            logging.info('get %d klines for %s of interval %d min' % (l, symbol_id, interval))
            cursor = self.conn.cursor()
            for kline in data['lists']:
                args = [table_name, symbol_id]
                args.extend(kline)
                cursor.execute(sql % tuple(args))
            start_time = data['lists'][-1][6] * 1000000000
            cursor.close()
        self.conn.commit()

    def _get_latest_kline(self, symbol_id, table_name):
        sql = "select * from %s where symbol_id='%s' and `timestamp`=(select max(`timestamp`) from %s where symbol_id='%s')" % (table_name, symbol_id, table_name, symbol_id)
        cursor = self.conn.cursor()
        cursor.execute(sql)
        latest = cursor.fetchall()
        cursor.close()
        if len(latest) > 0:
            return latest[0]
        return None
