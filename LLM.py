"""LLM Questions programme"""

import os

from dotenv import load_dotenv
from openai import OpenAI
import json

# Load the API key environment variable from the .env file.
load_dotenv()
AZURE_API_KEY = os.getenv("AZURE_API_KEY")
assert AZURE_API_KEY is not None

# EUS2 uses an OpenAI-compatible /v1 endpoint
EUS2_BASE_URL = "https://cuhk-apip.azure-api.net/openai-eus2/openai/v1"

# Initialize the client with the EUS2 base URL
client = OpenAI(
    base_url=EUS2_BASE_URL,
    api_key=AZURE_API_KEY,
    default_headers={"api-key": AZURE_API_KEY},
)

def q_generate(prompt: str) -> str:
        response = client.chat.completions.create(
            model="gpt-5.1",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0.7,  # Control response creativity (0-1)
        )
        return response.choices[0].message.content

username_prompt = """\
    Please provide a username for a game. (only the name, no other text)
    """

prompt1 = """\
    Please generate 5 statements, a list of 3 "what is" options per statement\
    with the correct answer index of the list for 5 categories,\
    namely "Science", "History", "Literature", "Geography" and "Entertainment".\
    The purpose of these statements are for the game "Jeopardy!"\
    Each statement in a category should consist of a value chosen from\
    200, 400, 600, 800 and 1000, with the statement of the smallest value being the easiest.\
    The statements made for this round is for "Jeopardy!" round. Overall difficulty: 2/10\
    Please generate the output as a json object with the following format\
    (only the dictionary, no other text):
    {
        "round1": [
            {
                "name": category,
                "questions": [
                    {
                    "value": value, "question": statement,\
                    "options": [options] (do not include "what is"), "correct": options list index
                    }
                ]
            }
        ]
    }
    """

prompt2 = """\
    Please generate 5 statements, a list of 3 "what is" options per statement\
    with the correct answer index of the list for 5 categories,\
    namely "Science", "History", "Literature", "Geography" and "Entertainment".\
    The purpose of these statements are for the game "Jeopardy!"\
    Each statement in a category should consist of a value chosen from\
    200, 400, 600, 800 and 1000, with the statement of the smallest value being the easiest.\
    The statements made for this round is for "Double Jeopardy!" round. Overall difficulty: 6/10\
    Please generate the output as a json object with the following format\
    (only the dictionary, no other text):
    {
        "round1": [
            {
                "name": category,
                "questions": [
                    {
                    "value": value, "question": statement,\
                    "options": [options] (do not include "what is"), "correct": options list index
                    }
                ]
            }
        ]
    }
    """

prompt3 = """\
    Please generate 5 statements, a list of 3 "what is" options per statement\
    with the correct answer index of the list for 5 categories,\
    namely "Science", "History", "Literature", "Geography" and "Entertainment".\
    The purpose of these statements are for the game "Jeopardy!"\
    Each statement in a category should consist of a value chosen from\
    200, 400, 600, 800 and 1000, with the statement of the smallest value being the easiest.\
    The statements made for this round is for "Final Jeopardy!" round. Overall difficulty: 10/10\
    Please generate the output as a json object with the following format\
    (only the dictionary, no other text):
    {
        "round1": [
            {
                "name": category,
                "questions": [
                    {
                    "value": value, "question": statement,\
                    "options": [options] (do not include "what is"), "correct": options list index
                    }
                ]
            }
        ]
    }
    """

if __name__ == "__main__":
    data = q_generate(prompt1)
    print(data)