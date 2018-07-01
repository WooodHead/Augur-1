from db.DB import DB
class TestDB(object):
    def setup_class(cls):
        cls.db = DB()

    def test_update_all_coins(self):
        self.db.update_all_coins()
        assert len(self.db.get_all_coins()) > 0

    def test_update_all_symbols(self):
        self.db.update_all_symbols()
        assert len(self.db.get_all_symbols()) > 0

    def test_get_latest_kline(self):
        kline = self.db.get_latest_kline(101, 3)
        print(kline)

    def test_update_kline(self):
        self.db.update_kline(104, 3)
