# llm_questions.py
import os
import json
import time
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
AZURE_API_KEY = os.getenv("AZURE_API_KEY")
assert AZURE_API_KEY, "Missing AZURE_API_KEY in .env file"

EUS2_BASE_URL = "https://cuhk-apip.azure-api.net/openai-eus2/openai/v1"
client = OpenAI(base_url=EUS2_BASE_URL, api_key=AZURE_API_KEY, default_headers={"api-key": AZURE_API_KEY})

def generate_jeopardy_round(retries=3):
    prompt = """\
Please generate 5 statements, a list of 3 "what is" options per statement with the correct answer index of the list for 5 categories, namely "Science", "History", "Literature", "Geography" and "Entertainment". The purpose of these statements are for the game "Jeopardy!". Each statement in a category should consist of a value chosen from 200, 400, 600, 800 and 1000, with the statement of the smallest value being the easiest. Please generate the output as a json object with the following format (only the dictionary, no other text):
{
    "round1": [
        {
            "name": category,
            "questions": [
                {"value": value, "question": statement, "options": [options] (do not include "what is"), "correct": options list index}
            ]
        }
    ]
}
"""
    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model="gpt-5.1",
                messages=[{"role": "system", "content": "You are a helpful assistant."},
                          {"role": "user", "content": prompt}],
                temperature=0.7,
            )
            raw = response.choices[0].message.content
            # 提取JSON部分（去除可能的前后说明文字）
            start = raw.find('{')
            end = raw.rfind('}') + 1
            if start == -1 or end == 0:
                raise ValueError("No JSON object found")
            json_str = raw[start:end]
            data = json.loads(json_str)
            # 简单验证结构
            if "round1" in data and len(data["round1"]) == 5:
                return data
            else:
                print(f"Attempt {attempt+1}: Invalid structure, retrying...")
        except Exception as e:
            print(f"Attempt {attempt+1} failed: {e}")
            time.sleep(2)
    raise RuntimeError("Failed to generate valid questions after retries")