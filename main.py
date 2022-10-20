import os
import requests
from datetime import datetime

username = os.environ.get("SHEET_USERNAME")
auth = os.environ.get("SHEET_AUTH")
api_key = os.environ.get("API_KEY")
app_id = os.environ.get("APP_ID")
sheet_endpoint = os.environ.get("SHEET_ENDPOINT")


sheety_headers = {
    "Authorization": auth,
    "Content-Type": "application/json"
}
# -------------------------- nutritionX NLP process----------------------#


headers = {
    "accept": "application/json",
    "Content-Type": "application/json",
    "x-app-id": app_id,
    "x-app-key": api_key,
    "x-remote_user_id": "0"
}

query = {
    "query": input("Enter your string: "),
}

exercise_url = "https://trackapi.nutritionix.com/v2/natural/exercise"
response = requests.post(url=exercise_url, json=query, headers=headers)
response.raise_for_status()
exercise_data = response.json()
exercises = exercise_data["exercises"]

# -----------------------------Using sheety api to manage the spreadsheet-----------------------#
"""Get request"""
# sheety_response = requests.get(url=sheety_get, headers=sheety_headers)
# print(sheety_response.text)

"""Post request"""
today = datetime.now()
date = today.strftime("%d/%m/%Y")
time = str(today.time())
print(time)

for i in range(len(exercises)):
    ex_name = exercises[i]["name"]
    ex_duration = exercises[i]["duration_min"]
    ex_calories = exercises[i]["nf_calories"]



    sheet = {
        "sheet1": {
            "date": date,
            "time": time,
            "exercise": ex_name,
            "duration": ex_duration,
            "calories": ex_calories
        }
    }

    post_response = requests.post(url=sheet_endpoint, json=sheet, headers=sheety_headers)


