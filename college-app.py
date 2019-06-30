# set up imports
from dotenv import load_dotenv
import json
import os
import requests
import datetime
import csv

def to_usd(my_price):
    return "${0:,.2f}".format(my_price)

load_dotenv()
# Need to securely input API credentials. using API guidance from this repo https://github.com/RTICWDT/open-data-maker/blob/master/API.md

api_key = os.environ.get("SCORECARD_API_KEY")

#restrict api call to eligible colleges in the url parameters. restrict the number of fields returned 
requests_url = f"https://api.data.gov/ed/collegescorecard/v1/schools?api_key={api_key}&school.main_campus=1&school.operating=1&_fields=school.name,school.city,school.state,2017.student.size,2017.admissions.sat_scores.average.overall,2017.cost.tuition.in_state,2017.cost.tuition.out_of_state,2017.aid.median_debt_suppressed.completers.overall,2017.student.demographics.female_share,2017.student.demographics.race_ethnicity.white_2000,2017.student.demographics.first_generation,2017.student.demographics.veteran"
response = requests.get(requests_url)
print(type(response)) #<class 'requests.models.Response'> its a string and need to use json module to treat as dictionary
print(response.status_code)
#print(response.text)
if response.status_code != 200:
    print("Sorry we have encountered an error with the data request. Please try again.")
    exit()

parsed_response = json.loads(response.text) #parsing string to dictionary