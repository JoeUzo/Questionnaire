import requests
import os
from dotenv import load_dotenv
import json

load_dotenv()

questions_url = os.getenv("QUESTION_URL")
questions = requests.get(url=questions_url).json()

# with open('data.json', 'r') as file:
#     questions = json.load(file)
