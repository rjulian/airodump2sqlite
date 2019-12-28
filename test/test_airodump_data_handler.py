import unittest
from unittest.mock import MagicMock
from airodump2sqlite import airodump_data_handler

EXAMPLE_SELECT = ('00:00:00:00:00:00',
                  'gordon_kujawa',
                  '2019-12-28 11:44:24',
                  '2019-12-28 11:44:24',
                  '-72',
                  '1',
                  '(not associated)',
                  '',
                  '2019-12-28 11:44:24')

EXAMPLE_DICTIONARY = { 'mac':'00:00:00:00:00:00',
                       'first':'2019-12-28 11:44:24',
                       'last':'2019-12-28 11:44:24',
                       'power':'-72',
                       'packets':'1',
                       'bssid':'(not associated)',
                       'probed':''}

EXAMPLE2_DICTIONARY = { 'mac':'00:00:00:00:00:00',
                        'first':'2019-12-28 11:44:24',
                        'last':'2019-12-28 11:45:24',
                        'power':'-72',
                        'packets':'1',
                        'bssid':'(not associated)',
                        'probed':''}



class AirodumpDataHandlerTestCase(unittest.TestCase):
    def setUp(self):
        self.database_handler = MagicMock()
        self.database_handler.update_item.return_value = True
        self.database_handler.insert_new_item.return_value = True

    def test_should_return_false_if_no_update_needed(self):
        self.database_handler.lookup_mac.return_value = EXAMPLE_SELECT
        example_dict_array = [ EXAMPLE_DICTIONARY ]
        test_handler = airodump_data_handler.AirodumpDataHandler(example_dict_array,self.database_handler)
        self.assertIsNone(test_handler.needs_updating(EXAMPLE_SELECT, EXAMPLE_DICTIONARY))

    def test_should_return_true_if_update_needed(self):
        self.database_handler.lookup_mac.return_value = EXAMPLE_SELECT
        example_dict_array = [ EXAMPLE2_DICTIONARY ]
        test_handler = airodump_data_handler.AirodumpDataHandler(example_dict_array,self.database_handler)
        self.assertTrue(test_handler.needs_updating(EXAMPLE_SELECT, EXAMPLE2_DICTIONARY))

    def test_adds_last_ten_correctly(self):
        last_ten = airodump_data_handler.AirodumpDataHandler.create_last_ten('2019-12-28 11:44:24','2019-12-28 11:44:24,2019-12-28 11:44:22,2019-12-28 11:44:23')
        self.assertIsInstance(last_ten, str)
        self.assertTrue(len(last_ten.split(',')) == 4)

    def test_adds_last_ten_only_adds_ten(self):
        last_ten = airodump_data_handler.AirodumpDataHandler.create_last_ten('2019-12-28 11:44:24','2019,2018,2017,2016,2015,2014,2013,2012,2011,2010')
        self.assertIsInstance(last_ten, str)
        self.assertTrue(len(last_ten.split(',')) == 10)
        self.assertEqual(last_ten.split(',')[0],'2019-12-28 11:44:24')
