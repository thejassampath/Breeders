from googlesearch import search
import csv
import pandas as pd
import re
from datetime import datetime
import numpy
print('================================================')
print('GOOGLE SEARCH')
print('================================================')

searchKeyWord = input('Enter your search keyword: ')

totalNoOfRecords = input('How many records you need to save in CSV? ')
print('Please wait. Your request is being processed. \n')
resultLinks = []

results = search(searchKeyWord, num_results=int(totalNoOfRecords))

for link in results:
    print(link)
df = pd.DataFrame(results)


now = datetime.now()
outputFileName = searchKeyWord + now.strftime("%d-%m-%Y") + '.csv'

df.to_csv(outputFileName, mode='a', encoding='utf-8',
          index=False, header=False)
print('================================================\n')
print('Your data has been processed successfully!!. Please check the output in the below file!!\n')
print(outputFileName + '\n')
print('================================================\n')
