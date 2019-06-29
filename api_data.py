# set up imports
from dotenv import load_dotenv
import json
import os
import requests
import datetime
import csv

load_dotenv()
# Need to securely input API credentials. using API guidance from this repo https://github.com/RTICWDT/open-data-maker/blob/master/API.md
api_key = os.environ.get("SCORECARD_API_KEY")
requests_url = f"https://api.data.gov/ed/collegescorecard/v1/schools?api_key={api_key}&school.name=Harvard"
response = requests.get(requests_url)
#print(type(response)) #<class 'requests.models.Response'> its a string and need to use json module to treat as dictionary
#print(response.status_code)
#print(response.text)
if response.status_code != 200:
    print("Sorry we have encountered an error with the data request. Please try again.")
    exit()

#Code to try to understand the data coming in from the API

parsed_response = json.loads(response.text) #parsing string to dictionary
print(type(parsed_response)) #class dict
my_keys = parsed_response.keys() #to do: sort to ensure latest date is first
tables = list(my_keys) #need to reference first in list as most recent date
print(tables) # metadata and results
print(type(parsed_response['results'])) #list
print(parsed_response['results'][0]) 
print(type(parsed_response['results'][0])) #dictionary 
subresults = parsed_response['results'][0] 
sub_keys = subresults.keys()
sub_tables = list(sub_keys) 
print(sub_tables) # years 1996-2017
print(type(subresults['2017'])) #dict
latest_year = subresults['2017']
year_keys = latest_year.keys()
year_tables = list(year_keys)
print(year_tables) #'completion', 'earnings', 'cost', 'student', 'academics', 'admissions', 'aid', 'repayment'