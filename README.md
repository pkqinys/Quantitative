# Quantitative

This repository contains code that can help you do technical researches on securities.

    data_collection.py: it contains a class hierachy called "Security". A "Security" class is used to fetch security informations and temporarily store them. In order for Security class to successfully save information from internet into local csv files, you have to first create two folders called CSV_price and CSV_price_google. CSV_price holds the csv files that you have manaully downloaded from yahoo finance, and CSV_price_google holds csv files that will be automatically saved when the functions in basci_functions.py use data from google. 
    
    basic_functions.py: it provides basic functions that can return price, volume, price returns and simple moving averages of a specified security. The invocation of a function has format like foo("AAPL", "20140303", "20170707", "filename.csv"). The last attribute is optinal. If it's not given, Security class will fetch that information from google. Otherwise, it would get the information from the provided local file. 
