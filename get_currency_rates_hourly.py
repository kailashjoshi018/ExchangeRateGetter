#!/usr/bin/env python3

import os
import requests
from datetime import datetime, timedelta
from pytz import timezone
import argparse
import configparser
import logging as logger
import csv

#usage content - This will be displayed whenever users try to run this script using -h (or) --help as the argument.
parser = argparse.ArgumentParser(description="""Gets current exchange rates from EXCHANGERATESAPI and saves them as CSV with year as PREFIX. Find the latest exchange rates at https://api.exchangeratesapi.io/latest. All the configurations are pickup from currency_code_api.config file.""")
args = parser.parse_args()
logger.basicConfig(filename='AppLogs/get_currency_rates_hourly.log', level=logger.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s',datefmt='%d-%m-%Y %H:%M:%S')
date = datetime.now(timezone('UTC')) - timedelta(hours=1, minutes=0)
current_date = date.strftime("%d-%m-%Y %H:00")


def start():
    """
    This is the start of the function and accepts no parameters. Here in this function we will
    read the configurations from config file and assign them to each variables. These variables
    will be used further to complete the script execution.
    """
    try:
        config = configparser.ConfigParser()
        config.read('currency_code_api.config')
        API_URL = config['CURRENCY_CODE_API_CONFIG']['API_URL']
        BASE_CURRENCY = config['CURRENCY_CODE_API_CONFIG']['BASE_CURRENCY']
        file_header = config['CURRENCY_CODE_API_CONFIG']['CURRENCY_CODES'].split(',')
        output_dir = config['CURRENCY_CODE_API_CONFIG']['OUTPUT_DIR']
        output_file_suffix = config['CURRENCY_CODE_API_CONFIG']['OUTPUT_FILE_SUFFIX']
        file_prefix = date.strftime("%Y")
        output_file = output_dir+file_prefix+"_"+output_file_suffix
        logger.info("The configurations are : \n\t\t\t API_URL = {} \n\t\t\t BASE_CURRENCY = {} \n\t\t\t FILE_HEADER = {}\n\t\t\t OUTPUT_FILE = {}".format(API_URL, BASE_CURRENCY, file_header, output_file))
        logger.info("Started the process to get exchange rates for {} at {}".format(BASE_CURRENCY, current_date))
        response_data = run_exchange_rates_api(API_URL, BASE_CURRENCY)
        exchange_rates = response_data['rates']
        is_data_write_complete = write_data_to_csv(exchange_rates, output_file, file_header)
        if is_data_write_complete:
            logger.info("The file : {} is updated with the recent data.".format(output_file))
    except (KeyError, NameError) as err:
        logger.error("Error occured with exception : {}".format(err))
        raise SystemExit("Error occured, please check logs..")
    

def run_exchange_rates_api(API_URL, BASE_CURRENCY):
    """
    This function deals with making the API call and returning the output and accepts
    API_URL and BASE_CURRENCY as parameters.
    API_URL - This is the main API url which we will be calling to get the exchange rates.
    BASE_CURRENCY - This is the base currency based on which we will be getting the exchange
                    rates. By default 'EUR' will be the base currency.
    """
    try:
        params = {'base':BASE_CURRENCY}
        r = requests.get(url = API_URL, params = params)
        data = r.json()
        logger.info("Response from API : {}".format(data))
        return data
    except (AttributeError, NameError, requests.exceptions.RequestException) as e:
        logger.error("Error occured with Exception : {}".format(e))
        raise SystemExit("Error occured while trying to make API call, please check logs..")
        

def write_data_to_csv(response_data, output_file, file_header):
    """
    This function deals with writing the data into the output file and 
    accepts response_json, output_file name and the output file_header.
    response_data - This contains the exchange rates for different currencies
    output_file - This is the file we will be writing [appending] the output to.
    file_header - This is used to make sure we are not adding any additional column of data
                  and is also used to add the headers to the file, if the file is being created
                  for the first time.
    """
    logger.info("Starting function to write data into CSV file at : {}".format(output_file))
    try:
        response_data['Date']=current_date
        fieldnames = file_header
        if not os.path.exists(output_file):
            logger.info("Output file not availabe, creating it now.")
            with open(output_file, 'w') as outfile:
                writer = csv.DictWriter(outfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerow(response_data)
                outfile.close()
        else:
            with open(output_file, 'a') as outfile:
                writer = csv.DictWriter(outfile, fieldnames=fieldnames)
                writer.writerow(response_data)
                outfile.close()
        return True
    except (KeyError, NameError, PermissionError, FileNotFoundError, ValueError) as e:
        logger.error("Error occured while writing data to output file with exception : {}".format(e))
        raise SystemExit("Error occured while writing data to output file, please check logs for more information..")
    

#start of the script
if __name__ == '__main__':
    start()