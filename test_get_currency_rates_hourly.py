#!/usr/bin/env python3

import unittest, os, csv
from get_currency_rates_hourly import run_exchange_rates_api, write_data_to_csv

class TestCurrencyRatesScript(unittest.TestCase):

    def test_run_exchange_rates_api(self):
        """
        Testcase to check if the API is working as expected. To verify we will be checking the length
        of the exchange rates by using data['rates']. We will also check the base currency value. It
        should be same as what we sent as parameter.
        """
        API_URL = "https://api.exchangeratesapi.io/latest"
        BASE_CURRENCY = "USD"
        data=run_exchange_rates_api(API_URL, BASE_CURRENCY)
        self.assertTrue(len(data['rates']) > 1)
        self.assertEqual(data['base'], 'USD')
    
    def test_neg_run_exchange_rates_api(self):
        """
        This is a negative testcase where we will be passing the wrong currency code as base currency
        and we would expect to get an error in the form of response from API.
        """
        API_URL = "https://api.exchangeratesapi.io/latest"
        BASE_CURRENCY = "USDE"
        data=run_exchange_rates_api(API_URL, BASE_CURRENCY)
        self.assertEqual(data['error'],"Base 'USDE' is not supported.")
        
    def test_write_data_to_csv(self):
        """
        This testcase is to check that the function 'write_data_to_csv' is able to create a new file,
        add headers and then append the output which is in dict format to the output file.
        We will be checking if the file is created and check the data quality (The data we passed as
        parameter should be present in the output file).
        
        At the end, we remove the output file so that when this test case is run next time the fresh
        file is created.
        """
        file_name = 'test_file.csv'
        file_header = ['Date', 'AUD', 'BGN', 'BRL', 'CAD', 'CHF', 'CNY', 'CZK', 'DKK', 'EUR', 'GBP', 'HKD', 'HRK', 'HUF', 'IDR', 'ILS', 'INR', 'ISK', 'JPY', 'KRW', 'MXN', 'MYR', 'NOK', 'NZD', 'PHP', 'PLN', 'RON', 'RUB', 'SEK', 'SGD', 'THB', 'TRY', 'USD', 'ZAR']
        dummy_json = {}
        dummy_json['EUR'] = '1.345'
        dummy_json['INR'] = '0.035'
        dummy_json['CAD'] = '2.010'
        write_data_to_csv(dummy_json, file_name, file_header)
        self.assertTrue(os.path.exists(file_name))
        with open(file_name, 'r') as data:
            for line in csv.DictReader(data):
                self.assertEqual(line.get('CAD'),'2.010')
                self.assertEqual(line.get('EUR'),'1.345')
                self.assertEqual(line.get('INR'),'0.035')
        data.close()
        os.remove(file_name)

if __name__ == '__main__':
    unittest.main()