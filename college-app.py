# set up imports
from dotenv import load_dotenv
import json
import os
import requests
import datetime
import csv
import emoji

def to_usd(my_price):
    return "${0:,.2f}".format(my_price)

load_dotenv()
# Need to securely input API credentials. using API guidance from this repo https://github.com/RTICWDT/open-data-maker/blob/master/API.md

api_key = os.environ.get("SCORECARD_API_KEY")

#introducing app to the user. leaarn if they are evaluating a college or searchong for one

print("Welcome to the 'Real Talk' College Evaluator. This tool allows you to find a school that what aligns with you on what matters most...and tells you if it's realistic.")
school_search =input("Are you looking to evaluate a specific school? Please enter 'Yes' or 'No': ")
if school_search == 'Yes':
    school_name = input("Please enter the name of the college you are looking to evaluate:")
    requests_url = f"https://api.data.gov/ed/collegescorecard/v1/schools?api_key={api_key}&school.name={school_name}&school.main_campus=1&school.operating=1&_fields=school.name,school.city,school.state,latest.student.size,latest.admissions.sat_scores.average.overall,latest.cost.tuition.in_state,latest.cost.tuition.out_of_state,latest.aid.median_debt_suppressed.completers.overall,latest.student.demographics.female_share,latest.student.demographics.race_ethnicity.white_2000,latest.student.demographics.first_generation,latest.student.demographics.veteran"
elif school_search == 'No': #remove school name as an input in url
    requests_url = f"https://api.data.gov/ed/collegescorecard/v1/schools?api_key={api_key}&school.main_campus=1&school.operating=1&_fields=school.name,school.city,school.state,latest.student.size,latest.admissions.sat_scores.average.overall,latest.cost.tuition.in_state,latest.cost.tuition.out_of_state,latest.aid.median_debt_suppressed.completers.overall,latest.student.demographics.female_share,latest.student.demographics.race_ethnicity.white_2000,latest.student.demographics.first_generation,latest.student.demographics.veteran"
else:
    print("That input is not valid. Please try again with 'Yes' or 'No'.")
    exit()

#Defining user restrictions

print("Awesome! Please help us determine if this is a realistic fit for you.")
student_state = input("What state do you live in? Please use a state abbreviation like 'PA':")
budget = input("Do you have a")
SAT_score = input("What is your SAT score out of 1600? If you don't mind me asking... :")

#restrict api call to eligible colleges in the url parameters. restrict the number of fields returned 
#requests_url = f"https://api.data.gov/ed/collegescorecard/v1/schools?api_key={api_key}&school.name={school_name}&school.main_campus=1&school.operating=1&_fields=school.name,school.city,school.state,latest.student.size,latest.admissions.sat_scores.average.overall,latest.cost.tuition.in_state,latest.cost.tuition.out_of_state,latest.aid.median_debt_suppressed.completers.overall,latest.student.demographics.female_share,latest.student.demographics.race_ethnicity.white_2000,latest.student.demographics.first_generation,latest.student.demographics.veteran"
response = requests.get(requests_url)
print(type(response)) #<class 'requests.models.Response'> its a string and need to use json module to treat as dictionary
print(response.status_code)
#print(response.text)
if response.status_code != 200:
    print("Sorry we have encountered an error with the data request. Please try again.")
    exit()

#move code over from api_data python code to evaluate results
parsed_response = json.loads(response.text) #parsing string to dictionary
parsed_response = json.loads(response.text) #parsing string to dictionary
print(type(parsed_response)) #class dict
my_keys = parsed_response.keys() #to do: sort to ensure latest date is first
tables = list(my_keys) #need to referen
print(tables) 
print(type(parsed_response['results'])) #list
print(parsed_response['results'][0]) 
print(type(parsed_response['results'][0])) #dictionary 

#Output for single college search 

print("-------------------------")
print("POTENTIAL COLLEGE:" + " " + str(school_name))
print("COLLEGE LOCATION:"+ " " + str(parsed_response['results'][0]['school.city'])+ ", " +str(parsed_response['results'][0]['school.state']))
print("STUDENT POPULATION SIZE:" + " " + str(parsed_response['results'][0]['latest.student.size']))
if student_state == parsed_response['results'][0]['school.state']:
    tuition = parsed_response['results'][0]['latest.cost.tuition.in_of_state']
else:
    tuition = parsed_response['results'][0]['latest.cost.tuition.out_of_state']



#print("REQUEST AT: " + " " + now.strftime("%Y-%m-%d %H:%M:%S"))
#print("-------------------------")
#print("LATEST DAY:" + " " + str(last_refreshed))
#print("LATEST CLOSE:" + " " + str(to_usd(float(latest_close)))) #need to convert string to float to use usd function
#print("RECENT HIGH:" + " " + str(to_usd(float(recent_high)))) 
#print("RECENT LOW:" + " " + str(to_usd(float(recent_low)))) 
#print("-------------------------")
#if float(latest_close) > float(recent_high):
    #print("RECOMMENDATION: SELL\nRECOMMENDATION REASON: Latest close is greater than recent highs. Don't you like money?") #https://stackoverflow.com/questions/34980251/how-to-print-multiple-lines-of-text-with-python
#elif float(latest_close) < float(recent_low):
    #print("RECOMMENDATION: BUY\nRECOMMENDATION REASON: Latest close is less than recent lows. Don't you like money?")
#else: 
    #print("RECOMMENDATION: HOLD\nRECOMMENDATION REASON: Data is inconclusive. We're feeling risk averse")
#print("-------------------------")
#print(f"WRITING DATA TO CSV: {csv_file_path}")
#print("-------------------------")
#print("HAPPY INVESTING!")
#print("-------------------------")