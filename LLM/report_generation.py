import requests
from dotenv import load_dotenv
import os

load_dotenv('.env')

hugging_face_api_key = os.getenv("HUGGING_FACE_API_KEY")

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
headers = {"Authorization": f"Bearer {hugging_face_api_key}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def report_generator(input):
    output = query({
        "inputs": """ Generate a short summary based on the given content""" + input,
        "parameters": {
            "return_full_text": False
        }
    })
    if isinstance(output, list) and len(output) > 0:
        return output[0].get('generated_text', '')
    return ''

