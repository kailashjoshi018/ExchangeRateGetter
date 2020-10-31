# ExchangeRateGetter

ExchangeRateGetter is a Python script for extracting the data from API at https://exchangeratesapi.io/ and write the values into the csv file.

## Prerequisites

Below are few prerequisites to run this program.

###Check the python version (this program runs on python3 & above)
```bash
python --version
```

The above should result similar to ```Python 3.6.9``` the version number can be changed.

###If there is no python installed in your system. It's the time to install it.
```bash
sudo apt install python3
```

This will install the python3 version onto your system. To confirm which version is installed you can run the ```--version``` command.

###Install package manager [pip]

pip is the package manager for python which is used to install the addition modules into the sytem. Install pip using below cmd.

```bash
sudo apt install python-pip
```

While running the script (as mentioned below), if you see an error mentioning ```module not found``` you can install that module using the package manager [pip].

```bash
pip install module_name
```

## Run the Script

Download the project and place them into a folder. From command line move the folder where the project is copied. This python program runs simply by using python command as shown below.

```bash
python get_currency_rates_hourly.py 
```

But, before running the program we need to know about the configurations and testing script.

File currency_code.config is the config file which is used for storing all the configuration details. The main python program reads the configurations such as API_URL, BASE_CURRENCY, OUTPUT_DIR, OUTPUT_FILE, CURRENCY_CODES (also used as headers) from the config file. This program is configured in this way as if there is any configuration change we have to make then it can be done by changing the values in config file rather than changing the python script.

test_get_currency_rates_hourly.py is the file which covers three test cases. Two of them are positive test cases and one is the negative test case.

## Output

Once the python program is run, you can see the output file at the location which is passed to the script in config file. If there is already a file existing with similar name the program appends the new values to it and if there is no file existing the program automatically creates one for you and add the data to it. Also note that, the file name will be prefixed with the current year.

Default output file name is : ```2020_currency_rates_hourly.csv```

## License
NA