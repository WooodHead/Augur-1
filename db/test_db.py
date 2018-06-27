import unittest
from DB import DB

class TestBD(unittest.TestCase):
    def setUp(self):
        print('setup')
        self.db = DB()

    def test_connect(self):
        print('connect')

    def test_update_all_coin(self):
        self.db.update_all_coin()


if __name__ == '__main__':
    unittest.main()
        
