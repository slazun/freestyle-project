# The 'Real Talk' College Search App

The goal of this project is to build a Python based application that combines college enrollment data from an API with user inputs to provide recommendations on whether or not a potential student is a good fit for a school. This app hopes to help potential students take ownership of their college searches by providing them a fun tool to get information and an honest point of view on whether or not they're qualified to attend a school. 

## Setting up Your Repository

To begin, fork this upstream repository by clicking the "Fork" button. Then, open the forked repo in GitHub Desktop by clicking the green "Clone or Download" button and selecting "Open in Desktop." This will create a copy of this repo but with your GitHub user name in the URL. From the newly opened GitHub desktop window, you can click "Open in Visual Studio" to have the ability to create and edit files in the text editor and connect seamlessly to your repo. From the navigation bar in GitHub desktop, select "Repository" then "Open in Terminal." In your cloned repo, you should have access to the "college-app.py" application file.

## Environment Set Up

To run the app from the command-line, you need to first execute the following environment set-up steps. This is not necessary if you took the "Open in Terminal" approach from above. First, create and activate a new Anaconda virtual environment:

```
conda create -n stocks-env python=3.7 # (first time only)
conda activate stocks-env
```

When you are in this new environment, install the following required packages:

```
pip install dotenv
pip install sendgrid==6.0.5
pip install emojis
```

Now, from within the environment you should be able to execute (from the command-line) the Python script found in the "college-app.py" file: 

```
python college-app.py
```
This app is also reliant on specific python modules. These are imported at the top of the college-app.py file, but for reference they are:

```
import json
import os
import requests
import random
```

## Running the App

This application runs off of an API from Data.gov. It is necessary for you to obtain your own unique API key in order to run this application. You can obtain your key [here](https://api.data.gov/signup/). Please follow the instructions below to ensure your personal key is secure. 

1. Obtain your Data.gov API key and store it somewhere secure. Do not store it anywhere public or visible
2. Create a file called ".env" in your project repository
3. In the .env file, create a variable called SCORECARD_API_KEY 
4. Set this vairable equal to your secure API key in the .env file only. Do not put your key in the .py file directly. Example: SCORECARD_API_KEY="abc123" where "abc123" is replaced by your API key

The SCORECARD_API_KEY variable is referenced in the college-app.py file, and your key will be pulled into the application to run it without displaying the key. If you face any issues with this API, please reference the documentation found [here](https://collegescorecard.ed.gov/data/documentation/). 

## User Inputs

The output of this app is completely reliant on user inputs. Aside from "School Name," the inputs must be entered in the exact format specified in the input prompt. We hope to update this in future iterations!

Here are the user inputs and what they are used for:

1. If a potential student wants to review a specific school
    - Responses are 'Yes' or 'No'
    - This input determines if the app should use an API call for a single school or choose a random school
    - If 'Yes,' the user will be prompted to enter the full school name
2. The user enters their state of residence in an abbreviated format like "NY" for New York 
    - This is used to determine if tuition should be in state or out of state
3. The user then enters any budget restrictions. This should be entered without commas, such as '50000'
    - This is used to determine if a school is too expensive for a potential student
4. Finally, the user inputs their SAT score. This must be a score out of 1600 with no commas, like '1460'
    - This is used to determine if the student is academically qualified to apply to the selected school

## Final Output 

After running the "python college-app.py" command in the terminal and entering all the prompts, you should see an output like this:

```
-------------------------
THE BASICS:
POTENTIAL COLLEGE: New York University
COLLEGE LOCATION: New York, NY
STUDENT POPULATION SIZE: 26055
-------------------------
HOW YOU MATCH UP:
YEARLY TUITION: $50,464.00 This school is outside of your budget. 😟
AVERAGE SAT SCORE: 1408 Worth a shot! 😌
-------------------------
THINGS TO NOTE:
PERCENT FEMALE: 61.14% Large female population at this school. 👩
RACIAL & ETHINIC DIVERSITY: This school is very diverse. 👍
PERCENT FIRST GEN: 21.49% This school has an average amount of first generation students. 😌
PERCENT VETERAN 0.17% This school does not have many veterans. 👎
Sadly no information is available on the school's LGBTQ community or if the instition is accessible for persons with disabilities. 😢
-------------------------
 
```
This output will give you basic information about the college and how your SAT scores and budget stack up. The app also returns additional information about the student body. We hope to add additiional information in the next iteration. The benchmarks being used to give the "rating" are from credible sources found in the code. 

## Sending a Reminder Email

This app contains the functionality to send an email to the user that serves as a reminder to apply to the school they are interested in and a link for the school's website. In order to send this email, the user needs to complete a few steps:

1. Sign up for a free SendGrid account [here](https://signup.sendgrid.com/). You should use an email address from which you want to deploy the reminder email. 
2. When logged in, you need to obtain a new API key. Please store this somewhere secure, nowhere public or visible. 
3. Add this API key to the ".env" file under a new variable called SENDGRID_API_KEY
4. Set this new variable equal to your secure API key in the .env file only. Do not put your key in the .py file directly. Example: SCORECARD_API_KEY="abc123" where "abc123" is replaced by your API key

The SENDGRID_API_KEY variable is referenced in the college-app.py file, and your key will be pulled into the application to run it without displaying the key. 

In order to send the email, you will have to adjust the "from_email" variable in your code to the email associated with your SendGrid API. 

## Additional Info

There is another .py file in this repo called "api_data.py." This file is not necessary to run the app, but provides some basic code to better understand the data coming through the API. 

Have fun! 


