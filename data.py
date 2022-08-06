import requests 


TRIVIA_API = "https://opentdb.com/api.php"
PARAMETERS = {
    "amount": 10,
    "type": "boolean"
}


#Preset variable for the first call
question_data = requests.get(TRIVIA_API, params=PARAMETERS).json()["results"]

#Make a GET request to get a newly generated set of questions from the TRIVIA using its API
def update_data():
    question_data = requests.get(TRIVIA_API, params=PARAMETERS).json()["results"]