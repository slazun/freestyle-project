# set up imports
from dotenv import load_dotenv
import json
import os
import requests
import csv
import emoji
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def to_usd(my_price):
    return "${0:,.2f}".format(my_price)

load_dotenv()
# Need to securely input API credentials. using API guidance from this repo https://github.com/RTICWDT/open-data-maker/blob/master/API.md

api_key = os.environ.get("SCORECARD_API_KEY")
SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")
MY_ADDRESS = os.environ.get("MY_EMAIL_ADDRESS")

#introducing app to the user. leaarn if they are evaluating a college or searchong for one
print(" ") # source https://stackoverflow.com/questions/13872049/print-empty-line/22534622
print("Welcome to 'Real Talk' College Search. This tool allows you to find a school that what aligns with you on what matters most...and tells you if it's realistic.")
print(" ")
school_search =input("Are you looking to evaluate a specific school? Please enter 'Yes' or 'No': ")
print(" ")
if school_search == 'Yes':
    school_name = input("Please enter the name of the college you are looking to evaluate: ")
    requests_url = f"https://api.data.gov/ed/collegescorecard/v1/schools?api_key={api_key}&school.name={school_name}&school.main_campus=1&school.operating=1&_fields=school.name,school.city,school.state,latest.student.size,latest.admissions.sat_scores.average.overall,latest.cost.tuition.in_state,latest.cost.tuition.out_of_state,latest.aid.median_debt_suppressed.completers.overall,latest.student.demographics.female_share,latest.student.demographics.race_ethnicity.white_2000,latest.student.demographics.first_generation,latest.student.demographics.veteran"
elif school_search == 'No': #remove school name as an input in url
    requests_url = f"https://api.data.gov/ed/collegescorecard/v1/schools?api_key={api_key}&school.main_campus=1&school.operating=1&_fields=school.name,school.city,school.state,latest.student.size,latest.admissions.sat_scores.average.overall,latest.cost.tuition.in_state,latest.cost.tuition.out_of_state,latest.aid.median_debt_suppressed.completers.overall,latest.student.demographics.female_share,latest.student.demographics.race_ethnicity.white_2000,latest.student.demographics.first_generation,latest.student.demographics.veteran"
else:
    print("That input is not valid. Please try again with 'Yes' or 'No'.")
    exit()

#Defining user restrictions
# emoji credit to https://stackoverflow.com/questions/40446784/display-emoji-in-pythons-console and https://www.geeksforgeeks.org/python-program-to-print-emojis/
print(" ")
print("Awesome! Please help us determine if this school is a realistic fit for you.")
print(" ")
student_state = input("What state do you live in? Please use a state abbreviation like 'NY': ")
print(" ")
budget = input("Do you have a budget restriction? Please enter 'Yes' or 'No': ") 
print(" ")
if budget == 'Yes':
    budget_amount = input("Please input a max yearly tuition amount like '50000': ") #TODO make tuition number user friendly
elif budget == 'No':
    print("LUCKY YOU!" + " " + emoji.emojize(":expressionless_face:"))
    budget_amount = 10000000000000
else:
    print("Sorry that is an invalid input. Please try again with 'Yes' or 'No'.")
    exit()
print(" ")
SAT_score = input("What is your SAT score out of 1600? If you don't mind me asking... : ")

if int(SAT_score) <= 1600:
    pass
else:
    print("Sorry that is an invalid input. Please enter a value less than or equal to 1600.")
    SAT_score = input("What is your SAT score out of 1600? If you don't mind me asking... : ")

#Defining benchmarks https://www.census.gov/library/visualizations/2018/comm/classroom-diversity.html

avg_percent_white = 0.547 
avg_percent_female = 0.559
avg_percent_first_gen = 0.3 #source http://www.firstgenerationfoundation.org/
avg_percent_veteran = 0.04 #source https://www.acenet.edu/the-presidency/columns-and-features/Pages/By-the-Numbers-Undergraduate-Student-Veterans.aspx


#restrict api call to eligible colleges in the url parameters. restrict the number of fields returned 
#requests_url = f"https://api.data.gov/ed/collegescorecard/v1/schools?api_key={api_key}&school.name={school_name}&school.main_campus=1&school.operating=1&_fields=school.name,school.city,school.state,latest.student.size,latest.admissions.sat_scores.average.overall,latest.cost.tuition.in_state,latest.cost.tuition.out_of_state,latest.aid.median_debt_suppressed.completers.overall,latest.student.demographics.female_share,latest.student.demographics.race_ethnicity.white_2000,latest.student.demographics.first_generation,latest.student.demographics.veteran"
response = requests.get(requests_url)
#print(type(response)) #<class 'requests.models.Response'> its a string and need to use json module to treat as dictionary
#print(response.status_code)
#print(response.text)
if response.status_code != 200:
    print("Sorry we have encountered an error with the data request. Please try again.")
    exit()

#move code over from api_data python code to evaluate results
parsed_response = json.loads(response.text) #parsing string to dictionary
#print(type(parsed_response)) #class dict
my_keys = parsed_response.keys() #to do: sort to ensure latest date is first
tables = list(my_keys) #need to referen
#print(tables) 
#print(type(parsed_response['results'])) #list
#print(parsed_response['results'][0]) 
#print(type(parsed_response['results'][0])) #dictionary 

#Output for single college search. Basic Info. Source credit: robo advisor project

print("-------------------------")
print("THE BASICS:")
print("POTENTIAL COLLEGE:" + " " + str(school_name))
print("COLLEGE LOCATION:"+ " " + str(parsed_response['results'][0]['school.city'])+ ", " +str(parsed_response['results'][0]['school.state']))
print("STUDENT POPULATION SIZE:" + " " + str(parsed_response['results'][0]['latest.student.size']))
print("-------------------------")

#Assessing if attendance is realistic
print("HOW YOU MATCH UP:")
if student_state == parsed_response['results'][0]['school.state']:
    tuition = parsed_response['results'][0]['latest.cost.tuition.in_state']
else:
    tuition = parsed_response['results'][0]['latest.cost.tuition.out_of_state']

if float(tuition) > float(budget_amount):
    print("YEARLY TUITION:" + " " + str(to_usd(float(tuition)))+ " " + "This school is outside of your budget." + " " + emoji.emojize(":worried_face:"))
elif float(tuition) <= float(budget_amount):
    print("YEARLY TUITION:" + " " + str(to_usd(float(tuition)))+ " " + " " + emoji.emojize(":money_with_wings:"))
else:
    pass

avg_SAT_score = int(parsed_response['results'][0]['latest.admissions.sat_scores.average.overall'])

if avg_SAT_score > (int(SAT_score) + 50):
    print("AVERAGE SAT SCORE:" + " " + str(avg_SAT_score)+ " " + "You might want to take that test again..." + " " + emoji.emojize(":grimacing_face:"))
elif avg_SAT_score <= (int(SAT_score) + 50):
    print("AVERAGE SAT SCORE:" + " " + str(avg_SAT_score) + " " + "(Worth a shot!)" + " " + emoji.emojize(":relieved_face:"))
else:
    pass
print("-------------------------")
print("THINGS TO NOTE:")
#Giving feedback on the diversity of the institution

percent_female = float(parsed_response['results'][0]['latest.student.demographics.female_share'])
percent_female_modified = percent_female * 100

if percent_female > float(avg_percent_female):
    print("PERCENT FEMALE:" + " " + str(round(percent_female_modified,2))+ "% " + "Large female population at this school." + " " + emoji.emojize(":woman:"))
elif 0.5 <= percent_female <= float(avg_percent_female):
    print("PERCENT FEMALE:" + " " + str(round(percent_female_modified,2))+ "% " + "Average sized female population at this school." + " " + emoji.emojize(":woman:"))
else:
    print("PERCENT FEMALE:" + " " + str(round(percent_female_modified,2))+ "% " + "Small female population at this school." + " " + emoji.emojize(":thumbs_down:"))

percent_white= float(parsed_response['results'][0]['latest.student.demographics.race_ethnicity.white_2000'])
percent_white_modified = percent_white * 100

if percent_white > float(avg_percent_white):
    print("RACIAL & ETHINIC DIVERSITY:" + " " + "This school is not very diverse." + " " + emoji.emojize(":thumbs_down:"))
elif 0.45 <= percent_white <= float(avg_percent_white):
    print("RACIAL & ETHINIC DIVERSITY:"  + " " + "This school is moderately diverse." + " " +emoji.emojize(":relieved_smile:"))
else:
    print("RACIAL & ETHINIC DIVERSITY:"  + " " + "This school is very diverse." + " " +emoji.emojize(":thumbs_up:"))

percent_first_gen = float(parsed_response['results'][0]['latest.student.demographics.first_generation'])
percent_first_gen_modified = percent_first_gen * 100

if percent_first_gen > float(avg_percent_first_gen):
    print("PERCENT FIRST GEN:" + " " + str(round(percent_first_gen_modified,2))+ "% "+ "This school has a large population of first generation students." + " " + emoji.emojize(":thumbs_up:"))
elif 0.2 <= percent_first_gen <= float(avg_percent_first_gen):
    print("PERCENT FIRST GEN:"  + " " + str(round(percent_first_gen_modified,2))+ "% "+ "This school has an average amount of first generation students." + " " +emoji.emojize(":relieved_face:"))
else:
    print("PERCENT FIRST GEN"  + " " + str(round(percent_first_gen_modified,2))+ "% " +"This school does not have many first generations students." + " " +emoji.emojize(":thumbs_down:"))

if parsed_response['results'][0]['latest.student.demographics.veteran'] == None:
    pass
else:
    percent_vet = float(parsed_response['results'][0]['latest.student.demographics.veteran'])
    percent_vet_modified = percent_vet * 100

    if percent_vet > float(avg_percent_veteran):
        print("PERCENT VETERAN:" + " " + str(round(percent_vet_modified,2))+ "% "+ "This school has a large population of veterans." + " " + emoji.emojize(":thumbs_up:"))
    elif 0.025 <= percent_vet <= float(avg_percent_veteran):
        print("PERCENT VETERAN:"  + " " + str(round(percent_vet_modified,2))+ "% "+ "This school has an average amount of veterans." + " " +emoji.emojize(":relieved_face:"))
    else:
        print("PERCENT VETERAN"  + " " + str(round(percent_vet_modified,2))+ "% " +"This school does not have many veterans." + " " +emoji.emojize(":thumbs_down:"))

print("-------------------------")
print(" ")

if avg_SAT_score > (int(SAT_score) + 50):
    print("Looks like you need to get your scores up before applying. Let's try another college!")
elif float(tuition) > float(budget_amount):
    apply_anyway = input("This school is too exspensive... Apply anyway? Enter 'Yes' or 'No': ")
        if apply_anyway == 'No':
            exit()
        elif apply_anyway == 'Yes':
            pass
        else:
            print("Sorry that is an invalid input. Please try again with 'Yes' or 'No'.")
            exit()
else:
    pass



#


