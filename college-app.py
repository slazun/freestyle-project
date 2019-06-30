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

#introducing app to the user. leaarn if they are evaluating a college or searchong for one

print("Welcome to the College Diversity Evaluator. This tool allows you to assess a school's level of diversity on different facotrs or find a school that's right for you.")
school_search =input("Are you looking to evaluate a specific school? Please enter 'Yes' or 'No': ")
if school_search == 'Yes':
    school_name = input("Please enter the name of the college you are looking to evaluate:")
    requests_url = f"https://api.data.gov/ed/collegescorecard/v1/schools?api_key={api_key}&school.name={school_name}&school.main_campus=1&school.operating=1&_fields=school.name,school.city,school.state,latest.student.size,latest.admissions.sat_scores.average.overall,latest.cost.tuition.in_state,latest.cost.tuition.out_of_state,latest.aid.median_debt_suppressed.completers.overall,latest.student.demographics.female_share,latest.student.demographics.race_ethnicity.white_2000,latest.student.demographics.first_generation,latest.student.demographics.veteran"
elif school_search == 'No': #remove school name as an input in url
    requests_url = f"https://api.data.gov/ed/collegescorecard/v1/schools?api_key={api_key}&school.main_campus=1&school.operating=1&_fields=school.name,school.city,school.state,latest.student.size,latest.admissions.sat_scores.average.overall,latest.cost.tuition.in_state,latest.cost.tuition.out_of_state,latest.aid.median_debt_suppressed.completers.overall,latest.student.demographics.female_share,latest.student.demographics.race_ethnicity.white_2000,latest.student.demographics.first_generation,latest.student.demographics.veteran"
else:
    print("That input is not valid. Please try again with 'Yes' or 'No'.")
    exit()

#restrict api call to eligible colleges in the url parameters. restrict the number of fields returned 
#requests_url = f"https://api.data.gov/ed/collegescorecard/v1/schools?api_key={api_key}&school.name={school_name}&school.main_campus=1&school.operating=1&_fields=school.name,school.city,school.state,latest.student.size,latest.admissions.sat_scores.average.overall,latest.cost.tuition.in_state,latest.cost.tuition.out_of_state,latest.aid.median_debt_suppressed.completers.overall,latest.student.demographics.female_share,latest.student.demographics.race_ethnicity.white_2000,latest.student.demographics.first_generation,latest.student.demographics.veteran"
response = requests.get(requests_url)
print(type(response)) #<class 'requests.models.Response'> its a string and need to use json module to treat as dictionary
print(response.status_code)
print(response.text)
if response.status_code != 200:
    print("Sorry we have encountered an error with the data request. Please try again.")
    exit()

parsed_response = json.loads(response.text) #parsing string to dictionary