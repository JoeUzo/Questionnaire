import requests
import os
from dotenv import load_dotenv

load_dotenv()

questions_url = os.getenv("QUESTION_URL")

def get_questions():
    questions = requests.get(url=questions_url).json()
    return questions
