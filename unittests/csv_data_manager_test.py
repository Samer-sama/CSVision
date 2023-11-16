""" This module contains the TestCSVManager class which tests the CSVDataManager class. """
import unittest
import logging
import inspect

import pandas as pd

import src.csv_data_manager as csv_d_m


class TestCSVManager(unittest.TestCase):
    ''' Module for testing the CSVDataManager class. '''
    logging.basicConfig(format='%(levelname)s\t%(asctime)s\t%(message)s', level=logging.DEBUG, datefmt='%I:%M:%S')

    logging.info('TESTCLASS: %s', inspect.currentframe().f_code.co_name)
    var = 0

    def setUp(self):
        self.csv_manager_good = csv_d_m.CSVDataManager('CSV_Files/TelemetryUI_log_2023_11_14_14_34_10_good.csv')

    def test_csv_data_manager(self):
        ''' Test the instance creation of the CSVDataManager class. '''
        TestCSVManager.var += 1
        logging.info('TEST %s: %s', TestCSVManager.var, inspect.currentframe().f_code.co_name)

        testcase, testcases = 1, 5
        logging.debug('TESTCASE (%s/%s): %s', testcase, testcases, 'Raises(TypeError)')
        with self.assertRaises(TypeError):
            csv_d_m.CSVDataManager()

        testcase += 1
        logging.debug('TESTCASE (%s/%s): %s', testcase, testcases, 'Raises(ValueError)')
        with self.assertRaises(ValueError):
            csv_d_m.CSVDataManager(4)
            csv_d_m.CSVDataManager('CSV_Files/TelemetryUI_log_2023_09_28_17_37_11_xlsx.xlsx')

        testcase += 1
        logging.debug('TESTCASE (%s/%s): %s', testcase, testcases, 'Raises(FileNotFoundError)')
        with self.assertRaises(FileNotFoundError):
            csv_d_m.CSVDataManager('hello')
            csv_d_m.CSVDataManager('CSV_Files/TelemetryUI_log_2023_11_14_14_34_1.csv')

        testcase += 1
        logging.debug('TESTCASE (%s/%s): %s', testcase, testcases, 'Raises(pd.errors.EmptyDataError)')
        with self.assertRaises(pd.errors.EmptyDataError):
            csv_d_m.CSVDataManager('CSV_Files/TelemetryUI_log_2023_09_28_17_37_11_empty.csv')

        testcase += 1
        logging.debug('TESTCASE (%s/%s): %s', testcase, testcases, 'True')
        self.assertTrue(self.csv_manager_good.loaded)


if __name__ == '__main__':
    unittest.main()
