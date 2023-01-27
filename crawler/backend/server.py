# Import flask and datetime module for showing date and time
from flask import Flask
from flask import request

import datetime
from googlesearch import search
import pandas as pd
import re
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template


# Initializing flask app
app = Flask(__name__)


# Route for seeing a data
@app.route('/data', methods=['GET', 'POST'])
def get_time():


 searchKeyWord = request.form['search']

 totalNoOfRecords = request.form['number']
 print('Please wait. Your request is being processed. \n')
 resultLinks = []

 results = search(searchKeyWord, num_results=int(totalNoOfRecords))
 contact_info = {
    "link": [],
    "phone": [],
    "email": [],
    "zipcode": [],
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
    zipcode_regex = re.compile(r'\b\d{5}\b')
    zipcode_match = re.search(zipcode_regex, soup.get_text())
    print(zipcode_match.group() if zipcode_match else None)
    print(email.group() if email else None)
    print(phone.group() if phone else None)
    print(link)
    contact_info['link'].append(link)
    contact_info['phone'].append(phone.group() if phone else 'N/A')
    contact_info['email'].append(email.group() if email else 'N/A')
    contact_info['zipcode'].append(
        zipcode_match.group() if zipcode_match else 'N/A')

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

 return 'Data downloaded'

@app.route('/main')
def home():
   return render_template('index.html')

# Running app
if __name__ == '__main__':
	app.run(debug=True)
