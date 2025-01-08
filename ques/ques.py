import requests
import os
from dotenv import load_dotenv

load_dotenv()

questions_url = os.getenv("QUESTION_URL")
questions = requests.get(url=questions_url).json()
