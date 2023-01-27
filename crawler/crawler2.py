from googlesearch import search
import csv
import pandas as pd
import re
from datetime import datetime
import numpy
import requests
from bs4 import BeautifulSoup

print('================================================')
print('GOOGLE SEARCH')
print('================================================')

searchKeyWord = input('Enter your search keyword: ')

totalNoOfRecords = input('How many records you need to save in CSV? ')
print('Please wait. Your request is being processed. \n')
resultLinks = []

results = search(searchKeyWord, num_results=int(totalNoOfRecords))
contact_info = {
    "link": [],
    "phone": [],
    "email": [],
    "address": [],
    "zipcode": [],
    "city": [],
}

for link in results:
    # send GET request to the link
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'html.parser')
    phone_regex = re.compile(
        r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})')
    phone = re.search(phone_regex, soup.get_text())

    email_regex = re.compile(
        r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}')
    email = re.search(email_regex, soup.get_text())
    address_regex = re.compile(r'\d{1,4} [\w\s]{1,20}(?:street|st|avenue|ave|road|rd|highway|hwy|square|sq|trail|trl|drive|dr|court|ct|park|parkway|pkwy|circle|cir|boulevard|blvd)\W?(?=\s|$)', re.IGNORECASE)
    address = re.search(address_regex, soup.get_text())
    zipcode_regex = re.compile(r'\b\d{5}\b')
    city_regex = re.compile(r'[A-Za-z\s]+(?:[,]|[\s]{1}[A-Z]{2})')
    zipcode_match = re.search(zipcode_regex, soup.get_text())
    city_match = re.search(city_regex, soup.get_text())
    print(address.group() if address else None)
    print(zipcode_match.group() if zipcode_match else None)
    print(city_match.group() if city_match else None)
    print(email.group() if email else None)
    print(phone.group() if phone else None)
    print(link)
    contact_info['link'].append(link)
    contact_info['phone'].append(phone.group() if phone else 'N/A')
    contact_info['email'].append(email.group() if email else 'N/A')
    contact_info['address'].append(address.group() if address else 'N/A')
    contact_info['zipcode'].append(
        zipcode_match.group() if zipcode_match else 'N/A')
    contact_info['city'].append(city_match.group() if city_match else 'N/A')

print(contact_info)

df = pd.DataFrame(contact_info)


now = datetime.now()
outputFileName = searchKeyWord + now.strftime("%d-%m-%Y") + '.csv'

df.to_csv(outputFileName, mode='a', encoding='utf-8',
          index=False, header=False)
print('================================================\n')
print('Your data has been processed successfully!!. Please check the output in the below file!!\n')
print(outputFileName + '\n')
print('================================================\n')
